import datetime
import decimal
import json
import time
from datetime import timedelta
import logging as LOG
import ldap
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import requests
import os, yaml
from database.models import db, User, Sample, AppLog, BlacklistToken
import clientsideconfigs.gridconfigs as gridconfigs


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

CORS(app)

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
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri']
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)
CORS(app)

blacklist= set()
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
    log_entry = LOG.info("testing")
    AppLog.log(AppLog(level="INFO", process="Root", user="Admin", message="Testing the logging to db."))
    return jsonify(columnHeaders = gridconfigs.clinicalColdHeaders, columns = gridconfigs.clinicalColumns, settings=gridconfigs.settings), 200


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
            AppLog.log(AppLog(level="INFO", process="Root", user=username,
                              message="Successfully authenticated and logged into the app."))
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = make_response(jsonify(valid=True, username=username, access_token=access_token, refresh_token=refresh_token), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ldap.INVALID_CREDENTIALS:
            response = make_response(jsonify(valid=False), 200, None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(AppLog(level="WARNING", process="Root", user=username,
                              message="Invalid username or password."))
            return make_response(response)
        except ldap.OPERATIONS_ERROR as e:
            response = make_response(jsonify(valid=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(AppLog(level="ERROR", process="Root", user=username,
                              message="ldap OPERATION ERROR occured. {}".format(e)))
            return make_response(response)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    try:
        current_user = get_jwt_identity()
        response = {
            'access_token': create_access_token(identity=current_user),
            'refresh_token': create_refresh_token(identity=current_user)
        }
        AppLog.log(AppLog(level="INFO", process="Root", user=current_user,
                          message="Successfully refreshed jwt token for user "+ current_user))
        return jsonify(response), 200
    except Exception as e:
        AppLog.log(AppLog(level="ERROR", process="Root", user=current_user,
                          message="Failed to refresh access token for user " + current_user))
        response = {
            'access_token': "",
            'refresh_token': "",
            'error': True,
            'message': "Failed to refresh access token. Please try to refresh page and login again."
        }
        return jsonify(response), 200



@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    try:
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        AppLog.log(AppLog(level="INFO", process="Root", user=current_user,
                          message="Successfully logged out user " + current_user))
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        AppLog.log(AppLog(level="ERROR", process="Root", user=current_user,
                          message="Error while logging out user " + current_user))
        return jsonify({"message": "Error while logging out user " + current_user,
                        "error": repr(e)}), 200


@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


def save_to_db(data):
    data_to_json = json.loads(data)
    """
    Method to save data to Sample Tracking database.
    """
    for item in data_to_json:
        print(item.get("recordId"))
        record_ids = []
        db.session.autoflush = False
        existing = Sample.query.filter_by(sampleid=item.get("sampleId")).first()
        if existing is None:
            print(" Not Existing True")
            sample = Sample(item.get("sampleId"), item.get("userSampleId"), item.get("cmoSampleId"), item.get("cmoPatientId"), item.get("dmpSampleId"), item.get("dmpPatientId"),
                             item.get("mrn"), item.get("sex"), item.get("sampleType"), item.get("sampleClass"), item.get("tumorType"), item.get("parentalTumorType"),
                             item.get("tissueSite"), item.get("molecularAccessionNum"), item.get("collectionYear"), item.get("dateDmpRequest"), item.get("dmpRequestId"), item.get("igoRequestId"),
                             item.get("dateIgoReceived"), item.get("igoCompleteDate"), item.get("applicationRequested"), item.get("baitsetUsed"), item.get("sequencerType"), item.get("projectTitle"),
                             item.get("labHead"), item.get("ccFund"), item.get("scientificPi"), item.get("consentPartAStatus"), item.get("consentPartCStatus"), item.get("sampleStatus"),
                             item.get("accessLevel"), item.get("clinicalTrial"), item.get("sequencingSite"), item.get("piRequestDate"), item.get("pipeline"), item.get("tissueType"), item.get("collaborationCenter"), item.get("limsRecordId")
            )
            db.session.add(sample)
            record_ids.append(item.get("recordId"))

        elif existing:
            print("existing true")
            api_update_sample(db, item)
    db.session.commit()
    db.session.flush()
    AppLog.log(AppLog(level="INFO", process="werkzeug",
                          message="Added {0} new records to the Sample Tracking Database".format(len(record_ids))))
    response = make_response(jsonify(data=(str(record_ids))), 200 , None)

    return len(record_ids)


@app.route("/get_wes_data", methods=['GET'])
def get_wes_data():
    """
    End point to get WES Sample data from LIMS using timestamp. User can either pass "timestamp" parameter (miliseconds) to this endpoint
    to fetch sample data that was created after the timestamp provided. Or use can call the endpoint without any parameters and the end point will fetch data for last 24 hours.
    :return:
    """
    try:
        timestamp = 0
        if request.args.get("timestamp") is not None:
            timestamp = request.args.get("timestamp")
            LOG.info("Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query")
            AppLog.log(AppLog(level="INFO", process="werkzeug", message="Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query"))
        else:
            timestamp = time.mktime((datetime.datetime.today() - timedelta(days=1.1)).timetuple()) * 1000 # 1.1 to account for lost during the firing of query. It is better to have some time overlap to get all the data.
            LOG.info("Starting WES Sample query after calculating time: " + str(timestamp) + ", provided to the endpoint by user.")
            AppLog.log(AppLog(level="INFO", process="werkzeug", message="Starting WES Sample query after calculating time: " + str(timestamp) + ", provided to the endpoint by user."))
        if int(timestamp) > 0:
            print(timestamp)
            LOG.info("Starting query : " + "http://localhost:5007" + "/timestamp=" + str(int(timestamp)))
            r = s.get("http://localhost:5007" + "/getWESSampleData?timestamp=" + str(int(timestamp)), auth=(USER, PASSW), verify=False)
            data = r.content.decode("utf-8", "strict")
            ids = save_to_db(data)
            LOG.info("Added {0} new records to the Sample Tracking Database".format(ids))
            AppLog.log(AppLog(level="INFO", process="werkzeug", message="Added {0} new records to the Sample Tracking Database".format(ids)))
            response = make_response(jsonify(data=(str(ids))), 200 , None)
            return response
    except Exception as e:
        AppLog.log(AppLog(level="ERROR", process="werkzeug", message=repr(e)))
        LOG.error(e, exc_info=True)
        response = make_response(jsonify(data="" , error="There was a problem processing the request."), 200 , None)
        return response

def api_update_sample(db, item):
    try:
        print (item.get("sampleId"))
        sample = db.session.query(Sample).filter_by(sampleid=item.get("sampleId"), lims_recordId=item.get("limsRecordId")).first()
        sample.sampleid=item.get("sampleId")
        sample.user_sampleid=item.get("userSampleId")
        sample.cmo_sampleid = item.get("cmoSampleId")
        sample.cmo_patientid= item.get("cmoPatientId")
        sample.dmp_sampleid= item.get("dmpSampleId")
        sample.dmp_patientid= item.get("dmpPatientId")
        sample.mrn= item.get("mrn")
        sample.sex= item.get("sex")
        sample.sample_type= item.get("sampleType")
        sample.sample_class= item.get("sampleClass")
        sample.tumor_type= item.get("tumorType")
        sample.parental_tumortype= item.get("parentalTumorType")
        sample.tumor_site= item.get("tissueSite")
        sample.molecular_accession_num= item.get("molecularAccessionNum")
        sample.collection_year= item.get("collectionYear")
        sample.date_dmp_request= item.get("dateDmpRequest")
        sample.dmp_requestid= item.get("dmpRequestId")
        sample.igo_requestid= item.get("igoRequestId")
        sample.date_igo_received= item.get("dateIgoReceived")
        sample.date_igo_complete= item.get("igoCompleteDate")
        sample.application_requested= item.get("applicationRequested")
        sample.baitset_used= item.get("baitsetUsed")
        sample.sequencer_type= item.get("sequencerType")
        sample.project_title= item.get("projectTitle")
        sample.lab_head= item.get("labHead")
        sample.cc_fund= item.get("ccFund")
        sample.consent_parta_status= item.get("consentPartAStatus")
        sample.consent_partc_status= item.get("consentPartCStatus")
        sample.sample_status= item.get("sampleStatus")
        db.session.commit()
    except Exception as e:
        LOG.error(e, exc_info=True)


@app.route("/update", methods=['POST'])
@jwt_required
def user_update_sample(session, item):
    try:
      sample = session.query(Sample).filter_by(sampleid=item.get("sampleId"), lims_recordId=item.get("limsRecordId")).first()
      sample.sampleid=item.get("sampleId")
      sample.user_sampleid=item.get("userSampleId")
      sample.cmo_sampleid = item.get("cmoSampleId")
      sample.cmo_patientid= item.get("cmoPatientId")
      sample.dmp_sampleid= item.get("dmpSampleId")
      sample.dmp_patientid= item.get("dmpPatientId")
      sample.mrn= item.get("mrn")
      sample.sex= item.get("sex")
      sample.sample_type= item.get("sampleType")
      sample.sample_class= item.get("sampleClass")
      sample.tumor_type= item.get("tumorType")
      sample.parental_tumortype= item.get("parentalTumorType")
      sample.tumor_site= item.get("tissueSite")
      sample.molecular_accession_num= item.get("molecularAccessionNum")
      sample.collection_year= item.get("collectionYear")
      sample.date_dmp_request= item.get("dateDmpRequest")
      sample.dmp_requestid= item.get("dmpRequestId")
      sample.igo_requestid= item.get("igoRequestId")
      sample.date_igo_received= item.get("dateIgoReceived")
      sample.date_igo_complete= item.get("igoCompleteDate")
      sample.application_requested= item.get("applicationRequested")
      sample.baitset_used= item.get("baitsetUsed")
      sample.sequencer_type= item.get("sequencerType")
      sample.project_title= item.get("projectTitle")
      sample.lab_head= item.get("labHead")
      sample.cc_fund= item.get("ccFund")
      sample.consent_parta_status= item.get("consentPartAStatus")
      sample.consent_partc_status= item.get("consentPartCStatus")
      sample.sample_status= item.get("sampleStatus")
      session.commit()
    except Exception as e:
        LOG.error(e, exc_info=True)


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

def get_column_configs(role):
    if role is 'clinical':
        return gridconfigs.clinicalColdHeaders, gridconfigs.clinicalColumns, gridconfigs.settings
    if role is 'admin':
        return gridconfigs.adminColdHeaders, gridconfigs.adminColumns , gridconfigs.settings
    else:
        return gridconfigs.nonClinicalColdHeaders, gridconfigs.nonClinicalColumns , gridconfigs.settings

@app.route("/search_data", methods=['POST'])
@jwt_required
def search_data():
    """
    From the client_side, user will search for samples using either "MRN's" or "Tumor_Type". Along with search words,
    "search_type (MRN || Tumor Type)" is also passed to this api route. The logic is to call different LIMSRest end points
    based on the search_type parameter to get appropriate data and send as Response to client side.
    :return:
    """
    if request.method == "POST":
        query_data = request.get_json(silent=True)
        print(query_data)
        print(request.headers['Authorization'])
        search_keywords = query_data.get('searchtext')
        search_type = query_data.get('searchtype')
        colHeaders, columns, settings = get_column_configs("admin")

        if search_keywords is not None and search_type.lower() == "mrn":
            search_keywords = [x.strip() for x in search_keywords.split(',')]
            result = db.session.query(Sample).filter(Sample.mrn.in_((search_keywords))).all()
            response = make_response(jsonify(data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                        separators=(',', ': '))), colHeaders=colHeaders, columns=columns, settings=settings, ), 200, None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return make_response(response)
        elif search_keywords is not None and search_type.lower() == "tumor type":
            search_keywords = search_keywords.split(",")
            result = db.session.query(Sample).filter(Sample.tumor_type.in_((search_keywords))).all()
            response = make_response(jsonify(data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                        separators=(',', ': '))), colHeaders=colHeaders, columns=columns, settings=settings), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return make_response(response)
        else:
            response = make_response(jsonify(json.dumps(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)), 200, None))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return make_response(response)

if __name__ == '__main__':
    app.run(debug=True)
