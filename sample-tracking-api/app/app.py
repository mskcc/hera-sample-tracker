import datetime
import decimal
import json
import time
from datetime import timedelta
import logging as LOG
import ldap
from flask_cors import CORS
from flask import request , make_response , jsonify , Flask , send_from_directory
from flask_jwt_extended import (
    JWTManager , jwt_required , get_jwt_identity ,
    create_access_token , create_refresh_token ,
    jwt_refresh_token_required , get_raw_jwt
    )
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import requests
import os , yaml
from userutils.userutils import get_user_fullname , get_user_group , get_user_title
from database.models import db , Sample , AppLog
import clientsideconfigs.gridconfigs as gridconfigs

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
if (ENV== 'dev'):
    PORT = config_options['port_dev']
    LIMS_API_ROOT = config_options['lims_end_point_dev']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_dev']
elif (ENV== 'prod'):
    PORT = config_options['port_prod']
    LIMS_API_ROOT = config_options['lims_end_point_prod']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_prod']
elif (ENV == 'local'):
    PORT = config_options['port_dev']
    LIMS_API_ROOT = config_options['lims_end_point_dev']
    app.config['SQLALCHEMY_DATABASE_URI'] = config_options['db_uri_local']

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

# ADMIN_GROUPS = ['AHDHD'] # add another admin group from PM's when available
ADMIN_GROUPS = ['zzPDL_SKI_IGO_DATA' , 'GRP_SKI_CMO_WESRecapture']
CLINICAL_GROUPS = ['clinical_group_update_when_available']


######################################################################################################

@app.route("/" , methods=['GET' , 'POST'])
def index() :
    '''
    This method is here only to test at times if the app is working correctly.
    :return:
    '''
    log_entry = LOG.info("testing")
    AppLog.log(AppLog(level="INFO" , process="Root" , user="Admin" , message="Testing the logging to db."))
    return jsonify(columnHeaders=gridconfigs.clinicalColdHeaders , columns=gridconfigs.clinicalColumns ,
                   settings=gridconfigs.settings) , 200


def get_ldap_connection() :
    conn = ldap.initialize(AUTH_LDAP_URL)
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS , 0)
    return conn


@app.route("/login" , methods=['GET' , 'POST'])
def login() :
    '''
    Login user using ldap connection and validate user role.
    :return:
    '''
    if request.method == "POST" :
        login_credentials = request.get_json(silent=True)
        username = login_credentials.get('username')
        password = login_credentials.get('password')
        try :
            conn = get_ldap_connection()
            conn.simple_bind_s('%s@mskcc.org' % username , password)
            attrs = ['sAMAccountName' , 'displayName' , 'memberOf' , 'title']
            result = conn.search_s(
                'DC=MSKCC,DC=ROOT,DC=MSKCC,DC=ORG' ,
                ldap.SCOPE_SUBTREE ,
                'sAMAccountName=' + username ,
                attrs ,
                )
            role = 'user'

            user_fullname = '' #get_user_fullname(result)
            user_title = get_user_title(result)
            user_groups = get_user_group(result)
            # check user role
            if len(set(user_groups).intersection(set(ADMIN_GROUPS))) > 0 :
                role = 'admin'
            elif len(set(user_groups).intersection(set(CLINICAL_GROUPS))) > 0 :
                role = 'clinical'
            conn.unbind_s()
            LOG.info("Successfully authenticated and logged {} into the app with role {}.".format(username , role))
            AppLog.log(AppLog(level="INFO" , process="Root" , user=username ,
                              message="Successfully authenticated and logged into the app."))
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = make_response(
                jsonify(valid=True , username=username , access_token=access_token , refresh_token=refresh_token ,
                        role=role , title=user_title , user_fullname=user_fullname) ,
                200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
        except ldap.INVALID_CREDENTIALS :
            response = make_response(jsonify(valid=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(AppLog(level="WARNING" , process="Root" , user=username ,
                              message="Invalid username or password."))
            return make_response(response)
        except ldap.OPERATIONS_ERROR as e :
            response = make_response(jsonify(valid=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(AppLog(level="ERROR" , process="Root" , user=username ,
                              message="ldap OPERATION ERROR occured. {}".format(e)))
            return make_response(response)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token) :
    '''
    Add JWT token to blacklist.
    :param decrypted_token:
    :return:
    '''
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/refresh_token' , methods=['POST'])
@jwt_refresh_token_required
def refresh() :
    '''
    Refresh JWT token when needed. Not being used as of now.
    :return:
    '''
    try :
        current_user = get_jwt_identity()
        response = {
            'access_token' : create_access_token(identity=current_user) ,
            'refresh_token' : create_refresh_token(identity=current_user)
            }
        AppLog.log(AppLog(level="INFO" , process="Root" , user=current_user ,
                          message="Successfully refreshed jwt token for user " + current_user))
        return jsonify(response) , 200
    except Exception as e :
        AppLog.log(AppLog(level="ERROR" , process="Root" , user=current_user ,
                          message="Failed to refresh access token for user " + current_user))
        response = {
            'access_token' : "" ,
            'refresh_token' : "" ,
            'error' : True ,
            'message' : "Failed to refresh access token. Please try to refresh page and login again."
            }
        return jsonify(response) , 200


@app.route('/logout' , methods=['POST'])
@jwt_required
def logout() :
    try :
        if request.method == "POST" :
            user_data = request.get_json(silent=True)
            print(user_data)
            current_user = get_jwt_identity()
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            AppLog.log(AppLog(level="INFO" , process="Root" , user=current_user ,
                              message="Successfully logged out user " + current_user))
            response = make_response(
                jsonify(success=True ,
                        valid=True ,
                        username=None ,
                        access_token=None ,
                        refresh_token=None ,
                        message="Successfully logged out user " + current_user) ,
                200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
    except Exception as e :
        AppLog.log(AppLog(level="ERROR" ,
                          process="Root" ,
                          user=current_user ,
                          message="Error while logging out user " + current_user))
        response = make_response(
            jsonify(valid=False ,
                    username=None ,
                    access_token=None ,
                    refresh_token=None ,
                    message="Error while logging out user " + current_user ,
                    error=repr(e)) ,
            200 , None)
        response.headers.add('Access-Control-Allow-Origin' , '*')
        return response


@jwt_refresh_token_required
def logout2() :
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({ "success" : True , "msg" : "Successfully logged out" }) , 200


@app.route("/get_wes_data" , methods=['GET'])
def get_wes_data() :
    """
    End point to get WES Sample data from LIMS using timestamp. User can either pass "timestamp" parameter (miliseconds) to this endpoint
    to fetch sample data that was created after the timestamp provided. Or user can call the endpoint without any parameters and the end point will fetch data for last 24 hours.
    :return:
    """
    try :
        timestamp = 0
        if request.args.get("timestamp") is not None :
            timestamp = request.args.get("timestamp")
            LOG.info("Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query")
            AppLog.log(AppLog(level="INFO" , process="werkzeug" , user='api',
                              message="Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query"))
        else :
            timestamp = time.mktime((datetime.datetime.today() - timedelta(
                days=1.1)).timetuple()) * 1000  # 1.1 to account for lost during the firing of query. It is better to have some time overlap to get all the data.
            LOG.info("Starting WES Sample query after calculating time: " + str(
                timestamp) + ", provided to the endpoint by user.")
            AppLog.log(AppLog(level="INFO" , process="werkzeug" , user='api',
                              message="Starting WES Sample query after calculating time: " + str(
                                  timestamp) + ", provided to the endpoint by user."))
        if int(timestamp) > 0 :
            print(timestamp)
            LOG.info(
                "Starting query : " + LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)))
            r = s.get(LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)) ,
                      auth=(USER , PASSW) , verify=False)
            data = r.content.decode("utf-8" , "strict")
            ids = save_to_db(data)
            LOG.info("Added {0} new records to the Sample Tracking Database".format(ids))
            AppLog.log(AppLog(level="INFO" , process="werkzeug" , user='api',
                              message="Added {0} new records to the Sample Tracking Database".format(ids)))
            response = make_response(jsonify(data=(str(ids))) , 200 , None)
            return response
    except Exception as e :
        AppLog.log(AppLog(level="ERROR" , process="werkzeug" , user='api', message=repr(e)))
        LOG.error(e , exc_info=True)
        response = make_response(jsonify(data="" , error="There was a problem processing the request.") , 200 , None)
        return response


def save_to_db(data) :
    '''
    Method to save data to Sample Tracking database. The method will update if the record already exists/create new.
    The existence of a record is validated using limsSampleRecordId and limsTrackerRecordId.
    :param data:
    :return:
    '''
    try :
        data_to_json = json.loads(data)

        record_ids = []
        for item in data_to_json :
            db.session.autoflush = False
            ''' check if the record already exists and is IGO processed Sample. If a sample was processed by IGO, 
                it should have both "limsSampleRecordId" and "limsTrackerRecordId" values. '''
            existing = None
            if item.get("limsSampleRecordId") is not None :
                existing = Sample.query.filter_by(lims_sample_recordid=item.get("limsSampleRecordId") ,
                                                  lims_tracker_recordid=item.get("limsTrackerRecordId")).first()

            '''If the record does not exist, create a new record.'''
            if existing is None :
                print(" Not Existing True")
                print(item.get("limsTrackerRecordId"))
                sample = Sample(sampleid=item.get("sampleId") , user_sampleid=item.get("userSampleId") ,
                                cmo_sampleid=item.get("cmoSampleId") , cmo_patientid=item.get("cmoPatientId") ,
                                dmp_sampleid=item.get("dmpSampleId") , dmp_patientid=item.get("dmpPatientId") ,
                                mrn=item.get("mrn") , sex=item.get("sex") , sample_type=item.get("sampleType") ,
                                sample_class=item.get("sampleClass") , tumor_type=item.get("tumorType") ,
                                parental_tumortype=item.get("parentalTumorType") ,
                                tumor_site=item.get("tissueSite") ,
                                molecular_accession_num=item.get("molecularAccessionNum") ,
                                collection_year=item.get("collectionYear") ,
                                date_dmp_request=item.get("dateDmpRequest") ,
                                dmp_requestid=item.get("dmpRequestId") , igo_requestid=item.get("igoRequestId") ,
                                date_igo_received=item.get("dateIgoReceived") ,
                                date_igo_complete=item.get("igoCompleteDate") ,
                                application_requested=item.get("applicationRequested") ,
                                baitset_used=item.get("baitsetUsed") , sequencer_type=item.get("sequencerType") ,
                                project_title=item.get("projectTitle") ,
                                lab_head=item.get("labHead") , cc_fund=item.get("ccFund") ,
                                scientific_pi=item.get("scientificPi") ,
                                consent_parta_status=item.get("consentPartAStatus") ,
                                consent_partc_status=item.get("consentPartCStatus") ,
                                sample_status=item.get("sampleStatus") ,
                                access_level=item.get("accessLevel") , clinical_trial=item.get("clinicalTrial") ,
                                seqiencing_site=item.get("sequencingSite") , pi_request_date=item.get("piRequestDate") ,
                                pipeline=item.get("pipeline") , tissue_type=item.get("tissueType") ,
                                collaboration_center=item.get("collaborationCenter") ,
                                lims_sample_recordid=item.get("limsSampleRecordId") ,
                                lims_tracker_recordid=item.get("limsTrackerRecordId")
                                )
                db.session.add(sample)
                db.session.commit()
                db.session.flush()
                record_ids.append(item.get("limsTrackerRecordId"))

            # If the record already exists, update the record.
            elif existing :
                print("existing true")
                api_update_sample(db , item)

            ''' check if the record already exists and is non IGO processed Sample. If a sample was not processed by IGO, 
                        it should only have "limsTrackerRecordId" value. '''
            partial_existing = None
            if item.get("limsSampleRecordId") is None and item.get("limsTrackerRecordId") is not None :
                partial_existing = Sample.query.filter_by(lims_sample_recordid=None ,
                                                          lims_tracker_recordid=item.get("limsTrackerRecordId")).first()
            '''If a non IGO sample exists, then update the values.'''
            if partial_existing :
                api_update_sample(db , item);

        AppLog.log(AppLog(level="INFO" , process="root" , user='api',
                          message="Added {} new records to the Sample Tracking Database".format(len(record_ids))))
        return len(record_ids)
    except Exception as e :
        AppLog.log(AppLog(level="ERROR" , process="root" , user='api',
                          message="{} Error occured while adding records to the Sample Tracking Database.\n{}".format(
                              e)))
        return None


def api_update_sample(db , item) :
    '''
    The method to update an existing record, done by api call. Not called by frontend.
    :param db:
    :param item:
    :return:
    '''
    try :
        sample = None
        if item.get("limsSampleRecordId") is not None :
            print(item.get("sampleId"))
            sample = db.session.query(Sample).filter_by(lims_sample_recordid=item.get("limsSampleRecordId") ,
                                                        lims_tracker_recordid=item.get("limsTrackerRecordId")).first()
            print("updating sample with both record ids")
        else :
            print(item.get("sampleId"))
            sample = db.session.query(Sample).filter_by(lims_sample_recordid=None ,
                                                        lims_tracker_recordid=item.get("limsTrackerRecordId")).first()
            print("updating sample with no sample record id")
        sample = db.session.query(Sample).filter_by(lims_tracker_recordid=item.get("limsTrackerRecordId")).first()
        sample.sampleid = item.get("sampleId")
        sample.user_sampleid = item.get("userSampleId")
        sample.cmo_sampleid = item.get("cmoSampleId")
        sample.cmo_patientid = item.get("cmoPatientId")
        sample.dmp_sampleid = item.get("dmpSampleId")
        sample.dmp_patientid = item.get("dmpPatientId")
        sample.mrn = item.get("mrn")
        sample.sex = item.get("sex")
        sample.sample_type = item.get("sampleType")
        sample.sample_class = item.get("sampleClass")
        sample.tumor_type = item.get("tumorType")
        sample.parental_tumortype = item.get("parentalTumorType")
        sample.tumor_site = item.get("tissueSite")
        sample.molecular_accession_num = item.get("molecularAccessionNum")
        sample.collection_year = item.get("collectionYear")
        sample.date_dmp_request = item.get("dateDmpRequest")
        sample.dmp_requestid = item.get("dmpRequestId")
        sample.igo_requestid = item.get("igoRequestId")
        sample.date_igo_received = item.get("dateIgoReceived")
        sample.date_igo_complete = item.get("igoCompleteDate")
        sample.application_requested = item.get("applicationRequested")
        sample.baitset_used = item.get("baitsetUsed")
        sample.sequencer_type = item.get("sequencerType")
        sample.project_title = item.get("projectTitle")
        sample.lab_head = item.get("labHead")
        sample.cc_fund = item.get("ccFund")
        sample.consent_parta_status = item.get("consentPartAStatus")
        sample.consent_partc_status = item.get("consentPartCStatus")
        sample.sample_status = item.get("sampleStatus")
        if item.get("limsSampleRecordId") is not None and sample.lims_sample_recordid is None :
            sample.lims_sample_recordid = item.get("limsSampleRecordId")
        db.session.commit()
        db.session.flush()
    except Exception as e :
        LOG.error(e , exc_info=True)


@app.route("/save_sample_changes" , methods=['POST'])
@jwt_required
def save_sample_changes() :
    '''
    Method to save samples when users call the save method from frontend app via button click events.
    :return: response
    '''
    try :
        if request.method == "POST" :
            sample_data = request.get_json(silent=True)
            for item in sample_data :
                user_update_sample(db.session , item)
            AppLog.log(
                AppLog(level="INFO" , process="root" , user=get_jwt_identity(), message="updated {} samples by user".format(len(sample_data))))
            LOG.info("update {} samples by user".format(len(sample_data)))
            response = make_response(
                jsonify(
                    success=True ,
                    message="Data updated successfully." ,
                    ) ,
                200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
    except Exception as e :
        LOG.error(repr(e))
        AppLog.log(
            AppLog(level="ERROR" , process="root" , user=get_jwt_identity(), message="error while updating the samples {}".format(repr(e))))
        response = make_response(
            jsonify(success=False ,
                    message="Save operation failed. Plese try again later." ,
                    ) ,
            200 , None)
        response.headers.add('Access-Control-Allow-Origin' , '*')
        return response


def user_update_sample(session , item) :
    '''
    Sometimes users will update some editable columns on the clientside. These updated values should be updated to the database.
    Only the fields that are editable on the front end will be updated.
    :param session:
    :param item:
    :return:
    '''
    try :
        sample = session.query(Sample).filter_by(lims_tracker_recordid=item.get("lims_tracker_recordid")).first()
        if sample is not None :
            sample.data_analyst = item.get("data_analyst")
            sample.scientific_pi = item.get("scientific_pi")
            sample.access_level = item.get("access_level")
            sample.clinical_trial = item.get("clinical_trial")
            sample.seqiencing_site = item.get("seqiencing_site")
            sample.pi_request_date = item.get("pi_request_date")
            sample.pipeline = item.get("pipeline")
            sample.tissue_type = item.get("tissue_type")
            sample.collaboration_center = item.get("collaboration_center")
            session.commit()
            session.flush()


    except Exception as e :
        LOG.error(e , exc_info=True)


def alchemy_encoder(obj) :
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj , datetime.date) :
        return obj.isoformat()
    elif isinstance(obj , decimal.Decimal) :
        return float(obj)


def get_column_configs(role) :
    '''
    Method to return column configurations based on user role. Not all users are authorized to see all the data returned by this server.
    :param role:
    :return: column configurations
    '''
    print(role)
    if role == 'clinical' :
        return gridconfigs.clinicalColHeaders , gridconfigs.clinicalColumns , gridconfigs.settings
    elif role == 'admin' :
        return gridconfigs.adminColHeaders , gridconfigs.adminColumns , gridconfigs.settings
    elif role == 'user' :
        return gridconfigs.nonClinicalColHeaders , gridconfigs.nonClinicalColumns , gridconfigs.settings


@app.route("/download_data" , methods=['POST'])
@jwt_required
def download_data() :
    '''
    Method to log the download data event from the forntend.
    :return:
    '''
    if request.method == "POST" :
        query_data = request.get_json(silent=True)
        print(query_data)
        num_samples = query_data.get('data_length')
        user = query_data.get('user')
        username = user.get('username')
        role = user.get('role')
        try :
            LOG.info("User {} with role {} downloaded data for {} samples".format(username , role ,
                                                                                      num_samples))
            AppLog.log(
                AppLog(level="INFO" , process="root" , user=username,
                       message="User {} with role {} downloaded data for {} samples".format(username , role ,
                                                                                            num_samples)))
            response = make_response(jsonify(
                success=True ), 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
        except Exception as e :
            AppLog.log(
                AppLog(level="ERROR" , process="root" , user=username,
                       message="Error occured while logging the data download event\n{}".format(e)))
            response = make_response(jsonify(
                success=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response

@app.route("/search_data" , methods=['POST'])
@jwt_required
def search_data() :
    """
    From the client_side, user will search for samples using either "MRN's", "Tumor_Type" or "Dmp ID". Along with search words,
    "search_type (MRN || Tumor Type)" is also passed to this api route. The logic is to call different LIMSRest end points
    based on the search_type parameter to get appropriate data and send as Response to client side.
    :return:
    """

    if request.method == "POST" :
        query_data = request.get_json(silent=True)
        search_keywords = query_data.get('searchtext')
        search_type = query_data.get('searchtype')
        user_role = query_data.get('role')
        username = get_jwt_identity()
        colHeaders , columns , settings = get_column_configs(user_role)
        try:
            if search_keywords is not None and search_type.lower() == "mrn" :
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                result = db.session.query(Sample).filter(Sample.mrn.in_((search_keywords))).all()
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings , ) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.log(
                    AppLog(level="INFO" , process="root" , user=username,
                           message="User {} with role {} searched using kewords {} and searchtype {}".format(username ,
                                                                                                             user_role ,
                                                                                                             search_keywords ,
                                                                                                             search_type)))
                return make_response(response)
            elif search_keywords is not None and search_type.lower() == "tumor type" :
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                search_results = []
                for item in search_keywords :
                    search_word_like = "%{}%".format(item)
                    result = db.session.query(Sample).filter(Sample.tumor_type.like(search_word_like)).all()
                    search_results.append(result)
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.log(
                    AppLog(level="INFO" , process="root" , user=username,
                           message="User {} with role {} searched using kewords {} and searchtype {}".format(username ,
                                                                                                             user_role ,
                                                                                                             search_keywords ,
                                                                                                             search_type)))
                return make_response(response)
            elif search_keywords is not None and search_type.lower() == "dmpid" :
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                result = db.session.query(Sample).filter(Sample.dmp_sampleid.in_((search_keywords))).all()
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.log(
                    AppLog(level="INFO" , process="root" , user=username,
                           message="User {} with role {} searched using kewords {} and searchtype {}".format(username ,
                                                                                                             user_role ,
                                                                                                             search_keywords ,
                                                                                                             search_type)))
                return make_response(response)
            else :
                response = make_response(
                    jsonify(json.dumps(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)) , 200 ,
                            None))
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.log(
                    AppLog(level="INFO" , process="root" , user=username,
                           message="User {} with role {} searched using kewords {} and searchtype {}".format(username ,
                                                                                                             user_role ,
                                                                                                             search_keywords ,
                                                                                                             search_type)))
                return make_response(response)
        except Exception as e:
            response = make_response(
                jsonify(json.dumps(data="Sorry, error occured while searching using {}.".format(search_type)) , 200 ,
                        None))
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(
                AppLog(level="INFO" , process="root" , user=username,
                       message="User {} with role {} searched using kewords {} and searchtype {}, it cuased error {}".format(username ,
                                                                                                         user_role ,
                                                                                                         search_keywords ,
                                                                                                         search_type, e)))
            return make_response(response)

#################################### scheduler to run at interval ####################################
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=get_wes_data, trigger="interval", minutes=15)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())
########################################################################################################

# if __name__ == '__main__':
#     app.run(debug=True)
