import datetime
import decimal
import json
import time
from datetime import timedelta
import sqlalchemy as sa
import logging as LOG
import ldap
from flask_cors import CORS
from flask import request , make_response , jsonify , Flask , send_from_directory
from flask_jwt_extended import (
    JWTManager , jwt_required , get_jwt_identity ,
    create_access_token , create_refresh_token ,
    jwt_refresh_token_required , get_raw_jwt
    )
from flask_migrate import Migrate
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import requests
import os , yaml

from urllib3.exceptions import InsecureRequestWarning

from userutils.userutils import get_user_fullname , get_user_group , get_user_title
from database.models import db , Dmpdata, Cvrdata, Sample , AppLog
import clientsideconfigs.gridconfigs as gridconfigs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

CORS(app)


class MyAdapter(HTTPAdapter) :
    def init_poolmanager(self , connections , maxsize , block=False) :
        self.poolmanager = PoolManager(num_pools=connections ,
                                       maxsize=maxsize ,
                                       block=block ,
                                       ssl_version=ssl.PROTOCOL_SSLv23)


s = requests.Session()
s.mount('https://' , MyAdapter())


####################################### app configuration settings ###################################

config = os.path.join(os.path.dirname(os.path.realpath(__file__)) , "lims_user_config")
config_options = yaml.safe_load(open(config , "r"))
USER = config_options['username']
PASSW = config_options['password']
ENV = config_options['env']
PORT = config_options['port_dev']
LIMS_API_ROOT = config_options['lims_end_point_dev']
if ENV== 'dev':
    PORT = config_options['port_dev']
    LIMS_API_ROOT = config_options['lims_end_point_dev']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_dev']
elif ENV== 'prod':
    PORT = config_options['port_prod']
    LIMS_API_ROOT = config_options['lims_end_point_prod']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_prod']
elif ENV == 'local':
    PORT = config_options['port_local']
    LIMS_API_ROOT = config_options['lims_end_point_local']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_local']

print(PORT)
print (LIMS_API_ROOT)

AUTH_LDAP_URL = config_options['auth_ldap_url']
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT , ldap.OPT_X_TLS_NEVER)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = config_options['secret_key']  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access' , 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)
CORS(app)

blacklist = set()


##################################### Logging settings ###############################################
log_file_path = ''
if ENV=='local' :
    log_file_path = config_options['log_file_local']
elif ENV == 'prod' or ENV == 'dev' :
    log_file_path = config_options['log_file_prod']

LOG.basicConfig(level=LOG.INFO ,
                filename=log_file_path.format(datetime.datetime.now().date()) ,
                format='%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')


##################################### DB Initialization###############################################

with app.app_context() :
    db.init_app(app)
    db.create_all()


#################################### APP CONSTANTS ###################################################

#ADMIN_GROUPS = ['AHDHD'] # add another admin group from PM's when available
#ADMIN_GROUPS = ['zzPDL_SKI_IGO_DATA', 'GRP_SKI_CMO_WESRecapture']
ADMIN_GROUPS = ['GRP_SKI_CMO_WESRecapture']
CLINICAL_GROUPS = ['clinical_group_update_when_available']
