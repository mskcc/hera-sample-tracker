import React, {Component} from 'react';
import {connect} from 'react-redux';
import DataTable from 'react-data-table-component';

class DataTableTest extends Component {



render() {
    const data = JSON.parse(this.props.data);
    console.log(data);
    const rowTheme = {
        rows: {
          borderColor: 'rgba(0,0,0,.12)',
          backgroundColor: 'white',
        },
        header: {
            fontSize: '12px',
            fontColor: 'white',
            backgroundColor: '#007CBA',
          },
        cells: {
            cellPadding: '48px',
            borderStyle:'solid',
            borderColor:'grey',

        },
      };

      const paginationOptions=[10,25, 50, 100, 250, 500]
      
      const columns = [
        {
            name: 'Sample ID',
            selector: 'sampleId',
            sortable: true,
            width:'200px'
        },
        {
            name: 'CMO Sample ID',
            selector: 'otherSampleId',
            sortable: true,
            wrap:true,
            width:'200px'
        },
        {
            name: 'Corrected CMO ID',
            selector: 'correctedCMOId',
            sortable: true,
            width:'200px',
            wrap:true
        },
        {
            name: 'MRN',
            selector: 'mrn',
            sortable: true,
            width:'200px',
            wrap:true
        },

        {
            name: 'Accession No',
            selector: 'accessionNumber',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'IGO Request ID',
            selector:'requestId',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'PI',
            selector: 'pi',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Tumor Type',
            selector: 'tumorType',
            sortable:true,
            width:'200px',
            wrap:true

        },
        {
            name: 'Tumor Location',
            selector: 'tumorSite',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Tissue Location',
            selector: 'tissueLocation',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'CMO Sample Class',
            selector: 'cmoSampleClass',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Onco Tree Code',
            selector: 'oncoTreeCode',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Data Access Status',
            selector: 'accessStatus',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Data Available',
            selector: 'dataAvailabilityStatus',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Clinical Trial',
            selector: 'associatedClinicalTrial',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'IGO Sample Status',
            selector: 'currentStatusIGO',
            sortable:true,
            wrap:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Date Created',
            selector: 'dateCreated',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Date IGO Received',
            selector: 'dateIgoReceived',
            sortable:true,
            width:'200px',
            wrap:true
        },
        {
            name: 'Date IGO Complete',
            selector: 'dateIGOComplete',
            sortable:true,
            width:'200px',
            wrap:true
        }
    ];

    return(
        <div style={{margin:'10px'}}>
        <DataTable
            title="Search Results"
            columns={columns}
            data={data}
            customTheme={rowTheme}
            keyField='recordId'
            responsive={true}
            pagination={true}
            paginationRowsPerPageOptions={paginationOptions}
        />
        </div>
        
    );
}
}
    const mapStateToProps = state => ({
        data: state.searchResult.data,
        error: state.searchResult.error,
        message:  state.searchResult.message
    });
export default connect(mapStateToProps)(DataTableTest);


