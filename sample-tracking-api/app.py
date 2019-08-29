import datetime
import decimal
import json
import pickle
import time
from datetime import timedelta
import logging as LOG
import ldap
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import requests
import os, yaml
from database.models import db, User, Samples

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_SSLv23)
                #ssl_version=ssl.PROTOCOL_SSLv3)


s = requests.Session()
s.mount('https://', MyAdapter())

####################################### app configuration settings ###################################

config = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lims_user_config")
config_options = yaml.safe_load(open(config, "r"))
USER = config_options['username']
PASSW = config_options['password']
PORT = config_options['port']
LIMS_API_ROOT =config_options['lims_end_point']
AUTH_LDAP_URL = config_options['auth_ldap_url']
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri']
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
CORS(app)

##################################### Logging settings ###############################################

LOG.basicConfig(level = LOG.INFO,
                    filename = "./logs/sample-tracking-db-{}.log".format(datetime.datetime.now().date()),
                    format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

##################################### DB Initialization###############################################

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route("/")
def index():
    return ""


def get_ldap_connection():
    conn = ldap.initialize(AUTH_LDAP_URL)
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        login_credentials = request.get_json(silent=True)
        username = login_credentials.get('username')
        password = login_credentials.get('password')
        try:
            conn = get_ldap_connection()
            conn.simple_bind_s('%s@mskcc.org' % username, password)
            attrs = ['sAMAccountName', 'displayName', 'memberOf', 'title']
            result = conn.search_s(
                'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG',
                ldap.SCOPE_SUBTREE,
                'sAMAccountName='+ username,
                attrs,
            )
            print(result)
            conn.unbind_s()
            response = make_response(jsonify(valid=True), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ldap.INVALID_CREDENTIALS:
            return make_response(jsonify(valid=False), 200, None)
        except ldap.OPERATIONS_ERROR :
            return make_response(jsonify(valid=False), 200, None)


def save_to_db(data):
    data_to_json = json.loads(data)
    """
    Method to save data to Sample Tracking database.
    """
    for item in data_to_json:
        print(item.get("recordId"))
        record_ids = []
        db.session.autoflush = False
        existing = Samples.query.filter_by(sampleid=item.get("sampleId")).first()
        if existing is None:
            print("True")
            sample = Samples(item.get("sampleId"), item.get("otherSampleId"), item.get("correctedCmoId"), item.get("requestId"), item.get("currentStatusIGO"), item.get("pi"),
                             item.get("investigator"), item.get("dateCreated"), item.get("dateIgoReceived"), item.get("dateIGOComplete"), item.get("recordId"), item.get("baitset"),
                             item.get("investigatorSampleId"), item.get("patientId"), item.get("dataAnalyst"), item.get("sample_type"), item.get("tumor_type"), item.get("sample_class"),
                             item.get("tumor_site"), item.get("tissue_location"), item.get("sex"), item.get("mrn"), item.get("m_accession_number"), item.get("oncotree_code"), item.get("parental_tumortype"),
                             item.get("collection_year"), item.get("dmp_sampleid"), item.get("dmp_patientid"), item.get("registration_12_245AC"), item.get("vaf"), item.get("facets")
            )
            db.session.add(sample)
            db.session.commit()
            db.session.flush()
            record_ids.append(item.get("recordId"))
    return record_ids


@app.route("/get_wes_data", methods=['GET'])
def get_wes_data():

    """
    End point to get WES Sample data from LIMS using timestamp. User can either pass "timestamp" parameter (miliseconds) to this endpoint
    to fetch sample data that was created after the timestamp provided. Or use can call the endpoint without any parameters and the
    :return:
    """
    try:
        timestamp = 0
        if request.args.get("timestamp") is not None:
            timestamp = request.args.get("timestamp")
            LOG.info("Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query")
        else:
            timestamp = time.mktime((datetime.datetime.today() - timedelta(days=1.1)).timetuple()) * 1000 # 1.1 to account for lost during the firing of query. It is better to have some time overlap to get all the data.
            LOG.info("Starting WES Sample query after calculating time: " + str(timestamp) + ", provided to the endpoint by user.")
        if int(timestamp) > 0:
            print(timestamp)
            LOG.info("Starting query : " + "http://localhost:8080" + "/LimsRest/getWESSampleData?time=" + str(int(timestamp)))
            r = s.get("http://localhost:8080" + "/LimsRest/getWESSampleData?time=" + str(int(timestamp)), auth=(USER, PASSW), verify=False)
            data = r.content.decode("utf-8", "strict")
            ids = save_to_db(data)
            LOG.info("Added '" + len(ids) + "' new records to the Sample Tracking Database")
            return str(ids)
    except Exception as e:
        print(e)
        LOG.error(e, exc_info=True)


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


@app.route("/search_data", methods=['GET', 'POST'])
def search_data():

    """
    From the client_side, user will search for samples using either "MRN's" or "Tumor_Type". Along with search words,
    "search_type (MRN || Tumor Type)" is also passed to this api route. The logic is to call different LIMSRest end points
    based on the search_type parameter to get appropriate data and send as Response to client side.
    :return:
    """
    if request.method == "POST":
        query_data = request.get_json(silent=True)
        search_keywords = query_data.get('searchtext')
        search_type = query_data.get('searchtype')
        print(search_keywords)
        print(search_type)

        if search_keywords is not None and search_type.lower() == "mrn":
            search_keywords = [x.strip() for x in search_keywords.split(',')]
            result = db.session.query(Samples).filter(Samples.other_sampleid.in_((search_keywords))).all()
            response_object = json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                        separators=(',', ': '))
            return make_response(jsonify(response_object), 200)
        elif search_keywords is not None and search_type.lower() == "tumor type":
            search_keywords = search_keywords.split(",")
            result = db.session.query(Samples).filter(Samples.tumor_type.in_((search_keywords))).all()
            response_object = json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                        separators=(',', ': '))
            return make_response(jsonify(response_object), 200)
        else:
            return make_response(jsonify(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)), 200, None)


if __name__ == '__main__':
    app.run(debug=True)