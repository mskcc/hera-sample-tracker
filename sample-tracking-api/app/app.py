import re
import traceback

from app import *
from database.models import get_sample_objects


@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    This method is here only to test at times if the app is working correctly.
    :return:
    '''
    log_entry = LOG.info("testing")
    AppLog.info(message="Testing the app.", user="api")
    LOG.info("Index route for testing. Returns grid column headers and settings.")
    return jsonify(columnHeaders=gridconfigs.clinicalColHeaders, columns=gridconfigs.clinicalColumns,
                   settings=gridconfigs.settings), 200


def get_ldap_connection():
    conn = ldap.initialize(AUTH_LDAP_URL)
    conn.protocol_version = ldap.VERSION3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    return conn


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    Login user using ldap connection and validate user role.
    :return:
    '''
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
                'sAMAccountName=' + username,
                attrs,
            )
            role = 'user'

            user_fullname = ''  # get_user_fullname(result)
            # user_title = get_user_title(result)
            user_groups = get_user_group(result)
            # check user role
            if len(set(user_groups).intersection(set(ADMIN_GROUPS))) > 0:
                role = 'admin'
            elif len(set(user_groups).intersection(set(CLINICAL_GROUPS))) > 0:
                role = 'clinical'
            else:
                role = 'user'
            conn.unbind_s()
            LOG.info("Successfully authenticated and logged {} into the app with role {}.".format(username, role))

            AppLog.info(message="Successfully authenticated and logged into the app.", user=username)

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            response = make_response(
                jsonify(valid=True, username=username, access_token=access_token, refresh_token=refresh_token,
                        role=role, title="not found", user_fullname=user_fullname),
                200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except ldap.INVALID_CREDENTIALS:
            response = make_response(jsonify(valid=False), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            AppLog.warning(message="Invalid username or password.", user=username)
            LOG.warning("Invalid username '{}' or password.".format(username))
            return make_response(response)
        except ldap.OPERATIONS_ERROR as e:
            response = make_response(jsonify(valid=False), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            AppLog.error(message="ldap OPERATION ERROR occured. {}".format(e), user=username)
            LOG.error("ldap OPERATION ERROR occured. {}".format(traceback.print_exc()))
            return make_response(response)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''
    Add JWT token to blacklist.
    :param decrypted_token:
    :return:
    '''
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    try:
        if request.method == "POST":
            # user_data = request.get_json(silent=True)
            current_user = get_jwt_identity()
            jti = get_raw_jwt()['jti']
            blacklist.add(jti)
            AppLog.info(message="Successfully logged out user " + current_user, user=current_user)
            LOG.info("Successfully logged out user {}".format(current_user))
            response = make_response(
                jsonify(success=True,
                        valid=True,
                        username=None,
                        access_token=None,
                        refresh_token=None,
                        message="Successfully logged out user " + current_user),
                200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e:
        AppLog.error(message="Error while logging out user " + current_user, user=current_user)
        LOG.error("Error while logging out user {}. {}".format(current_user, traceback.print_exc()))
        response = make_response(
            jsonify(valid=False,
                    username=None,
                    access_token=None,
                    refresh_token=None,
                    message="Error while logging out user " + current_user,
                    error=repr(e)),
            200, None)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route("/get_wes_data", methods=['GET'])
def get_wes_data():
    """
    End point to get WES Sample data from LIMS using timestamp. User can either pass "timestamp" parameter (miliseconds) to this endpoint
    to fetch sample data that was created after the timestamp provided. Or user can call the endpoint without any parameters and the end point will fetch data for last 24 hours.
    :return:

    """
    try:
        if request.args.get("timestamp") is not None:
            timestamp = request.args.get("timestamp")
            LOG.info("Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query")
            AppLog.info(
                message="Starting WES Sample query using time stamp: " + timestamp + ", provided to the endpoint query",
                user='api', )
        else:
            timestamp = time.mktime((datetime.datetime.today() - timedelta(
                days=1.1)).timetuple()) * 1000  # 1.1 to account for time lost during the initialization of query. It is better to have some time overlap to get all the data.
            LOG.info("Starting WES Sample query after calculating time: {} provided to the endpoint by user.".format(
                str(timestamp)))
            AppLog.info(
                message="Starting WES Sample query after calculating time: {} provided to the endpoint by user.".format(
                    str(timestamp)), user="api")
        if int(timestamp) > 0:
            print(timestamp)
            LOG.info(
                "Starting query : " + LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)))
            r = s.get(LIMS_API_ROOT + "/LimsRest/getWESSampleData?timestamp=" + str(int(timestamp)),
                      auth=(USER, PASSW), verify=False)
            data = r.content.decode("utf-8", "strict")
            ids = save_to_db(data)
            LOG.info("Added {} new records to the Sample Tracking Database".format(ids))
            AppLog.info(message="Added {} new records to the Sample Tracking Database".format(ids), user="api")
            response = make_response(jsonify(data=(len(ids))), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e:
        AppLog.error(message=repr(e), user='api')
        LOG.error(e, exc_info=True)
        response = make_response(jsonify(data="", error="There was a problem processing the request."), 200, None)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


def save_to_db(data):
    try:
        data_to_json = json.loads(data)
        new_record_ids = []
        for item in data_to_json:
            AppLog.info(message="Processing Sample with User Sample ID: {}".format(item.get("userSampleId")),
                        user="api")
            dmp_recordid = item.get('limsTrackerRecordId')
            tracker_record = Dmpdata.query.filter_by(lims_tracker_recordid=dmp_recordid).first()
            if tracker_record is None:
                AppLog.info(
                    message="Creating new  DmpData record with User Sample ID: {}".format(item.get("userSampleId")),
                    user="api")
                new_dmpdata_record = Dmpdata(
                    user_sampleid_historical=item.get('userSampleidHistorical'),
                    user_sampleid=item.get('userSampleId'),
                    duplicate_sample=item.get('duplicateSample'),
                    wes_sampleid=item.get('wesSampleid'),
                    source_dna_type=item.get('sourceDnaType'),
                    date_dmp_request=item.get('dateDmpRequest'),
                    dmp_requestid=item.get('dmpRequestId'),
                    project_title=item.get('projectTitle'),
                    data_analyst='',
                    data_custodian=item.get("dataCustodian"),
                    cc_fund=item.get('ccFund'),
                    scientific_pi=item.get('scientificPi'),
                    access_level="MSK Embargo",
                    seqiencing_site=item.get('sequencingSite'),
                    pi_request_date=item.get('piRequestDate'),
                    tempo_qc_status='NOT RUN',
                    pm_redaction='',
                    tempo_output_delivery_date=item.get("tempoOutputDeliveryDate",''),
                    embargo_end_date=calculate_outdate(item.get("tempoOutputDeliveryDate",'')),
                    tempo_analysis_update='',
                    tissue_type=item.get('tissueType'),
                    date_created=str(datetime.datetime.now()),
                    created_by='api',
                    date_updated=str(datetime.datetime.now()),
                    updated_by='api',
                    lims_tracker_recordid=item.get('limsTrackerRecordId'),
                )
                db.session.add(new_dmpdata_record)
                db.session.commit()
                new_record_ids.append(new_dmpdata_record.id)
                AppLog.info(
                    message="Added new Dmpdata record with ID: {}".format(
                        new_dmpdata_record.id),
                    user="api")
                new_cvrdata_record = Cvrdata(
                    dmp_sampleid=item.get('dmpSampleId'),
                    dmp_patientid=item.get('dmpPatientId'),
                    mrn=item.get('mrn'),
                    sex=item.get('sex'),
                    sample_class=item.get('sampleClass'),
                    tumor_type=item.get('tumorType'),
                    tumor_site=item.get('tissueSite'),
                    molecular_accession_num=item.get('molecularAccessionNum'),
                    consent_parta_status=item.get('consentPartAStatus'),
                    consent_partc_status=item.get('consentPartCStatus'),
                    date_created=str(datetime.datetime.now()),
                    created_by='api',
                    date_updated=str(datetime.datetime.now()),
                    updated_by='api',
                    dmpdata=new_dmpdata_record
                )
                db.session.add(new_cvrdata_record)
                db.session.commit()
                AppLog.info(
                    message="Added new Cvrdata record with ID: {}".format(
                        new_cvrdata_record.id),
                    user="api")

                # if item.get('limsSampleRecordId') != '':
                new_sample_record = Sample(
                    sampleid=item.get('sampleId'),
                    alt_id=item.get("altId"),
                    cmo_sampleid=item.get("cmoSampleId",""),
                    cmo_patientid=item.get("cmoPatientId",""),
                    parental_tumortype=item.get('parentalTumorType'),
                    collection_year=item.get('collectionYear'),
                    igo_requestid=item.get('igoRequestId'),
                    date_igo_received=item.get('dateIgoReceived'),
                    date_igo_complete=item.get('igoCompleteDate'),
                    application_requested=item.get('applicationRequested'),
                    baitset_used=item.get('baitsetUsed'),
                    sequencer_type=item.get('sequencerType'),
                    lab_head=item.get('labHead'),
                    sample_status=item.get('sampleStatus'),
                    date_created=str(datetime.datetime.now()),
                    created_by='api',
                    date_updated=str(datetime.datetime.now()),
                    updated_by='api',
                    lims_sample_recordid=item.get('limsSampleRecordId'),
                    dmpdata=new_dmpdata_record
                )
                db.session.add(new_sample_record)
                db.session.commit()
                AppLog.info(
                    message="Added new Sample record with  ID: {}".format(new_sample_record.id),
                    user="api")
            elif tracker_record is not None:
                update_record(tracker_record, item)
        return new_record_ids
    except Exception as e:
        AppLog.error(message=repr(e), user='api')
        LOG.error(e, exc_info=True)


def update_record(record, item):
    try:
        record.user_sampleid_historical = item.get('userSampleidHistorical')
        record.user_sampleid = item.get('userSampleId')
        record.duplicate_sample = item.get('duplicateSample')
        record.wes_sampleid = item.get('wesSampleid')
        record.date_dmp_request = item.get('dateDmpRequest')
        record.dmp_requestid = item.get('dmpRequestId')
        record.project_title = item.get('projectTitle')
        record.cc_fund = item.get('ccFund')
        record.pi_request_date = item.get('piRequestDate')
        record.tissue_type = item.get('tissueType')
        record.scientific_pi = item.get('scientificPi')
        record.source_dna_type = item.get('sourceDnaType')
        record.data_custodian = item.get("dataCustodian")
        record.tempo_output_delivery_date = item.get("tempoOutputDeliveryDate")
        record.embargo_end_date = calculate_outdate(record.tempo_output_delivery_date)
        record.date_updated = str(datetime.datetime.now())
        record.updated_by = 'api'
        db.session.commit()
        AppLog.info(
            message="Update Dmpdata record with ID: {}".format(
                record.id),
            user="api")
        '''find and update the cvrdata record. An existing Dmpdata record must always have related Cvrdata record'''
        cvrdata = Cvrdata.query.filter_by(lims_tracker_recordid=item.get('limsTrackerRecordId')).first()
        if cvrdata is not None:
            cvrdata.dmp_sampleid = item.get('dmpSampleId')
            cvrdata.dmp_patientid = item.get('dmpPatientId')
            cvrdata.mrn = item.get('mrn')
            cvrdata.sex = item.get('sex')
            cvrdata.sample_class = item.get('sampleClass')
            cvrdata.tumor_type = item.get('tumorType')
            cvrdata.tumor_site = item.get('tissueSite')
            cvrdata.molecular_accession_num = item.get('molecularAccessionNum')
            cvrdata.consent_parta_status = item.get('consentPartAStatus')
            cvrdata.consent_partc_status = item.get('consentPartCStatus')
            cvrdata.date_updated = str(datetime.datetime.now())
            cvrdata.updated_by = 'api'
            db.session.commit()
            AppLog.info(
                message="Updated Cvrdata record with ID: {}".format(
                    cvrdata.id),
                user="api")
        '''find if the record has related sample record, if found, update it, if not found then add sample record'''
        sampledata = Sample.query.filter_by(lims_sample_recordid=item.get('limsSampleRecordId'), lims_tracker_recordid=item.get('limsTrackerRecordId')).first()
        if sampledata is not None:
            sampledata.sampleid = item.get('sampleId')
            sampledata.alt_id = item.get('altId')
            cmo_sampleid = item.get('cmoSampleId',None)
            cmo_patientid = item.get('cmoPatientId',None)
            sampledata.cmo_sampleid = cmo_sampleid if cmo_sampleid else sampledata.get("cmo_sampleid","")
            sampledata.cmo_patientid = cmo_patientid if cmo_patientid else sampledata.get("cmo_patientid","")
            sampledata.parental_tumortype = item.get('parentalTumorType')
            sampledata.collection_year = item.get('collectionYear')
            sampledata.igo_requestid = item.get('igoRequestId')
            sampledata.date_igo_received = item.get('dateIgoReceived')
            sampledata.date_igo_complete = item.get('igoCompleteDate')
            sampledata.application_requested = item.get('applicationRequested')
            sampledata.sequencer_type = item.get('sequencerType')
            sampledata.lab_head = item.get('labHead')
            sampledata.sample_status = item.get('sampleStatus')
            sampledata.date_updated = str(datetime.datetime.now())
            # update baitset only if sample is IGO sample and sequenced at IGO. IGO samples will have a
            # 'limsSampleRecordId' value in the endpoint data. If the sample was Sequenced at IGO it will also have
            # status of "Failed - Illumina Sequencing Analysis" or "Data QC - Completed".
            if item.get('limsSampleRecordId') and item.get('baitsetUsed'):
                sampledata.baitset_used = item.get('baitsetUsed')
            sampledata.updated_by = 'api'
            db.session.commit()
        elif sampledata is None:
            new_sample_record = Sample(
                sampleid=item.get('sampleId'),
                alt_id=item.get("altId"),
                parental_tumortype=item.get('parentalTumorType'),
                collection_year=item.get('collectionYear'),
                igo_requestid=item.get('igoRequestId'),
                date_igo_received=item.get('dateIgoReceived'),
                date_igo_complete=item.get('igoCompleteDate'),
                application_requested=item.get('applicationRequested'),
                baitset_used=item.get('baitsetUsed'),
                sequencer_type=item.get('sequencerType'),
                lab_head=item.get('labHead'),
                sample_status=item.get('sampleStatus'),
                date_created=str(datetime.datetime.now()),
                created_by='api',
                date_updated=str(datetime.datetime.now()),
                updated_by='api',
                lims_sample_recordid=item.get('limsSampleRecordId'),
                dmpdata=record
            )
            db.session.add(new_sample_record)
            db.session.commit()
            AppLog.info(
                message="Added new Sample record with  ID: {}".format(new_sample_record.id),
                user="api")

    except Exception as e:
        AppLog.error(message=repr(e), user='api')
        LOG.error(traceback.print_exc())


def user_update_sample(item, username):
    '''
    user updates are meant for Dmpdata record. Get the Dmpdatarecord using the id
    :param username:
    :param item:
    :return:
    '''
    try:
        dmpdata = db.session.query(Dmpdata).filter_by(id=item.get("id")).first()
        if dmpdata is not None:
            dmpdata.data_analyst = item.get("data_analyst")
            dmpdata.scientific_pi = item.get("scientific_pi")
            dmpdata.access_level = item.get("access_level")
            dmpdata.clinical_trial = item.get("clinical_trial")
            dmpdata.seqiencing_site = item.get("seqiencing_site")
            dmpdata.pi_request_date = item.get("pi_request_date")
            dmpdata.tissue_type = item.get("tissue_type")
            dmpdata.tempo_qc_status = item.get("tempo_qc_status")
            dmpdata.pm_redaction = item.get("pm_redaction")
            dmpdata.tempo_analysis_update = item.get("tempo_analysis_update")
            dmpdata.date_updated = str(datetime.datetime.now())
            dmpdata.updated_by = username
            db.session.commit()
            AppLog.info(message="Updated DmpData record with ID: {}".format(dmpdata.id), user=username)
            if dmpdata.samples is not None:
                for sample in dmpdata.samples:
                    sample.baitset_used = item.get("baitset_used")
                    AppLog.info(message="Updated Sample record with ID: {}".format(sample.id), user=username)
            db.session.commit()
            AppLog.info(message="Updated DmpData record with ID: {}".format(dmpdata.id), user=username)
    except Exception as e:
        LOG.error(traceback.print_exc())
        AppLog.error(message=e, user="api")


@app.route("/save_sample_changes", methods=['POST'])
@jwt_required
def save_sample_changes():
    '''
    Method to save samples when users call the save method from frontend app via button click events.
    :return: response
    '''
    try:
        if request.method == "POST":
            sample_data = request.get_json(silent=True)
            username = get_jwt_identity()
            for item in sample_data:
                user_update_sample(item, username)
            AppLog.info(message="Updated {} samples by user".format(len(sample_data)), user=username)
            response = make_response(
                jsonify(
                    success=True,
                    message="Data updated successfully.",
                ),
                200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as e:
        LOG.error(traceback.print_exc())
        AppLog.error(message="error while updating the samples {}".format(e.with_traceback()), user="api")
        response = make_response(
            jsonify(success=False,
                    message="Save operation failed. Plese try again later.",
                    ),
            200, None)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def get_column_configs(role):
    '''
    Method to return column configurations based on user role. Not all users are authorized to see all the data returned by this server.
    :param role:
    :return: column configurations
    '''
    if role == 'clinical':
        return gridconfigs.clinicalColHeaders, gridconfigs.clinicalColumns, gridconfigs.settings
    elif role == 'admin':
        return gridconfigs.adminColHeaders, gridconfigs.adminColumns, gridconfigs.settings
    elif role == 'user':
        return gridconfigs.nonClinicalColHeaders, gridconfigs.nonClinicalColumns, gridconfigs.settings

def calculate_outdate(indate,delta=547):
    # Add 1.5 yr to tempo output delivery date. 
    outdate = ""
    try:
        indate_p = datetime.datetime.strptime(indate,"%m-%d-%Y")
        outdate_p = indate_p + datetime.timedelta(days=delta)
        outdate = outdate_p.strftime("%m-%d-%Y")
    except Exception as e:
        print(e)
    finally:
        return outdate


@app.route("/download_data", methods=['POST'])
@jwt_required
def download_data():
    '''
    Method to log the download data event from the forntend.
    :return:
    '''
    if request.method == "POST":
        query_data = request.get_json(silent=True)
        num_samples = query_data.get('data_length')
        user = query_data.get('user')
        username = user.get('username')
        role = user.get('role')
        try:
            AppLog.info(
                message="User {} with role {} downloaded data for {} samples".format(username, role, num_samples),
                user=username)
            response = make_response(jsonify(
                success=True), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            AppLog.error(message="Error occured while logging the data download event\n{}".format(e), user=username)
            LOG.error("Error occured while logging the data download event\n{}".format(traceback.print_exc()))
            response = make_response(jsonify(
                success=False), 200, None)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


@app.route("/search_data", methods=['POST'])
@jwt_required
def search_data():
    """
    From the client_side, user will search for samples using either "MRN's", "Tumor_Type" or "Dmp ID". Along with search words,
    "search_type (MRN || Tumor Type)" is also passed to this api route. The logic is to call different LIMSRest end points
    based on the search_type parameter to get appropriate data and send as Response to client side.
    :return:
    """
    if request.method == "POST":
        query_data = request.get_json(silent=True)
        search_keywords = query_data.get('searchtext')
        search_type = query_data.get('searchtype')
        user_role = query_data.get('role')
        print("logged in user role: ", user_role)
        exact_match = query_data.get('exactmatch')
        username = get_jwt_identity()
        col_headers, columns, settings = get_column_configs(user_role)
        try:
            result = None
            if search_keywords is not None and search_keywords == "*":
                if 'admin' != user_role:
                    print("non admin search")
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(~Sample.sample_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.in_(["NOT RUN",""]), Dmpdata.pm_redaction == "").all()
                    result = get_sample_objects(db_data, filter_failed=True)
                    print("total unfiltered", len(db_data))
                    print("total results: ", len(result))
                else:
                    print("admin search")
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid).all()
                    result = get_sample_objects(db_data, filter_failed=False)
                    print("total unfiltered", len(db_data))
                    print("total results: ", len(result))

                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                     separators=(',', ': '))), colHeaders=col_headers, columns=columns,
                    settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} made wildcard query using search keywords {}".format(username,
                                                                                                               user_role,
                                                                                                               search_keywords),
                            user=username)
                LOG.info("User {} with role {} made wildcard query using search keywords {}".format(username,
                                                                                                    user_role,
                                                                                                    search_keywords))
                return response

            elif search_keywords is not None and search_type.lower() == "mrn":
                search_keywords = [x.strip() for x in re.split(r'[,\s\n]\s*', search_keywords)]
                if 'admin' != user_role:
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.mrn.in_(search_keywords), ~Sample.sample_status.like('%Failed%'),
                                Sample.sampleid != '', ~Dmpdata.tempo_qc_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.in_(["NOT RUN",""]), Dmpdata.pm_redaction == "").all()
                    result = get_sample_objects(db_data, filter_failed=True)
                    print("total results: ", len(result))
                else:
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.mrn.in_(search_keywords)).all()
                    result = get_sample_objects(db_data, filter_failed=False)
                    print("total results: ", len(result))
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                     separators=(',', ': '))), colHeaders=col_headers, columns=columns,
                    settings=settings, ), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                              user_role,
                                                                                                              search_keywords,
                                                                                                              search_type),
                            user=username)
                LOG.info("User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                   user_role,
                                                                                                   search_keywords,
                                                                                                   search_type))
                return response
            elif search_keywords is not None and search_type.lower() == "tumor type" and exact_match:
                search_keywords = [x.strip() for x in re.split(r'[,\n]', search_keywords)]
                print(search_keywords)
                if 'admin' != user_role:
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.tumor_type.in_(search_keywords), ~Sample.sample_status.like('%Failed%'),
                                Sample.sampleid != '', ~Dmpdata.tempo_qc_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.in_(["NOT RUN",""]), Dmpdata.pm_redaction == "").all()
                    result = get_sample_objects(db_data, filter_failed=True)
                    print("total results: ", len(result))
                else:
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.tumor_type.in_(search_keywords)).all()
                    result = get_sample_objects(db_data, filter_failed=False)
                    print("total results: ", len(result))
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True,
                                     indent=4,
                                     separators=(',', ': '))), colHeaders=col_headers, columns=columns,
                    settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                              user_role,
                                                                                                              search_keywords,
                                                                                                              search_type),
                            user=username)
                LOG.info("User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                   user_role,
                                                                                                   search_keywords,
                                                                                                   search_type))
                return response
            elif search_keywords is not None and search_type.lower() == "tumor type" and not exact_match:
                search_keywords = [x.strip() for x in re.split(r'[,\n]', search_keywords)]
                for item in search_keywords:
                    search_word_like = "%{}%".format(item)
                    print(search_word_like)
                    if user_role != 'admin':
                        db_data = db.session.query(Dmpdata) \
                            .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                            .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                            .filter(Cvrdata.tumor_type.like(search_word_like), ~Sample.sample_status.like('%Failed%'),
                                    Sample.sampleid != '', ~Dmpdata.tempo_qc_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.in_(["NOT RUN",""]), Dmpdata.pm_redaction == "").all()
                        result = get_sample_objects(db_data, filter_failed=True)
                        print("total results: ", len(result))
                    else:
                        db_data = db.session.query(Dmpdata) \
                            .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                            .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                            .filter(Cvrdata.tumor_type.like(search_word_like)).all()
                        result = get_sample_objects(db_data, filter_failed=False)
                        print("total results: ", len(result))
                response = make_response(
                    jsonify(
                        data=(json.dumps([r.__dict__ for r in result],
                                         default=alchemy_encoder, sort_keys=True,
                                         indent=4,
                                         separators=(',', ': '))),
                        colHeaders=col_headers,
                        columns=columns,
                        settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                              user_role,
                                                                                                              search_keywords,
                                                                                                              search_type),
                            user=username)
                LOG.info("User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                   user_role,
                                                                                                   search_keywords,
                                                                                                   search_type))
                return response
            elif search_keywords is not None and search_type.lower() == "dmpid":
                search_keywords = [x.strip() for x in re.split(r'[,\s\n]\s*', search_keywords)]
                if user_role != 'admin':
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.dmp_sampleid.in_(search_keywords), ~Sample.sample_status.like('%Failed%'),
                                Sample.sampleid != '', ~Dmpdata.tempo_qc_status.like('%Fail%'), ~Dmpdata.tempo_qc_status.in_(["NOT RUN",""]), Dmpdata.pm_redaction == "").all()
                    result = get_sample_objects(db_data, filter_failed=True)
                    print("total results: ", len(result))
                else:
                    db_data = db.session.query(Dmpdata) \
                        .outerjoin(Cvrdata, Cvrdata.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .outerjoin(Sample, Sample.lims_tracker_recordid == Dmpdata.lims_tracker_recordid) \
                        .filter(Cvrdata.dmp_sampleid.in_(search_keywords)).all()
                    result = get_sample_objects(db_data, filter_failed=False)
                    print("total results: ", len(result))
                response = make_response(jsonify(
                    data=(json.dumps([r.__dict__ for r in result], default=alchemy_encoder, sort_keys=True, indent=4,
                                     separators=(',', ': '))), colHeaders=col_headers, columns=columns,
                    settings=settings), 200, None)
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                              user_role,
                                                                                                              search_keywords,
                                                                                                              search_type),
                            user=username)
                LOG.info("User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                   user_role,
                                                                                                   search_keywords,
                                                                                                   search_type))
                return response
            else:
                response = make_response(
                    jsonify(json.dumps(data="Sorry, 'Search Type' '{}' is not supported.".format(search_type)), 200,
                            None))
                response.headers.add('Access-Control-Allow-Origin', '*')
                AppLog.info(message="User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                              user_role,
                                                                                                              search_keywords,
                                                                                                              search_type),
                            user=username)
                LOG.info("User {} with role {} searched using kewords {} and searchtype {}".format(username,
                                                                                                   user_role,
                                                                                                   search_keywords,
                                                                                                   search_type))
                return response
        except Exception as e:
            response = make_response(
                jsonify(json.dumps(data="Sorry, error occured while searching using {}.".format(search_type)), 200,
                        None))
            response.headers.add('Access-Control-Allow-Origin', '*')
            AppLog.error(
                message="User {} with role {} searched using kewords {} and searchtype {}, it cuased error {}. Check logs for details.".format(
                    username, user_role, search_keywords, search_type, e), user=username)
            LOG.error(traceback.print_exc())
            return response


@app.route("/update_tempo_status", methods=['POST'])
def update_tempo_status():
    """
    Endpoint to update tempo status on the Dmpdata object related to Sample. Find Sample using cmo_id and igo_id passed
    by the request. If matching Sample is found, find related Dmpdata and update tempo_qc_status value to tempo_status
    passed by request.
    @param cmo_id : cmo_id for the sample to update. It is required.
    @param igo_id : igo_id for the ample to update. It is required.
    @param tempo_status: status to update to
    """
    if request.method == "POST":
        parms = request.get_json(force=True)
        print("Tempo status update parameters: ", parms)
        cmo_id = parms.get('cmo_id')
        igo_id = parms.get('igo_id')
        tempo_status = parms.get('tempo_status')
        try:
            if cmo_id and igo_id and tempo_status:
                db_data = db.session.query(Sample).filter(Sample.sampleid == igo_id, Sample.cmo_sampleid==cmo_id).all()
                LOG.info(msg="found {} records to update tempo status".format(len(db_data)))
                if db_data:
                    for item in db_data:
                        dmp_tracker_data = item.dmpdata
                        dmp_tracker_data.tempo_qc_status=tempo_status
                        dmp_tracker_data.date_updated = str(datetime.datetime.now())
                        dmp_tracker_data.updated_by = "tempo pipeline"
                        db.session.commit()
                    response = make_response(jsonify(success=True,
                                         message="successfully updated tempo status."), 200)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                else:
                    response = make_response(jsonify(success=False,
                                                     message="No matching records for cmo_id and igo_id found."), 400)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
            else:
                message = "Missing parameter values. Valid cmo_id, igo_id and tempo_status values are required to update" \
                          " tempo status."
                response = make_response(jsonify(success=False,
                                             message=message), 400)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
        except Exception as e:
            response = make_response(
                jsonify(success=False,
                        message="Server error. failed to update tempo status"), 500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(e)
            LOG.error(traceback.print_exc(e))
            return response

@app.route("/update_tempo_delivery_date", methods=['POST'])
def update_tempo_delivery_date():
    """
    Endpoint to update Tempo Output Delivery Date on the Dmpdata object related to Sample. 
    Find Sample using cmo_id and igo_id passed by the request. 
    If matching Sample is found, find related Dmpdata and update tempo_output_delivery_date 
    value to delivery_date passed by request. 
    Do not overwrite non-empty values unless the date is determined to be earlier. 
    @param cmo_id : cmo_id for the sample to update. It is required.
    @param igo_id : igo_id for the sample to update. It is required.
    @param delivery_date: date as string. 
    """
    if request.method == "POST":
        parms = request.get_json(force=True)
        print("Tempo delivery parameters: ", parms)
        cmo_id = parms.get('cmo_id')
        igo_id = parms.get('igo_id')
        delivery_date = parms.get('delivery_date', datetime.datetime.now().strftime("%m-%d-%Y"))
        class UnparseableDate(ValueError):
            pass
        try:
            if cmo_id and igo_id and delivery_date:
                delivery_date = delivery_date[:10]
                embargo_end_date = calculate_outdate(delivery_date)
                if embargo_end_date == "":
                    raise UnparseableDate("Valid Embargo End Date could not be calculated.")
                db_data = db.session.query(Sample).filter(Sample.sampleid == igo_id, Sample.cmo_sampleid==cmo_id).all()
                LOG.info(msg="found {} records to update tempo delivery date".format(len(db_data)))
                if db_data:
                    for item in db_data:
                        dmp_tracker_data = item.dmpdata
                        older_date = False
                        try:
                            older_date = (datetime.datetime.strptime(delivery_date,"%m-%d-%Y")-datetime.datetime.strptime(dmp_tracker_data.tempo_output_delivery_date,"%m-%d-%Y")).days < 0
                        except:
                            pass
                        if dmp_tracker_data.tempo_output_delivery_date in [None, ""] or older_date:
                            dmp_tracker_data.tempo_output_delivery_date=str(delivery_date)
                            dmp_tracker_data.embargo_end_date=str(embargo_end_date)
                            dmp_tracker_data.date_updated = str(datetime.datetime.now())
                            dmp_tracker_data.updated_by = "tempo pipeline"
                            db.session.commit()
                    response = make_response(jsonify(success=True,
                                         message="successfully updated tempo status."), 200)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                else:
                    response = make_response(jsonify(success=False,
                                                     message="No matching records for cmo_id and igo_id found."), 400)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
            else:
                message = "Missing parameter values. Valid cmo_id, igo_id and delivery_date values are required to update" \
                          " tempo output delivery date."
                response = make_response(jsonify(success=False,
                                             message=message), 400)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
        except UnparseableDate as u:
            response = make_response(
                jsonify(success=False,
                        message="Error: " + u),500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(u)
            LOG.error(traceback.print_exc(u))
            return response

        except Exception as e:
            response = make_response(
                jsonify(success=False,
                        message="Server error. Failed to update tempo output delivery date."), 500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(e)
            LOG.error(traceback.print_exc(e))
            return response

@app.route("/update_tempo_analysis_complete", methods=['POST'])
def update_tempo_analysis_complete():
    """
    Endpoint to update Tempo Analysis Update on the Dmpdata object related to Sample. 
    Find Sample using cmo_id and igo_id passed by the request. 
    If matching Sample is found, find related Dmpdata and update tempo_analysis_update 
    value to analysis_date passed by request. 
    @param cmo_id : cmo_id for the sample to update. It is required.
    @param igo_id : igo_id for the sample to update. It is required.
    @param analysis_date: date as string.
    """
    if request.method == "POST":
        parms = request.get_json(force=True)
        print("Tempo analysis complete parameters: ", parms)
        cmo_id = parms.get('cmo_id')
        igo_id = parms.get('igo_id')
        analysis_date = parms.get('analysis_date', datetime.datetime.now().strftime("%m-%d-%Y"))
        try:
            if cmo_id and igo_id:
                analysis_date = analysis_date[:10]
                datetime.datetime.strptime(analysis_date,"%m-%d-%Y")
                db_data = db.session.query(Sample).filter(Sample.sampleid == igo_id, Sample.cmo_sampleid==cmo_id).all()
                LOG.info(msg="found {} records to update tempo analysis update date".format(len(db_data)))
                if db_data:
                    for item in db_data:
                        dmp_tracker_data = item.dmpdata
                        dmp_tracker_data.tempo_analysis_update = analysis_date
                        dmp_tracker_data.date_updated = str(datetime.datetime.now())
                        dmp_tracker_data.updated_by = "tempo pipeline"
                        db.session.commit()
                    response = make_response(jsonify(success=True,
                                         message="successfully updated tempo analysis update date."), 200)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                else:
                    response = make_response(jsonify(success=False,
                                                     message="No matching records for cmo_id and igo_id found."), 400)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
            else:
                message = "Missing parameter values. Valid cmo_id, igo_id and analysis_date values are required to update" \
                          " tempo analysis update date."
                response = make_response(jsonify(success=False,
                                             message=message), 400)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
        except Exception as e:
            response = make_response(
                jsonify(success=False,
                        message="Server error. Failed to update tempo analysis update date."), 500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(e)
            LOG.error(traceback.print_exc(e))
            return response

@app.route("/update_cmo_id", methods=['POST'])
def update_cmo_id():
    """
    Endpoint to update CMO Patient ID on the Dmpdata object related to Sample.
    Find Sample using igo_id passed by the request.
    If matching Sample is found, update cmo_sampleid and cmo_patientid
    value to cmo_id passed by request.
    Do not overwrite non-empty values unless the date is determined to be earlier.
    @param cmo_id : cmo_id for the sample to update. It is required.
    @param igo_id : igo_id for the sample to update. It is required.
    @param overwrite : boolean value indicated whether previous value for 
    cmo_sampleid and cmo_patientid should be overwritten. Default to False.
    """
    if request.method == "POST":
        parms = request.get_json(force=True)
        print("CMO ID update parameters: ", parms)
        cmo_id = parms.get('cmo_id')
        igo_id = parms.get('igo_id')
        overwrite = parms.get('overwrite',False)
        class UnparseableCmo(ValueError):
            pass
        class BoolValueError(ValueError):
            pass
        try:
            if not isinstance(overwrite,bool):
                raise BoolValueError("Invalid overwrite value, boolean required.")
            if cmo_id and igo_id:
                cmo_id_styled = cmo_id.replace("_","-")
                if cmo_id_styled.startswith("s-C-"):
                    cmo_id_styled = cmo_id_styled[2:]
                if len(re.findall('^C-[A-Z0-9]{6}-\w\d{3}-d',cmo_id_styled)) != 1:
                    raise UnparseableCmo("Not a valid CMO ID")
                db_data = db.session.query(Sample).filter(Sample.sampleid == igo_id).all()
                LOG.info(msg="found {} records to update CMO ID".format(len(db_data)))
                if db_data:
                    for item in db_data:
                        if item.cmo_sampleid in [None, ""] or overwrite == True:
                            item.cmo_sampleid = cmo_id_styled
                            item.cmo_patientid = cmo_id_styled[:8]
                            item.date_updated = str(datetime.datetime.now())
                            item.updated_by = "tempo pipeline"
                            db.session.commit()
                    response = make_response(jsonify(success=True,
                                         message="successfully updated tempo status."), 200)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                else:
                    response = make_response(jsonify(success=False,
                                                     message="No matching records for cmo_id and igo_id found."), 400)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
            else:
                message = "Missing parameter values. Valid cmo_id and igo_id are required to update" \
                          " CMO Sample ID and CMO Patient ID."
                response = make_response(jsonify(success=False,
                                             message=message), 400)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
        except UnparseableCmo as u:
            response = make_response(
                jsonify(success=False,
                        message="Error: " + u),500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(u)
            LOG.error(traceback.print_exc(u))
            return response

        except Exception as e:
            response = make_response(
                jsonify(success=False,
                        message="Server error. Failed to update CMO ID. " + e), 500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(e)
            LOG.error(traceback.print_exc(e))
            return response

        except BoolValueError as v:
            response = make_response(
                jsonify(success=False,
                        message="Server error. Failed to update CMO ID. " + v), 500)
            response.headers.add('Access-Control-Allow-Origin', '*')
            print(v)
            LOG.error(traceback.print_exc(v))
            return response

