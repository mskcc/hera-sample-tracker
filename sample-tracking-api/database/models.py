import datetime
from collections import defaultdict

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_continuum import make_versioned

db = SQLAlchemy()
make_versioned(user_cls=None)


class Dmpdata(db.Model):
    __versioned__ = {}
    __tablename__ = 'dmpdata'
    id = db.Column(db.Integer, primary_key=True)
    user_sampleid_historical = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    user_sampleid = db.Column(db.String(300))
    duplicate_sample = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    wes_sampleid = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    source_dna_type = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    date_dmp_request = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    dmp_requestid = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    project_title = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    data_analyst = db.Column(db.String(300))  # entered by PM's
    data_custodian = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    cc_fund = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    scientific_pi = db.Column(db.String(300))  # entered by PM's
    access_level = db.Column(db.String(300), default="MSK Embargo")  # default "MSK Public", updated by PM's
    clinical_trial = db.Column(db.String(300))  # entered by PM's
    seqiencing_site = db.Column(db.String(300))  # entered by PM's
    pi_request_date = db.Column(db.String(300))  # entered by PM's
    pipeline = db.Column(db.String(300))  # entered by PM's
    tempo_qc_status = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    pm_redaction = db.Column(db.String(300)) # entered by PM's
    tempo_output_delivery_date = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    embargo_end_date = db.Column(db.String(300))
    tempo_analysis_update = db.Column(db.String(300))
    tissue_type = db.Column(db.String(300))  # entered by PM's
    collaboration_center = db.Column(db.String(300))  # entered by PM's
    date_created = db.Column(db.String(300))
    created_by = db.Column(db.String(300))
    date_updated = db.Column(db.String(300))
    updated_by = db.Column(db.String(300))
    lims_tracker_recordid = db.Column(db.String(300), unique=True, nullable=False, index=True)
    samples = db.relationship('Sample', backref='dmpdata', lazy='joined')
    cvr_data = db.relationship('Cvrdata', backref='dmpdata', uselist=False, lazy='joined')


class Cvrdata(db.Model):
    __versioned__ = {}
    __tablename__ = 'cvrdata'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    dmp_sampleid = db.Column(db.String(300))  # pulled from CVR endpoint
    dmp_patientid = db.Column(db.String(300))  # pulled from CVR endpoint
    mrn = db.Column(db.String(300))  # pulled from CVR endpoint
    sex = db.Column(db.String(300))  # pulled from CVR endpoint
    sample_class = db.Column(db.String(300))  # pulled from CVR endpoint
    tumor_type = db.Column(db.String(300))  # pulled from CVR endpoint
    tumor_site = db.Column(db.String(300))  # pulled from CVR endpoint
    molecular_accession_num = db.Column(db.String(300))  # pulled from CVR endpoint
    consent_parta_status = db.Column(db.Boolean())  # pulled from CVR endpoint
    consent_partc_status = db.Column(db.Boolean())  # pulled from CVR endpoint
    date_created = db.Column(db.String(300))
    created_by = db.Column(db.String(300))
    date_updated = db.Column(db.String(300))
    updated_by = db.Column(db.String(300))
    lims_tracker_recordid = db.Column(db.String(300), db.ForeignKey('dmpdata.lims_tracker_recordid'))


class Sample(db.Model):
    __versioned__ = {}
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    sampleid = db.Column(db.String(300))  # pulled from LIMS Sample table
    alt_id = db.Column(db.String(300))  # pulled from LIMS Sample table
    cmo_sampleid = db.Column(db.String(300))  # pulled from LIMS Sample table
    cmo_patientid = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    sample_type = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    parental_tumortype = db.Column(db.String(300))  # pulled from Oncotree endpoint
    collection_year = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    igo_requestid = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    date_igo_received = db.Column(db.String(300))  # pulled from LIMS Request table
    date_igo_complete = db.Column(db.String(300))  # pulled from LIMS Request table
    application_requested = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    baitset_used = db.Column(db.String(300))  # pulled from LIMS KAPAAgilentCaptureProtocol2 table
    sequencer_type = db.Column(db.String(300))  # pulled from LIMS SeqAnalysisSampleQC table
    lab_head = db.Column(db.String(300))  # pulled from LIMS Request table
    sample_status = db.Column(db.String(300))  # pulled from LIMS Sample table
    date_created = db.Column(db.String(300))
    created_by = db.Column(db.String(300))
    date_updated = db.Column(db.String(300))
    updated_by = db.Column(db.String(300))
    lims_sample_recordid = db.Column(db.String(300))  # entered by PM's
    lims_tracker_recordid = db.Column(db.String(300), db.ForeignKey('dmpdata.lims_tracker_recordid'))


class Dmpsampledata():

    def __init__(self, id=None, sampleid=None, alt_id=None, user_sampleid=None, user_sampleid_historical=None,
                 duplicate_sample=None,
                 wes_sampleid=None, cmo_sampleid=None, cmo_patientid=None, dmp_sampleid=None,
                 dmp_patientid=None, mrn=None, sex=None, source_dna_type=None, sample_class=None, tumor_type=None,
                 parental_tumortype=None, tumor_site=None, molecular_accession_num=None, collection_year=None,
                 date_dmp_request=None, dmp_requestid=None, igo_requestid=None, date_igo_received=None,
                 date_igo_complete=None, application_requested=None, baitset_used=None, sequencer_type=None,
                 project_title=None, data_analyst=None, data_custodian=None, lab_head=None, cc_fund=None,
                 scientific_pi=None,
                 consent_parta_status=None, consent_partc_status=None, sample_status=None, access_level="MSK Public",
                 seqiencing_site=None, pi_request_date=None, tempo_qc_status=None, pm_redaction=None,
                 tempo_output_delivery_date=None, embargo_end_date=None, tempo_analysis_update=None, tissue_type=None, lims_sample_recordid=None,
                 lims_tracker_recordid=None
                 ):
        self.id = id
        self.sampleid = sampleid
        self.alt_id = alt_id
        self.user_sampleid = user_sampleid
        self.user_sampleid_historical = user_sampleid_historical
        self.duplicate_sample = duplicate_sample
        self.wes_sampleid = wes_sampleid
        self.cmo_sampleid = cmo_sampleid
        self.cmo_patientid = cmo_patientid
        self.dmp_sampleid = dmp_sampleid
        self.dmp_patientid = dmp_patientid
        self.mrn = mrn
        self.sex = sex
        self.source_dna_type = source_dna_type;
        self.sample_class = sample_class
        self.tumor_type = tumor_type
        self.parental_tumortype = parental_tumortype
        self.tumor_site = tumor_site
        self.molecular_accession_num = molecular_accession_num
        self.collection_year = collection_year
        self.date_dmp_request = date_dmp_request
        self.dmp_requestid = dmp_requestid
        self.igo_requestid = igo_requestid
        self.date_igo_received = date_igo_received
        self.date_igo_complete = date_igo_complete
        self.application_requested = application_requested
        self.baitset_used = baitset_used
        self.sequencer_type = sequencer_type
        self.project_title = project_title
        self.data_analyst = data_analyst
        self.data_custodian = data_custodian
        self.lab_head = lab_head
        self.cc_fund = cc_fund
        self.scientific_pi = scientific_pi
        self.consent_parta_status = consent_parta_status
        self.consent_partc_status = consent_partc_status
        self.sample_status = sample_status
        self.access_level = access_level
        self.seqiencing_site = seqiencing_site
        self.pi_request_date = pi_request_date
        self.tempo_qc_status = tempo_qc_status
        self.pm_redaction = pm_redaction
        self.tempo_output_delivery_date = tempo_output_delivery_date
        self.embargo_end_date = embargo_end_date
        self.tempo_analysis_update = tempo_analysis_update
        self.tissue_type = tissue_type
        self.lims_sample_recordid = lims_sample_recordid
        self.lims_tracker_recordid = lims_tracker_recordid


def create_sample_object(dmpdata, cvrdata, sample):
    """
    method to return Sample Data Object created from three data types passed as params.
    :param dmpdata:
    :param cvrdata:
    :param sample:
    :return:
    """
    sample_object = Dmpsampledata()
    sample_object.id = dmpdata.id
    sample_object.user_sampleid_historical = dmpdata.user_sampleid_historical
    sample_object.user_sampleid = dmpdata.user_sampleid
    sample_object.duplicate_sample = dmpdata.duplicate_sample
    sample_object.wes_sampleid = dmpdata.wes_sampleid
    sample_object.date_dmp_request = dmpdata.date_dmp_request
    sample_object.dmp_requestid = dmpdata.dmp_requestid
    sample_object.project_title = dmpdata.project_title
    sample_object.data_analyst = dmpdata.data_analyst
    sample_object.data_custodian = dmpdata.data_custodian
    sample_object.cc_fund = dmpdata.cc_fund
    sample_object.scientific_pi = dmpdata.scientific_pi
    sample_object.access_level = dmpdata.access_level
    sample_object.seqiencing_site = dmpdata.seqiencing_site
    sample_object.pi_request_date = dmpdata.pi_request_date
    sample_object.tempo_qc_status = dmpdata.tempo_qc_status
    sample_object.pm_redaction = dmpdata.pm_redaction
    sample_object.tempo_output_delivery_date = dmpdata.tempo_output_delivery_date
    sample_object.embargo_end_date = dmpdata.embargo_end_date
    sample_object.tempo_analysis_update = dmpdata.tempo_analysis_update
    sample_object.tissue_type = dmpdata.tissue_type
    sample_object.source_dna_type = dmpdata.source_dna_type
    sample_object.dmp_sampleid = cvrdata.dmp_sampleid
    sample_object.dmp_patientid = cvrdata.dmp_patientid
    sample_object.mrn = cvrdata.mrn
    sample_object.sex = cvrdata.sex
    sample_object.sample_class = cvrdata.sample_class
    sample_object.tumor_type = cvrdata.tumor_type
    sample_object.tumor_site = cvrdata.tumor_site
    sample_object.molecular_accession_num = cvrdata.molecular_accession_num
    sample_object.consent_parta_status = cvrdata.consent_parta_status
    sample_object.consent_partc_status = cvrdata.consent_partc_status
    sample_object.sampleid = sample.sampleid if sample else ''
    sample_object.alt_id = sample.alt_id if sample else ''
    sample_object.cmo_sampleid = sample.cmo_sampleid if sample else ''
    sample_object.cmo_patientid = sample.cmo_patientid if sample else ''
    sample_object.parental_tumortype = sample.parental_tumortype if sample else ''
    sample_object.collection_year = sample.collection_year if sample else ''
    sample_object.igo_requestid = sample.igo_requestid if sample else ''
    sample_object.date_igo_received = sample.date_igo_received if sample else ''
    sample_object.date_igo_complete = sample.date_igo_complete if sample else ''
    sample_object.application_requested = sample.application_requested if sample else ''
    sample_object.baitset_used = sample.baitset_used if sample else ''
    sample_object.sequencer_type = sample.sequencer_type if sample else ''
    sample_object.lab_head = sample.lab_head if sample else ''
    sample_object.sample_status = sample.sample_status if sample else ''
    sample_object.lims_tracker_recordid = dmpdata.lims_tracker_recordid
    sample_object.lims_sample_recordid = sample.lims_sample_recordid if sample else ''
    return sample_object


def filter_qc_application(sample_objects):
    """
    Method to filter Samples with QC application when same samples also have %exome% as recipe under one of the
    Request within a Project. Note: A project can have multiple child Requests.
    :param sample_objects
    """
    after_filter_duplicates = []
    groups = defaultdict(list)
    for obj in sample_objects:
        if obj.igo_requestid:
            project = obj.igo_requestid.split("_")[0]
            groups[project + "__" + obj.dmp_sampleid].append(obj)
        else:
            groups["solo"].append(obj)
    for key in groups.keys():
        if key != "solo":
            values = groups[key]
            if len(values) > 1:
                for sample in values:
                    if "exome" in sample.application_requested.lower():
                        after_filter_duplicates.append(sample)
                    else:
                        after_filter_duplicates.append(sample)
            else:
                after_filter_duplicates.extend(values)
        if key == "solo":
            non_igo_objs = groups[key]
            after_filter_duplicates.extend(non_igo_objs)
    return after_filter_duplicates


def get_sample_objects(objlist, filter_failed):
    """ Method to get Sample Objects with boolean param to filter Sample Objects with sample_status '%failed-%'
    :param objlist
    :param filter_failed
    """
    sample_objects = []
    for dmpdata in objlist:
        samples = dmpdata.samples
        cvrdata = dmpdata.cvr_data
        if len(samples) > 1 and (has_sequencing_status(samples) or has_mixed_application(samples)):
            desired_samples = get_desired_sample(samples)
            if filter_failed is False:
                for sample in desired_samples:
                    sample_object = create_sample_object(dmpdata, cvrdata, sample)
                    sample_objects.append(sample_object)
            if filter_failed is True:
                for sample in desired_samples:
                    if 'failed' not in sample.sample_status.lower():
                        sample_object = create_sample_object(dmpdata, cvrdata, sample)
                        sample_objects.append(sample_object)
        elif len(samples) == 1:
            sample = samples[0]
            sample_object = create_sample_object(dmpdata, cvrdata, sample)
            sample_objects.append(sample_object)
        elif len(samples) > 1 and not has_mixed_application(samples):
            for sample in samples:
                sample_object = create_sample_object(dmpdata, cvrdata, sample)
                sample_objects.append(sample_object)
        else:
            sample = None
            sample_object = create_sample_object(dmpdata, cvrdata, sample)
            sample_objects.append(sample_object)
    return filter_qc_application(sample_objects)


def has_mixed_application(sample_list):
    """
    Method to check if Sample Objects in sample_list has different application_requested values.
    :param sample_list"""
    qc_application = False
    exome_application = False
    for samp in sample_list:
        if samp.application_requested and 'exome' in samp.application_requested.lower():
            exome_application = True
        if samp.application_requested and 'qc' in samp.application_requested.lower():
            qc_application = True
    if qc_application is True and exome_application is True:
        return True
    return False


def has_sequencing_status(sample_list):
    """
        Method to check if Sample Objects in sample_list has completed sequencing status.
        :param sample_list
    """
    failed_sequencing_status = "failed - illumina sequencing analysis"
    completed_sequencing_status = "data qc - completed"
    for samp in sample_list:
        if samp.sample_status and (failed_sequencing_status in samp.application_requested.lower() or
                                   completed_sequencing_status in samp.sample_status.lower()):
            return True
    return False


def get_desired_sample(sample_list):
    """
    Method to get samples with desired application_requested value or sample status. Sample status indicating Sequencing
    completion checked first followed by application_requested value that matches
    %exome%' followed by '%library%' and then everything else.
    :param sample_list
    """
    sequencing_passed_samples = []
    sequencing_failed_samples = []
    exome_samples = []
    library_samples = []
    failed_sequencing_status = "failed - illumina sequencing analysis"
    completed_sequencing_status = "data qc - completed"
    for samp in sample_list:
        if completed_sequencing_status in samp.sample_status.lower():
            sequencing_passed_samples.append(samp)
        if failed_sequencing_status in samp.sample_status.lower():
            sequencing_failed_samples.append(samp)
        if 'exome' in samp.application_requested.lower():
            exome_samples.append(samp)
        # for samp in sample_list:
        if 'library' in samp.application_requested.lower() or 'qc' in samp.application_requested.lower():
            library_samples.append(samp)
    if len(sequencing_passed_samples) > 0:
        return sequencing_passed_samples
    if len(sequencing_failed_samples) > 0:
        return sequencing_failed_samples
    if len(exome_samples) > 0:
        return exome_samples
    if len(library_samples) > 0:
        return library_samples
    return list(sample_list[-1])


class AppLog(db.Model):
    __tablename__ = 'applog'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(300))
    level = db.Column(db.String(300))
    process = db.Column(db.String(300))
    user = db.Column(db.String(300))
    message = db.Column(db.Text(4294000000))

    def __init__(self, time=datetime.datetime.now(), level=None, process=None, user=None, message=None):
        self.time = time
        self.level = level,
        self.process = process
        self.user = user
        self.message = message

    def log(self, db=db):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def info(message, user):
        applog = AppLog()
        applog.level = "INFO"
        applog.process = "root"
        applog.user = user
        applog.message = message
        db.session.add(applog)
        db.session.commit()

    @staticmethod
    def warning(message, user):
        applog = AppLog()
        applog.level = "WARNING"
        applog.process = "root"
        applog.user = user
        applog.message = message
        db.session.add(applog)
        db.session.commit()

    @staticmethod
    def error(message, user):
        applog = AppLog()
        applog.level = "ERROR"
        applog.process = "root"
        applog.user = user
        applog.message = message
        db.session.add(applog)
        db.session.commit()


sa.orm.configure_mappers()
