import datetime

from flask import json
from flask_sqlalchemy import SQLAlchemy, Model

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(300), nullable=False)


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sampleid = db.Column(db.String(300), unique=True, nullable=False)  # pulled from LIMS Sample table
    user_sampleid = db.Column(db.String(300), unique=True, nullable=False)  # pulled from LIMS Sample table
    cmo_sampleid = db.Column(db.String(300))  # pulled from LIMS Sample table
    cmo_patientid = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    dmp_sampleid = db.Column(db.String(300))  # pulled from CVR endpoint
    dmp_patientid = db.Column(db.String(300))  # pulled from CVR endpoint
    mrn = db.Column(db.String(300))  # pulled from CVR endpoint
    sex = db.Column(db.String(300))  # pulled from CVR endpoint
    sample_type = db.Column(db.String(300))  # pulled from CVR endpoint
    sample_class = db.Column(db.String(300))  # pulled from CVR endpoint
    tumor_type = db.Column(db.String(300))  # pulled from CVR endpoint
    parental_tumortype = db.Column(db.String(300))  # pulled from Oncotree endpoint
    tumor_site = db.Column(db.String(300))  # pulled from CVR endpoint
    molecular_accession_num = db.Column(db.String(300))  # pulled from CVR endpoint
    collection_year = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    date_dmp_request = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    dmp_requestid = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    igo_requestid = db.Column(db.String(300))  # pulled from LIMS SampleCMOInfoRecords table
    date_igo_received = db.Column(db.String(300))  # pulled from LIMS Request table
    date_igo_complete = db.Column(db.String(300))  # pulled from LIMS Request table
    application_requested = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    baitset_used = db.Column(db.String(300))  # pulled from LIMS KAPAAgilentCaptureProtocol2 table
    sequencer_type = db.Column(db.String(300))  # pulled from LIMS SeqAnalysisSampleQC table
    project_title = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    lab_head = db.Column(db.String(300))  # pulled from LIMS Request table
    cc_fund = db.Column(db.String(300))  # pulled from LIMS DMPSampleTracker table
    scientific_pi = db.Column(db.String(300))  # entered by PM's
    consent_parta_status = db.Boolean()  # pulled from CVR endpoint
    consent_partc_status = db.Boolean()  # pulled from CVR endpoint
    sample_status = db.Column(db.String(300))  # pulled from LIMS Sample table
    access_level = db.Column(db.String(300), default="MSK Public")  # default "MSK Public", updated by PM's
    clinical_trial = db.Column(db.String(300))  # entered by PM's
    seqiencing_site = db.Column(db.String(300))  # entered by PM's
    pi_request_date = db.Column(db.String(300))  # entered by PM's
    pipeline = db.Column(db.String(300))  # entered by PM's
    tissue_type = db.Column(db.String(300))  # entered by PM's
    collaboration_center = db.Column(db.String(300))  # entered by PM's
    lims_recordId = db.Column(db.String(300))  # entered by PM's

    def __init__(self, sampleid=None, user_sampleid=None, cmo_sampleid=None, cmo_patientid=None, dmp_sampleid=None,
                 dmp_patientid=None, mrn=None, sex=None, sample_type=None, sample_class=None, tumor_type=None, parental_tumortype=None,
                 tumor_site=None, molecular_accession_num=None, collection_year=None, date_dmp_request=None, dmp_requestid=None,
                 igo_requestid=None, date_igo_received=None, date_igo_complete=None, application_requested=None, baitset_used=None,
                 sequencer_type=None, project_title=None, lab_head=None, cc_fund=None, scientific_pi=None, consent_parta_status=None,
                 consent_partc_status=None, sample_status=None, access_level=None, clinical_trial=None, seqiencing_site=None, pi_request_date=None,
                 pipeline=None, tissue_type=None, collaboration_center=None, lims_recordId=None
                 ):

        self.sampleid = sampleid
        self.user_sampleid = user_sampleid
        self.cmo_sampleid = cmo_sampleid
        self.cmo_patientid = cmo_patientid
        self.dmp_sampleid = dmp_sampleid
        self.dmp_patientid = dmp_patientid
        self.mrn = mrn
        self.sex = sex
        self.sample_type = sample_type
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
        self.lab_head = lab_head
        self.cc_fund = cc_fund
        self.scientific_pi = scientific_pi
        self.consent_parta_status = consent_parta_status
        self.consent_partc_status = consent_partc_status
        self.sample_status = sample_status
        self.access_level = access_level
        self.clinical_trial = clinical_trial
        self.seqiencing_site = seqiencing_site
        self.pi_request_date = pi_request_date
        self.pipeline = pipeline
        self.tissue_type = tissue_type
        self.collaboration_center = collaboration_center
        self.lims_recordId = lims_recordId


class BlacklistToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    jti2 = db.Column(db.String(120))


    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        query = BlacklistToken.query.filter_by(jti=jti).first()
        return bool(query)


class AppLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column (db.String(300))
    level = db.Column(db.String(300))
    process = db.Column(db.String(300))
    user = db.Column(db.String(300))
    message = db.Column(db.Text(4294000000))

    def __init__(self, time = datetime.datetime.now(), level= None, process=None, user=None, message=None):
        self.time=time
        self.level = level,
        self.process=process
        self.user=user
        self.message=message

    def log(self, db=db):
        db.session.add(self)
        db.session.commit()
        db.session.flush()