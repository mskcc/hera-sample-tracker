from flask import json
from flask_sqlalchemy import SQLAlchemy, Model

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)


class Samples(db.Model):
    __tablename__ = 'samples'

    # fields that can be found in LIMS
    id = db.Column(db.Integer, primary_key=True)
    sampleid = db.Column(db.String(300), unique=True, nullable=False)
    other_sampleid = db.Column(db.String(300), unique=True, nullable=False)
    corrected_cmo_id = db.Column(db.String(300))
    request_id = db.Column(db.String(300))
    igo_sample_status = db.Column(db.String(300))
    pi = db.Column(db.String(300))
    investigator = db.Column(db.String(300))
    date_created = db.Column(db.String(300))
    date_igo_received = db.Column(db.String(300))
    date_igo_complete = db.Column(db.String(300))
    lims_sample_record_id = db.Column(db.String(300))
    baitset_used = db.Column(db.String(300))
    investigator_sampleid = db.Column(db.String(300))
    investigator_patientid = db.Column(db.String(300))
    data_analyst = db.Column(db.String(300))

    # fields coming from DMP end points with clinical information
    sample_type = db.Column(db.String(300))
    tumor_type = db.Column(db.String(300))
    sample_class = db.Column(db.String(300))
    tumor_site = db.Column(db.String(300))
    tissue_location = db.Column(db.String(300))
    sex = db.Column(db.String(300))
    mrn = db.Column(db.String(300))
    surgical_accession_number = db.Column(db.String(300))
    m_accession_number = db.Column(db.String(300))
    oncotree_code = db.Column(db.String(300))
    parental_tumortype = db.Column(db.String(300))
    collection_year = db.Column(db.DateTime())
    dmp_sampleid = db.Column(db.String(300))
    dmp_patientid = db.Column(db.String(300))
    registration_12_245AC = db.Column(db.String(300))
    vaf = db.Column(db.String(300))
    facets = db.Column(db.String(300))

    # fields to be maintained by Project Managers and also to be editable fields

    associated_clinical_trial = db.Column(db.String(300))
    access_status = db.Column(db.String(300))
    data_access_status = db.Column(db.String(300))
    date_requested_from_dmp = db.Column(db.DateTime())
    #sample_name = db.Column(db.String(300))  # this is duplicate with igo information? confirm
    #sampleid_dmp = db.Column(db.String(300))  # this is duplicate with igo information? confirm
    recipe_application = db.Column(db.String(300))  # this is duplicate with igo information? confirm
    payee = db.Column(db.String(300))
    #staus = db.Column(db.String(300))  # this is duplicate with igo information? confirm
    report = db.Column(db.String(300))  # what is this field
    data_requested = db.Column(db.String(300))
    date_pipeline_in = db.Column(db.DateTime())
    date_pipeline_complete = db.Column(db.DateTime())
    date_portal_in = db.Column(db.DateTime())
    project_title = db.Column(db.String(300))
    cc_fund = db.Column(db.String(300))
    sequencer_type = db.Column(db.String(300))
    cbioportal_sampleid = db.Column(db.String(300))
    cbioportal_patientid = db.Column(db.String(300))
    sequencing_location = db.Column(db.String(300))
    pipeline_requested = db.Column(db.Boolean())
    dmp_requestid = db.Column(db.String(300))

    def __init__(self, sampleid = None, other_sampleid = None, corrected_cmo_id = None, request_id = None, igo_sample_status = None, pi = None, investigator = None,
                 date_created = None, date_igo_received = None, date_igo_complete = None,lims_sample_record_id = None,baitset_used = None, investigator_sampleid = None,
                 investigator_patientid = None, data_analyst = None,

                 sample_type=None, tumor_type=None, parental_tumortype=None, sample_class=None, tumor_site=None, tissue_location=None, sex=None, mrn=None,
                 surgical_accession_number=None, m_accession_number=None, oncotree_code=None, collection_year=None, dmp_sampleid=None, dmp_patientid=None,
                 registration_12_245AC=None, vaf=None, facets=None,

                 associated_clinical_trial=None, access_status=None, date_requested_from_dmp=None, recipe_application=None, payee=None, cc_fund=None, date_requested=None,
                 project_title=None, date_pipeline_in=None, date_pipeline_complete=None, sequencing_location=None, sequencer_type=None, cbioportal_sampleid=None,
                 cbioportal_patientid=None, date_portal_in=None, pipeline_requested=None, dmp_requestid=None
                  ):

        # IGO LIMS fields
        self.sampleid = sampleid
        self.other_sampleid = other_sampleid
        self.corrected_cmo_id = corrected_cmo_id
        self.request_id = request_id
        self.igo_sample_status = igo_sample_status
        self.pi = pi
        self.investigator = investigator
        self.date_created = date_created
        self.date_igo_received = date_igo_received
        self.date_igo_complete = date_igo_complete
        self.lims_sample_record_id = lims_sample_record_id
        self.baitset_used = baitset_used
        self.investigator_sampleid =investigator_sampleid
        self.investigator_patientid = investigator_patientid
        self.data_analyst = data_analyst

        # fields coming from CVR end points
        self.sample_type = sample_type
        self.tumor_type = tumor_type
        self.parental_tumortype = parental_tumortype
        self.sample_class = sample_class
        self.tumor_site = tumor_site
        self.tissue_location = tissue_location
        self.sex = sex
        self.mrn = mrn
        self.surgical_accession_number = surgical_accession_number
        self.m_accession_number = m_accession_number
        self.oncotree_code = oncotree_code
        self.collection_year = collection_year
        self.dmp_sampleid = dmp_sampleid
        self.dmp_patientid = dmp_patientid
        self.registration_12_245AC = registration_12_245AC
        self.vaf = vaf
        self.facets = facets

        # fields to be populated by PM's
        self.date_requested_from_dmp = date_requested_from_dmp
        self.recipe_application = recipe_application
        self.associated_clinical_trial = associated_clinical_trial
        self.access_status = access_status
        self.payee = payee
        self.cc_fund = cc_fund
        self.date_requested = date_requested
        self.project_title = project_title
        self.date_pipeline_in= date_pipeline_in
        self.date_pipeline_complete = date_pipeline_complete
        self.sequencing_location = sequencing_location
        self.sequencer_type = sequencer_type
        self.cbioportal_sampleid = cbioportal_sampleid
        self.cbioportal_patientid = cbioportal_patientid
        self.date_portal_in = date_portal_in
        self.pipeline_requested = pipeline_requested
        self.dmp_requestid = dmp_requestid


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """

    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))


    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        query = BlacklistToken.query.filter_by(jti=jti).first()
        return bool(query)
