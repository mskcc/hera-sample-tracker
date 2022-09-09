###############################################################HandsonTable Column configs #############################################################################

clinicalColHeaders = ['MRN', 'Mol Accession #', 'Tempo QC Status', 'DMP Sample ID', 'CMO Sample ID', 'Sample Class', 'Tumor Type',
                      'Parental Tumor Type', 'Tumor Site',  'User Sample ID', 'IGO Request ID',
                      'DMP Request ID', 'Sequencing Site', 'Baitset',  'Project Name', 'Lab Head', 'Scientific PI',
                      'Data Custodian', 'Data Analyst', 'Tempo Output Delivery Date', 'Embargo End Date', 'Access Level', 'Consent Part A',
                      'Consent Part C'
                      ]

clinicalColumns = [
    {
        'data': 'mrn',
        'readOnly': True
    },
    {
        'data': 'molecular_accession_num',
        'readOnly': True
    },
    {
        'data': 'tempo_qc_status',
        'readOnly': True
    },
    {
        'data': 'dmp_sampleid',
        'readOnly': True
    },
    {
        'data': 'cmo_sampleid',
        'readOnly': True
    },
    {
        'data': 'sample_class',
        'readOnly': True
    },
    {
        'data': 'tumor_type',
        'readOnly': True
    },
    {
        'data': 'parental_tumortype',
        'readOnly': True
    },
    {
        'data': 'tumor_site',
        'readOnly': True
    },
    {
        'data': 'user_sampleid',
        'readOnly': True
    },
    {
        'data': 'igo_requestid',
        'readOnly': True
    },
    {
        'data': 'dmp_requestid',
        'readOnly': True
    },
    {
        'data': 'seqiencing_site',
        'readOnly': True
    },
    {
        'data': 'baitset_used',
        'readOnly': True
    },
    {
        'data': 'project_title',
        'readOnly': True
    },
    {
        'data': 'lab_head',
        'readOnly': True
    },
    {
        'data': 'scientific_pi',
        'readOnly': True
    },
    {
        'data': 'data_custodian',
        'readOnly': True
    },
    {
        'data': 'data_analyst',
        'readOnly': True
    },
    {
        'data': 'tempo_output_delivery_date',
        'readOnly': True
    },
    {
        'data': 'embargo_end_date',
        'readOnly': True
    },
    {
        'data': 'access_level',
        'readOnly': True
    },
    {
        'data': 'consent_parta_status',
        'readOnly': True
    },
    {
        'data': 'consent_partc_status',
        'readOnly': True
    },
]


nonClinicalColHeaders = ['DMP Sample ID', 'User Sample ID', 'CMO Sample ID', 'Molecular Accession No.', 'Sex', 'Tumor Type',
                         'Parental Tumor Type', 'Tumor Site', 'Sample Class', 'Sequencing Site', 'Baitset', 'Data Custodian',
                         'Tempo Output Delivery Date', 'Embargo End Date', 'Access Level', 'Consent Part A', 'Consent Part C']

nonClinicalColumns = [
    {
        'data': 'dmp_sampleid',
        'readOnly': True
    },
    {
        'data': 'user_sampleid',
        'readOnly': True
    },
    {
        'data': 'cmo_sampleid',
        'readOnly': True
    },
    {
        'data': 'molecular_accession_num',
        'readOnly': True
    },
    {
        'data': 'sex',
        'readOnly': True
    },
    {
        'data': 'tumor_type',
        'readOnly': True
    },
    {
        'data': 'parental_tumortype',
        'readOnly': True
    },
    {
        'data': 'tumor_site',
        'readOnly': True
    },
    {
        'data': 'sample_class',
        'readOnly': True
    },
    {
        'data': 'seqiencing_site',
        'readOnly': True
    },
    {
        'data': 'baitset_used',
        'readOnly': True
    },
    {
        'data': 'data_custodian',
        'readOnly': True
    },
    {
        'data': 'tempo_output_delivery_date',
        'readOnly': True
    },
    {
        'data': 'embargo_end_date',
        'readOnly': True
    },
    {
        'data': 'access_level',
        'readOnly': True
    },
    {
        'data': 'consent_parta_status',
        'readOnly': True
    },
    {
        'data': 'consent_partc_status',
        'readOnly': True
    },
]

adminColHeaders = ['MRN', 'Mol Accession #', 'Tempo QC Status', 'DMP Patient ID', 'DMP Sample ID', 'CMO Patient ID', 'CMO Sample ID',
                   'Sample Class', 'Tumor Type', 'Parental Tumor Type', 'Tumor Site', 'User Sample ID',
                   'User Sample ID-historical', 'WES Sample ID', 'Source DNA Type', 'Sample Status',
                   'PM Redaction', 'Sex', 'IGO ID', 'Alt ID', 'IGO Request ID', 'DMP Request ID', 'Application',
                   'Sequencing Site', 'Baitset', 'Sequencer', 'IGO Complete Date', 'Project Name', 'Lab Head',
                   'Scientific PI', 'Data Custodian', 'Data Analyst', 'CC/Fund', 'Tempo Output Delivery Date', 'Embargo End Date',
                   'Tempo Analysis Update', 'Access Level', 'Consent Part A', 'Consent Part C']

adminColumns = [
    {
        'data': 'mrn',
        'readOnly': True
    },
    {
        'data': 'molecular_accession_num',
        'readOnly': True
    },
    {
        'data': 'tempo_qc_status',
        'editor': 'select',
        'selectOptions': ['Pass', 'Failed', 'Not Run']
    },
    {
        'data': 'dmp_patientid',
        'readOnly': True
    },
    {
        'data': 'dmp_sampleid',
        'readOnly': True
    },
    {
        'data': 'cmo_patientid',
        'readOnly': True
    },
    {
        'data': 'cmo_sampleid',
        'readOnly': True
    },
    {
        'data': 'sample_class',
        'readOnly': True
    },
    {
        'data': 'tumor_type',
        'readOnly': True
    },
    {
        'data': 'parental_tumortype',
        'readOnly': True
    },
    {
        'data': 'tumor_site',
        'readOnly': True
    },
    {
        'data': 'user_sampleid',
        'readOnly': True
    },
    {
        'data': 'user_sampleid_historical',
        'readOnly': True
    },
    {
        'data': 'wes_sampleid',
        'readOnly': True
    },
    {
        'data': 'source_dna_type',
        'readOnly': True
    },
    {
        'data': 'sample_status',
        'readOnly': True
    },
    {
        'data': 'pm_redaction',
        'type': 'autocomplete',
        'source': ['CCS_DMP_DUPLICATE','HERA_BUG','NOT_CONSENTED'],
        'strict': False
    },
    {
        'data': 'sex',
        'readOnly': True
    },
    {
        'data': 'sampleid',
        'readOnly': True,
    },
    {
        'data': 'alt_id',
        'readOnly': True
    },
    {
        'data': 'igo_requestid',
        'readOnly': True
    },
    {
        'data': 'dmp_requestid',
        'readOnly': True
    },
    {
        'data': 'application_requested',
        'readOnly': True
    },
    {
        'data': 'seqiencing_site',
        'editor': 'select',
        'selectOptions': ['IGO', 'Outside']
    },
    {
        'data': 'baitset_used'
    },
    {
        'data': 'sequencer_type',
        'readOnly': True
    },
    {
        'data': 'date_igo_complete',
        'readOnly': True
    },
    {
        'data': 'project_title',
        'readOnly': True
    },
    {
        'data': 'lab_head',
        'readOnly': True
    },
    {
        'data': 'scientific_pi',
    },
    {
        'data': 'data_custodian',
        'readOnly': True
    },
    {
        'data': 'data_analyst',
    },
    {
        'data': 'cc_fund',
        'readOnly': True
    },
    {
        'data': 'tempo_output_delivery_date',
        'readOnly': True
    },
    {
        'data': 'embargo_end_date',
        'readOnly': True
    },
    {
        'data': 'tempo_analysis_update',
        'readOnly':True
    },
    {
        'data': 'access_level',
        'editor': 'select',
        'selectOptions': ['MSK Embargo', 'MSK public', 'Published']
    },
    {
        'data': 'consent_parta_status',
        'readOnly': True
    },
    {
        'data': 'consent_partc_status',
        'readOnly': True
    },
]

settings = {
    'columnSorting': True,
    'filters': True,
    'autoColumnSize': True,
    'width': '100%',
    'height': 500,
    'colWidths': [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                  200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                  200, 200, 200],
    'manualColumnResize': True,
    'rowHeaders': True,
    'colHeaders': True,
    'search': True,
    'dropdownMenu': ['filter_by_condition', 'filter_action_bar'],
}

########################################################################################################################################
