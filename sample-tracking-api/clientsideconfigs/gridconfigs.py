###############################################################HandsonTable Column configs #############################################################################

clinicalColHeaders = ['IGO ID' , 'User Sample ID' , 'CMO Sample ID' , 'CMO Patient ID' , 'DMP Sample ID' ,
                       'DMP Patient ID' , 'MRN' , 'Sex' , 'Sample Type' , 'Sample Class' ,
                       'Tumor Type' , 'Parental Tumor Type' , 'Tumor Site' , 'Mol Accession #' , 'Collection Yr' ,
                       'Date DMP Request' , 'DMP Request ID' , 'IGO Request ID' , 'Date IGO Received' ,
                       'IGO Complete Date' ,
                       'Application' , 'Baitset' , 'Sequencer' , 'Project Name' , 'Lab Head' , 'CC/Fund' ,
                       'Scientific PI' , 'Consent Part A' , 'Consent Part C' , 'Sample Status' ,
                       'Access Level' , 'Clinical Trial' , 'Sequencing Site' , 'PI Request Date' , 'Pipeline' ,
                       'Tissue Type' , 'Collaboration Center']
clinicalColumns = [
    {
        'data' : 'sampleid' ,
        'readOnly' : True ,
        } ,
    {
        'data' : 'user_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cmo_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cmo_patientid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_patientid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'mrn' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sex' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_class' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'parental_tumortype' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_site' ,
        'readOnly' : True
        } ,
    {
        'data' : 'molecular_accession_num' ,
        'readOnly' : True
        } ,
    {
        'data' : 'collection_year' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_dmp_request' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'igo_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_received' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_complete' ,
        'readOnly' : True
        } ,
    {
        'data' : 'application_requested' ,
        'readOnly' : True
        } ,
    {
        'data' : 'baitset_used' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sequencer_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'project_title' ,
        'readOnly' : True
        } ,
    {
        'data' : 'lab_head' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cc_fund' ,
        'readOnly' : True
        } ,
    {
        'data' : 'scientific_pi' ,
        'readOnly' : True
        } ,
    {
        'data' : 'consent_parta_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'consent_partc_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'access_level' ,
        'readOnly' : True
        } ,
    {
        'data' : 'clinical_trial' ,
        'readOnly' : True
        } ,
    {
        'data' : 'seqiencing_site' ,
        'readOnly' : True
        } ,
    {
        'data' : 'pi_request_date' ,
        'readOnly' : True
        } ,
    {
        'data' : 'pipeline' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tissue_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'collaboration_center' ,
        'readOnly' : True
        } ,
    ]

nonClinicalColHeaders = ['IGO ID' , 'User Sample ID' , 'CMO Sample ID' , 'Sex' , 'Sample Type' , 'Sample Class' ,
                          'Tumor Type' , 'Parental Tumor Type' , 'Tumor Site' , 'Collection Yr' , 'Date DMP Request' ,
                          'DMP Request ID' , 'IGO Request ID' , 'Date IGO Received' , 'IGO Complete Date' ,
                          'Application' , 'Baitset' ,
                          'Sequencer' , 'Project Name' , 'Lab Head' , 'CC/Fund' , 'Scientific PI' , 'Sample Status' ,
                          'Access Level' ,
                          'Sequencing Site' , 'PI Request Date' , 'Pipeline' , 'Tissue Type' , 'Collaboration Center']

nonClinicalColumns = [
    {
        'data' : 'sampleid' ,
        'readOnly' : True ,
        'width' : 200
        } ,
    {
        'data' : 'user_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cmo_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sex' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_class' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'parental_tumortype' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_site' ,
        'readOnly' : True
        } ,
    {
        'data' : 'collection_year' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_dmp_request' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'igo_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_received' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_complete' ,
        'readOnly' : True
        } ,
    {
        'data' : 'application_requested' ,
        'readOnly' : True
        } ,
    {
        'data' : 'baitset_used' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sequencer_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'project_title' ,
        'readOnly' : True
        } ,
    {
        'data' : 'lab_head' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cc_fund' ,
        'readOnly' : True
        } ,
    {
        'data' : 'scientific_pi' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'access_level' ,
        'readOnly' : True
        } ,
    {
        'data' : 'seqiencing_site' ,
        'readOnly' : True
        } ,
    {
        'data' : 'pi_request_date' ,
        'readOnly' : True
        } ,
    {
        'data' : 'pipeline' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tissue_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'collaboration_center' ,
        'readOnly' : True
        } ,
    ]

adminColHeaders = ['IGO ID' , 'User Sample ID' , 'CMO Sample ID' , 'CMO Patient ID' , 'DMP Sample ID' ,
                    'DMP Patient ID' , 'MRN' , 'Sex' , 'Sample Type' , 'Sample Class' ,
                    'Tumor Type' , 'Parental Tumor Type' , 'Tumor Site' , 'Mol Accession #' , 'Collection Yr' ,
                    'Date DMP Request' , 'DMP Request ID' , 'IGO Request ID' , 'Date IGO Received' ,
                    'IGO Complete Date' , 'Application' , 'Baitset' , 'Sequencer' , 'Project Name' , 'Data Analyst' ,
                    'Lab Head' , 'CC/Fund' , 'Scientific PI' , 'Consent Part A' , 'Consent Part C' , 'Sample Status' ,
                    'Access Level' , 'Clinical Trial' , 'Sequencing Site' , 'PI Request Date' , 'Pipeline' ,
                    'Tissue Type' , 'Collaboration Center']
adminColumns = [
    {
        'data' : 'sampleid' ,
        'readOnly' : True ,
        'width' : 200
        } ,
    {
        'data' : 'user_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cmo_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cmo_patientid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_sampleid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_patientid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'mrn' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sex' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_class' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'parental_tumortype' ,
        'readOnly' : True
        } ,
    {
        'data' : 'tumor_site' ,
        'readOnly' : True
        } ,
    {
        'data' : 'molecular_accession_num' ,
        'readOnly' : True
        } ,
    {
        'data' : 'collection_year' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_dmp_request' ,
        'readOnly' : True
        } ,
    {
        'data' : 'dmp_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'igo_requestid' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_received' ,
        'readOnly' : True
        } ,
    {
        'data' : 'date_igo_complete' ,
        'readOnly' : True
        } ,
    {
        'data' : 'application_requested' ,
        'readOnly' : True
        } ,
    {
        'data' : 'baitset_used' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sequencer_type' ,
        'readOnly' : True
        } ,
    {
        'data' : 'project_title' ,
        'readOnly' : True
        } ,
    {
        'data' : 'data_analyst' ,
        } ,
    {
        'data' : 'lab_head' ,
        'readOnly' : True
        } ,
    {
        'data' : 'cc_fund' ,
        'readOnly' : True
        } ,
    {
        'data' : 'scientific_pi' ,
        } ,
    {
        'data' : 'consent_parta_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'consent_partc_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'sample_status' ,
        'readOnly' : True
        } ,
    {
        'data' : 'access_level' ,
        'editor' : 'select' ,
        'selectOptions' : ['PI restricted' , 'MSK public' , 'Published']
        } ,
    {
        'data' : 'clinical_trial' ,
        } ,
    {
        'data' : 'seqiencing_site' ,
        } ,
    {
        'data' : 'pi_request_date' ,
        } ,
    {
        'data' : 'pipeline' ,
        } ,
    {
        'data' : 'tissue_type' ,
        'editor' : 'select' ,
        'selectOptions' : ['cfDNA' , 'Tumor' , 'Normal']
        } ,
    {
        'data' : 'collaboration_center' ,
        } ,
    ]

settings = {
    'columnSorting': True ,
    'filters': True ,
    'autoColumnSize': True ,
    'width': '100%',
    'height': 500,
    'colWidths': [200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 ,
                   200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 , 200 ,
                   200 , 200 , 200 , 200, 200, 200, 200] ,
    'manualColumnResize' : True ,
    'rowHeaders': True,
    'colHeaders': True,
    'search': True,
    'dropdownMenu': ['filter_by_condition' , 'filter_action_bar'] ,
    }


########################################################################################################################################