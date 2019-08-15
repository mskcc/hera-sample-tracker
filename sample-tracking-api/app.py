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

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route("/")
def index():
    return "Hello Hera...What do you want?"


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
            attrs = ['memberOf']
            attrs = ['sAMAccountName', 'displayName', 'memberOf', 'title']
            result = conn.search_s(
                'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG',
                ldap.SCOPE_SUBTREE,
                'sAMAccountName=wagnerl',
                attrs,
            )
            conn.unbind_s()
            response = make_response(jsonify(valid=True), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ldap.INVALID_CREDENTIALS:
            return make_response(jsonify(valid=False), 200, None)
        except ldap.OPERATIONS_ERROR :
            return make_response(jsonify(valid=False), 200, None)


@app.route("/search_data", methods=['GET','POST'])
def search_data():
    '''
    From the client_side, user will search for samples using either "MRN's" or "Tumor_Type". Along with search words,
    "search_type (MRN || Tumor Type)" is also passed to this api route. The logic is to call different LIMSRest end points
    based on the search_type parameter to get appropriate data and send as Response to client side.
    :return:
    '''
    if request.method == "POST":
        query_data = request.get_json(silent=True)
        search_keywords = query_data.get('searchtext')
        search_type = query_data.get('searchtype')

        print(search_keywords)
        print(search_type)
        if search_keywords is not None and search_type.lower() == "mrn":
            r = s.get("http://localhost:8080" + "/getWESSampleData?sampleIds=" + search_keywords + "&searchType=" + search_type, auth=(USER, PASSW), verify=False)
            data = r.content.decode("utf-8", "strict")
            return make_response(jsonify(data), 200)
        elif search_keywords is not None and search_type.lower() == "tumor type":
            r = s.get("http://localhost:8080" + "/getWESSampleData?sampleIds=" + search_keywords + "&searchType=" + search_type, auth=(USER, PASSW), verify=False)
            data = r.content.decode("utf-8", "strict")
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)), 200, None)


if __name__ == '__main__':
    app.run(debug=True)