
from app import *
from app_tasks.app_tasks import reverse

@app.route("/" , methods=['GET' , 'POST'])
def index() :
    '''
    This method is here only to test at times if the app is working correctly.
    :return:
    '''
    log_entry = LOG.info("testing")
    AppLog.info(message="Testing the app.", user="api")
    #samples = db.session.query(Sample).filter(sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == '')).all()
    #samples = db.session.query(Sample).filter(sa.not_(Sample.sample_status.like('%Failed%'))).all()
    #samples = db.session.query(Sample).all()
    #return jsonify(totalrecords = len(samples))
    return jsonify(columnHeaders=gridconfigs.clinicalColHeaders , columns=gridconfigs.clinicalColumns ,
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
            #user_title = get_user_title(result)
            user_groups = get_user_group(result)
            # check user role
            if len(set(user_groups).intersection(set(ADMIN_GROUPS))) > 0 :
                role = 'admin'
            elif len(set(user_groups).intersection(set(ADMIN_GROUPS))) > 0 and len(set(user_groups).intersection(set(CLINICAL_GROUPS))) > 0 :
                role = 'admin'
            elif len(set(user_groups).intersection(set(CLINICAL_GROUPS))) > 0 :
                role = 'clinical'
            conn.unbind_s()
            LOG.info("Successfully authenticated and logged {} into the app with role {}.".format(username , role))

            AppLog.info(message="Successfully authenticated and logged into the app.", user = username)

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = make_response(
                jsonify(valid=True , username=username , access_token=access_token , refresh_token=refresh_token ,
                        role=role , title="not found" , user_fullname=user_fullname) ,
                200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
        except ldap.INVALID_CREDENTIALS :
            response = make_response(jsonify(valid=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.log(AppLog(level="WARNING" , process="Root" , user=username ,
                              message="Invalid username or password."))
            AppLog.warning(message="Invalid username or password.", user=username)
            return make_response(response)
        except ldap.OPERATIONS_ERROR as e :
            response = make_response(jsonify(valid=False) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.error(message="ldap OPERATION ERROR occured. {}".format(e), user=username )
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
        AppLog.info(message="Successfully refreshed jwt token for user " + current_user, user=current_user)
        return jsonify(response) , 200
    except Exception as e :
        AppLog.error( message="Failed to refresh access token for user " + current_user, user=current_user)
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
            current_user = get_jwt_identity()
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            AppLog.info(message="Successfully logged out user " + current_user, user=current_user)
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
        AppLog.error(message="Error while logging out user " + current_user, user=current_user)
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




def get_tracker_data():
    "hello"
    timestamp = 0


@app.route("/get_wes_data" , methods=['GET'])
def get_wes_data() :
    """
    End point to get WES Sample data from LIMS using timestamp. User can either pass "timestamp" parameter (miliseconds) to this endpoint
    to fetch sample data that was created after the timestamp provided. Or user can call the endpoint without any parameters and the end point will fetch data for last 24 hours.
    :return:

    """
    try :
        if request.args.get("timestamp") is not None :
            timestamp = request.args.get("timestamp")
            LOG.info("Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query")
            AppLog.info(
                message="Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query" ,
                user='api' , )
        else :
            timestamp = time.mktime((datetime.datetime.today() - timedelta(
                days=1.1)).timetuple()) * 1000  # 1.1 to account for time lost during the initialization of query. It is better to have some time overlap to get all the data.
            LOG.info("Starting WES Sample query after calculating time: {} provided to the endpoint by user.".format(
                str(timestamp)))
            AppLog.info(
                message="Starting WES Sample query after calculating time: {} provided to the endpoint by user.".format(
                    str(timestamp)) , user="api")
        if int(timestamp) > 0 :
            print(timestamp)
            LOG.info(
                "Starting query : " + LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)))
            r = s.get(LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)) ,
                      auth=(USER , PASSW) , verify=False)
            data = r.content.decode("utf-8" , "strict")
            ids = save_to_db(data)
            LOG.info("Added {0} new records to the Sample Tracking Database".format(ids))
            AppLog.info(message="Added {0} new records to the Sample Tracking Database".format(ids), user="api")
            response = make_response(jsonify(data=(str(ids))) , 200 , None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e :
        AppLog.error(message=repr(e), user='api')
        LOG.error(e , exc_info=True)
        response = make_response(jsonify(data="" , error="There was a problem processing the request.") , 200 , None)
        response.headers.add('Access-Control-Allow-Origin', '*')
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
            partial_existing = None
            existing = None
            if item.get("limsSampleRecordId") is None and item.get("limsTrackerRecordId") is not None :
                ''' check if the record already exists and is non IGO processed Sample. If a sample was not processed by IGO, 
                                                    it should only have "limsTrackerRecordId" value. '''
                print("running partial existing block")
                partial_existing = Sample.query.filter(sa.and_(Sample.lims_sample_recordid == '', Sample.lims_tracker_recordid==item.get("limsTrackerRecordId"))).first()

                '''If a non IGO sample exists, this means that the sample values have changed in DMP tracker and LIMS since last build of DB, then update the values on existing record.'''
                if partial_existing :
                    api_update_sample(db , item);


            elif item.get("limsSampleRecordId") is not None and item.get("limsTrackerRecordId") is not None :
                ''' check if the record already exists and is IGO processed Sample. If a sample was processed by IGO, 
                                it should have both "limsSampleRecordId" and "limsTrackerRecordId" values. '''

                existing = Sample.query.filter(sa.and_(Sample.lims_sample_recordid==item.get("limsSampleRecordId") ,
                                                  Sample.lims_tracker_recordid==item.get("limsTrackerRecordId"))).first()
                if existing:
                    print("running existing block")
                    api_update_sample(db , item)

            '''If the record does not exist, create a new record.'''
            if partial_existing is None and existing is None:
                print ("running not existing block")
                sample = Sample(sampleid=item.get("sampleId") , user_sampleid=item.get("userSampleId") ,
                                user_sampleid_historical= item.get("userSampleidHistorical"),
                                duplicate_sample= item.get("duplicateSample"),
                                wes_sampleid=item.get("wesSampleid") ,
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
                                scientific_pi=item.get("labHead") ,
                                consent_parta_status=item.get("consentPartAStatus") ,
                                consent_partc_status=item.get("consentPartCStatus") ,
                                sample_status=item.get("sampleStatus") ,
                                access_level="MSK public" , clinical_trial=item.get("clinicalTrial") ,
                                seqiencing_site=item.get("sequencingSite") , pi_request_date=item.get("piRequestDate") ,
                                pipeline=item.get("pipeline") , tissue_type=item.get("tissueType") ,
                                collaboration_center=item.get("collaborationCenter") ,
                                lims_sample_recordid=item.get("limsSampleRecordId") ,
                                lims_tracker_recordid=item.get("limsTrackerRecordId"),
                                date_created = str(datetime.datetime.now()),
                                created_by = 'api',
                                date_updated = str(datetime.datetime.now()),
                                )
                db.session.add(sample)
                db.session.commit()
                db.session.flush()
                record_ids.append(item.get("limsTrackerRecordId"))
        AppLog.info(message="Added {} new records to the Sample Tracking Database".format(len(record_ids)), user="api")
        return len(record_ids)
    except Exception as e :
        AppLog.error(message="{} Error occured while adding records to the Sample Tracking Database.\n{}".format(e), user="api")
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
        if item.get("limsSampleRecordId") is not None and item.get("limsTrackerRecordId") is not None :
            sample = db.session.query(Sample).filter(sa.and_(Sample.lims_sample_recordid == item.get("limsSampleRecordId") ,
                                                        Sample.lims_tracker_recordid == item.get("limsTrackerRecordId"))).first()
            print("updating sample with both record ids")
        elif item.get("limsSampleRecordId") is None and item.get("limsTrackerRecordId") is not None :
            print(item.get("sampleId"))
            sample = db.session.query(Sample).filter(sa.and_(Sample.lims_sample_recordid == item.get("limsSampleRecordId"), Sample.lims_tracker_recordid == item.get("limsTrackerRecordId"))).first()
            print("updating sample with no sample record id")

        if sample is not None :
            #sample = db.session.query(Sample).filter(lims_tracker_recordid=item.get("limsTrackerRecordId")).first()
            sample.sampleid = item.get("sampleId")
            sample.user_sampleid = item.get("userSampleId")
            sample.user_sampleid_historical = item.get("userSampleidHistorical")
            sample.duplicate_sample = item.get("duplicateSample")
            sample.wes_sampleid = item.get("wesSampleid")
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
            if sample.scientific_pi is None:
                sample.scientific_pi = item.get("labHead")
            sample.cc_fund = item.get("ccFund")
            sample.consent_parta_status = item.get("consentPartAStatus")
            sample.consent_partc_status = item.get("consentPartCStatus")
            sample.sample_status = item.get("sampleStatus")
            if sample.access_level is None:
                sample.access_level="MSK public"
            if item.get("limsSampleRecordId") is not None and sample.lims_sample_recordid is None :
                sample.lims_sample_recordid = item.get("limsSampleRecordId")
            sample.date_updated = str(datetime.datetime.now())
            sample.updated_by = 'api'
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
            username = get_jwt_identity()
            for item in sample_data :
                user_update_sample(db.session , item, username)
            AppLog.info(message="updated {} samples by user".format(len(sample_data)), user=username)
            LOG.info("update {} samples by user {}".format(len(sample_data), username))
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
        AppLog.error(message="error while updating the samples {}".format(e.with_traceback()), user="api")
        response = make_response(
            jsonify(success=False ,
                    message="Save operation failed. Plese try again later." ,
                    ) ,
            200 , None)
        response.headers.add('Access-Control-Allow-Origin' , '*')
        return response


def user_update_sample(session , item, username) :
    '''
    Sometimes users will update some editable columns on the clientside. These updated values should be updated to the database.
    Only the fields that are editable on the front end will be updated.
    :param session:
    :param item:
    :return:
    '''
    print(username)
    try :
        sample = session.query(Sample).filter_by(id=item.get("id")).first()
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
            sample.date_updated = str(datetime.datetime.now())
            sample.updated_by = username
            session.commit()
            session.flush()

    except Exception as e :
        LOG.error(e , exc_info=True)
        AppLog.error(message=e, user="api")


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
            AppLog.info(message="User {} with role {} downloaded data for {} samples".format(username , role , num_samples), user=username)
            response = make_response(jsonify(
                success=True ), 200 , None)
            response.headers.add('Access-Control-Allow-Origin' , '*')
            return response
        except Exception as e :
            AppLog.error(message="Error occured while logging the data download event\n{}".format(e), user=username)
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
        exact_match = query_data.get('exactmatch')
        username = get_jwt_identity()
        colHeaders , columns , settings = get_column_configs(user_role)
        try:
            result = None
            if search_keywords is not None and search_keywords == "*":
                if user_role != 'admin':
                    result = db.session.query(Sample).filter(sa.and_(sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == ''))).all()
                else:
                    result = db.session.query(Sample).all()
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                     separators=(',', ': '))), colHeaders=colHeaders, columns=columns,
                    settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using wildcard {}".format(username, user_role, search_keywords), user=username)
                return response

            elif search_keywords is not None and search_type.lower() == "mrn":
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                if user_role != 'admin':
                    result = db.session.query(Sample).filter(sa.and_(Sample.mrn.in_((search_keywords)), sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == ''))).all()
                else:
                    result = db.session.query(Sample).filter(Sample.mrn.in_((search_keywords))).all()
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings , ) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username ,user_role ,search_keywords ,search_type), user=username)
                return response
            elif search_keywords is not None and search_type.lower() == "tumor type" and exact_match:
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                search_results = []
                if user_role != 'admin':
                    result = db.session.query(Sample).filter(sa.and_(Sample.tumor_type.in_((search_keywords)), sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == ''))).all()
                else:
                    result = db.session.query(Sample).filter(Sample.tumor_type.in_(search_keywords)).all()
                search_results.extend(result)
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in search_results], default=alchemy_encoder, sort_keys=True, indent=4,
                                     separators=(',', ': '))), colHeaders=colHeaders, columns=columns,
                    settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username, user_role, search_keywords, search_type), user=username)
                return response
            elif search_keywords is not None and search_type.lower() == "tumor type" and not exact_match:
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                search_results = list()
                for item in search_keywords :
                    search_word_like = "%{}%".format(item)
                    print(search_word_like)
                    if user_role != 'admin' :
                        result = db.session.query(Sample).filter(Sample.tumor_type.like(search_word_like), sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == '')).all()
                    else:
                        result = db.session.query(Sample).filter(Sample.tumor_type.like(search_word_like)).all()
                    search_results.extend(result)
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in search_results] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username , user_role, search_keywords, search_type), user=username)
                return response
            elif search_keywords is not None and search_type.lower() == "dmpid" :
                search_keywords = [x.strip() for x in search_keywords.split(',')]
                if user_role != 'admin' :
                    result = db.session.query(Sample).filter(Sample.dmp_sampleid.in_(search_keywords), sa.not_(Sample.sample_status.like('%Failed%')), sa.not_(Sample.sampleid == '')).all()
                else :
                    result = db.session.query(Sample).filter(Sample.dmp_sampleid.in_((search_keywords))).all()
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result] , default=alchemy_encoder , sort_keys=True , indent=4 ,
                                     separators=(',' , ': '))) , colHeaders=colHeaders , columns=columns ,
                    settings=settings) , 200 , None)
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username, user_role, search_keywords, search_type), user=username)
                return response
            else :
                response = make_response(
                    jsonify(json.dumps(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)) , 200 ,
                            None))
                response.headers.add('Access-Control-Allow-Origin' , '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username, user_role, search_keywords ,search_type), user=username)
                return response
        except Exception as e:
            response = make_response(
                jsonify(json.dumps(data="Sorry, error occured while searching using {}.".format(search_type)) , 200 ,
                        None))
            response.headers.add('Access-Control-Allow-Origin' , '*')
            AppLog.error(message="User {} with role {} searched using kewords {} and searchtype {}, it cuased error {}".format(username , user_role , search_keywords , search_type, e), user=username)
            return response




@app.route("/get_reverse/<name>")
def get_reverse(name):
    result = reverse.delay(name)
    result.wait()
    print(result.get())
    response = make_response(jsonify(data=result.get()))
    response.headers.add('Access-Control-Allow-Origin' , '*')
    return response



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
