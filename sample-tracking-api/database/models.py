from flask_sqlalchemy import SQLAlchemy, Model
db = SQLAlchemy()


class User(db.Model):
    id                                  = db.Column(db.Integer, primary_key=True)
    username                            = db.Column(db.String(80), unique=True, nullable=False)
    email                               = db.Column(db.String(120), unique=True, nullable=False)
    password                            = db.Column(db.String(300), nullable=False)


class Samples(db.Model):
    # fields that can be found in LIMS
    id                                  = db.Column(db.Integer, primary_key=True)
    sampleid                            = db.Column(db.String(300), unique=True, nullable=False)
    other_sampleid                      = db.Column(db.String(300), unique=True, nullable=False)
    corrected_cmo_id                    = db.Column(db.String(300))
    request_id                          = db.Column(db.String(300))
    igo_sample_status                   = db.Column(db.String(300))
    pi                                  = db.Column(db.String(300))
    investigator                        = db.Column(db.String(300))
    date_created                        = db.Column(db.Integer)
    date_igo_received                   = db.Column(db.Integer)
    date_igo_complete                   = db.Column(db.Integer)
    lims_sample_record_id               = db.Column(db.Integer)
    baitset_used                        = db.Column(db.String(300))
    investigator_sampleid               = db.Column(db.String(300))
    investigator_patientid              = db.Column(db.String(300))
    data_analyst                        = db.Column(db.String(300))

    # fields coming from DMP end points
    sample_type                         = db.Column(db.String(300))
    tumor_type                          = db.Column(db.String(300))
    sample_class                        = db.Column(db.String(300))
    tumor_site                          = db.Column(db.String(300))
    tissue_location                     = db.Column(db.String(300))
    sex                                 = db.Column(db.String(300))
    mrn                                 = db.Column(db.String(300))
    surgical_accession_number           = db.Column(db.String(300))
    m_accession_number                  = db.Column(db.String(300))
    oncotree_code                       = db.Column(db.String(300))
    parental_tumortype                  = db.Column(db.String(300))
    collection_year                     = db.Column(db.DateTime())
    dmp_sampleid                        = db.Column(db.String(300))
    dmp_patientid                       = db.Column(db.String(300))
    registration_12_245AC               = db.Column(db.String(300))
    vaf                                 = db.Column(db.String(300))
    facets                              = db.Column(db.String(300))


    # fields to be maintained by Project Managers

    associated_clinical_trial = db.Column(db.String(300))
    access_status                       = db.Column(db.String(300))
    data_access_status                  = db.Column(db.String(300))
    date_requested_from_dmp             = db.Column(db.DateTime())
    sample_name                         = db.Column(db.String(300)) # this is duplicate with igo information? confirm
    sampleid_dmp                        = db.Column(db.String(300)) # this is duplicate with igo information? confirm
    recipe_application                  = db.Column(db.String(300)) # this is duplicate with igo information? confirm
    payee                               = db.Column(db.String(300))
    staus                               = db.Column(db.String(300)) # this is duplicate with igo information? confirm
    report                              = db.Column(db.String(300)) # what is this field
    data_requested                      = db.Column(db.String(300))
    date_pipeline_in                    = db.Column(db.DateTime())
    date_pipeline_complete              = db.Column(db.DateTime())
    date_portal_in                      = db.Column(db.DateTime())
    project_title                       = db.Column(db.String(300))
    cc_fund                             = db.Column(db.String(300))
    sequencer_type                      = db.Column(db.String(300))
    cbioportal_sampleid                 = db.Column(db.String(300))
    cbioportal_patientid                = db.Column(db.String(300))
    sequencing_location                 = db.Column(db.String(300))
    pipeline_requested                  = db.Column(db.Boolean())
    dmp_requestid                       = db.Column(db.String(300))
