import * as React from 'react';
import { 
        Grid, 
        Table, 
        Toolbar,
        SearchPanel,
        TableHeaderRow, 
        TableColumnResizing, 
        TableFilterRow,
        PagingPanel,
        TableFixedColumns,
        ColumnChooser,
        TableColumnVisibility,
        VirtualTable,} from '@devexpress/dx-react-grid-material-ui';
import {
        SortingState,
        IntegratedSorting,
        SearchState,
        IntegratedFiltering,
        FilteringState, 
        PagingState,
        IntegratedPaging, }from '@devexpress/dx-react-grid';


import { Paper, withStyles, Button } from '@material-ui/core';


//const getRowId = row => row.recordId;
const FilterIcon = ({ type, ...restProps }) => {
    if (type === 'month') return <DateRange {...restProps} />;
    return <TableFilterRow.Icon type={type} {...restProps} />;
  };

const styles = {
  customHeaderRow: {
    '& th': {
      whiteSpace: "normal",
      wordWrap: "break-word",
      border:"solid",
      backgroundColor:'#007CBA',
      borderWidth:'1px',
      borderCollapse: "collapse",
      borderColor:'grey',
      fontWeight:'bold',
      color:'white',
      fontSize:'12px'
    }
    /*your styles here*/
  },
  customTableRow: {
    '& td': {
      whiteSpace: "normal",
      wordWrap: "break-word",
      border:"solid",
      backgroundColor:'',
      borderWidth:'1px',
      borderCollapse: 'true',
      borderColor:'grey',
      fontSize:'12px'
    }
    /*your styles here*/
  }
 
 };


const CustomTableHeaderRowBase = ({ classes, ...restProps }) => {
//   restProps.value = restProps.row || restProps.row;
 return <TableHeaderRow.Row className={classes.customHeaderRow} {...restProps} />
}
export const CustomTableHeaderRow = withStyles(styles)(CustomTableHeaderRowBase);


const CustomTableRowBase = ({ classes, ...restProps }) => {
//   restProps.value = restProps.row || restProps.row;
 return <Table.Row className={classes.customTableRow} {...restProps} />
}
export const CustomTableRow = withStyles(styles)(CustomTableRowBase);

class DataGridTrackingInfo extends React.PureComponent {
    constructor(props) {
        super(props);
        this.state = {
        defaultColumnWidths: [
                {   columnName: 'sampleid',
                    width: 150
                },
                {
                    columnName: 'other_sampleid',
                    width: 200
                },
                {
                    columnName: 'corrected_cmo_id',
                    width: 200  
                },
                {
                    columnName: 'date_requested_from_dmp',
                    width: 200  
                },
                {
                    columnName: 'recipe_application',
                    width: 200  
                },
                {
                    columnName: 'associated_clinical_trial',
                    width: 200  
                },
                {
                    columnName: 'access_status',
                    width: 200  
                },
                {
                    columnName: 'payee',
                    width: 200  
                },
                {
                    columnName: 'cc_fund',
                    width: 200  
                },
                {
                    columnName: 'date_requested',
                    width: 200  
                },
                {
                    columnName: 'project_title',
                    width: 200  
                },
                {
                    columnName: 'date_pipeline_in',
                    width: 200  
                },
                {
                    columnName: 'date_pipeline_complete',
                    width: 200  
                },
                {
                    columnName: 'sequencing_location',
                    width: 200  
                },
                {
                    columnName: 'sequencer_type',
                    width: 200  
                },
                {
                    columnName: 'cbioportal_sampleid',
                    width: 200  
                },
                {
                    columnName: 'cbioportal_patientid',
                    width: 200  
                },
                {
                    columnName: 'date_portal_in',
                    width: 200  
                },
                {
                    columnName: 'pipeline_requested',
                    width: 200  
                },
                {
                    columnName: 'dmp_requestid',
                    width: 200  
                },
            ],
            columns : [
                {   title: 'IGO ID', 
                    name: 'sampleid', 
                },
                {
                    title: 'CMO Sample ID',
                    name: 'other_sampleid',
                },
                {
                    title: 'Corrected CMO ID',
                    name: 'corrected_cmo_id', 
                },
                {
                    title: 'Date DMP Requested',
                    name: 'date_requested_from_dmp', 
                },
                {
                    title: "DMP Request Id",
                    name: 'dmp_requestid', 
                },
                {
                    title: 'Recipe/Application',
                    name: 'recipe_application', 
                },
                {
                    title: 'Clinical Trial',
                    name: 'associated_clinical_trial', 
                },
                {
                    title: 'Data Access',
                    name: 'access_status', 
                },
                {
                    title: 'Payee' ,
                    name: 'payee', 
                },
                {
                    title: 'CC/Fund#',
                    name: 'cc_fund', 
                },
                {
                    title: 'Date Requested',
                    name: 'date_requested', 
                },
                {
                    title: 'Project Title',
                    name: 'project_title', 
                },
                {
                    title: "Date Pipeline Start",
                    name: 'date_pipeline_in', 
                },
                {
                    title: "Date Pipeline Complete",
                    name: 'date_pipeline_complete', 
                },
                {
                    title: 'Sequencing Site',
                    name: 'sequencing_location', 
                },
                {
                    title: 'Sequencer Type',
                    name: 'sequencer_type', 
                },
                {
                    title: 'cBio Portal SampleID',
                    name: 'cbioportal_sampleid', 
                },
                {
                    title: 'cBio Portal PatientID',
                    name: 'cbioportal_patientid', 
                },
                {
                    title: 'Date Portal In',
                    name: 'date_portal_in', 
                },
                {
                    title: "Pipeline Requested",
                    name: "pipeline_requested", 
                },
            ],
            rows : JSON.parse(this.props.rowdata),
            pageSizes: [25, 50, 100, 250, 500],

        }
    }

    toggleButton(props) {
        return (
            <Button color="primary" onClick={props.onToggle} buttonRef={props.buttonRef} style={{marginRight:'50px'}}>
                Show/Hide Columns 
            </Button>
        );
      }

  render() {
    const { rows, columns, defaultColumnWidths, pageSizes } = this.state;
    return (
        <div style={{marginTop:'25px', marginLeft:'15px', marginRight:'15px'}}>
        <Paper elevation={5}>
            <Grid
            rows={rows}
            columns={columns}>
            <SearchState defaultValue="" />
            <SortingState defaultSorting={[{ columnName: 'sampleId', direction: 'asc' }]}/>
            <IntegratedSorting />
            <FilteringState defaultFilters={[]} />
            <IntegratedFiltering/>
            <PagingState
                defaultCurrentPage={0}
                defaultPageSize={100}
            />
            <IntegratedPaging />
            <VirtualTable rowComponent={CustomTableRow}/>
            <div style ={{marginLeft:'25px', fontSize:"15px", fontWeight:'bold'}}>Search returned {rows.length} results</div>
            <TableColumnResizing defaultColumnWidths={defaultColumnWidths} />
            <TableHeaderRow rowComponent={CustomTableHeaderRow} showSortingControls/>
            <TableColumnVisibility/>
            <Toolbar/>
            <ColumnChooser toggleButtonComponent={this.toggleButton}/>
            <SearchPanel />
            <TableFilterRow showFilterSelector iconComponent={FilterIcon}/>
            <TableFixedColumns/>
            <PagingPanel pageSizes={pageSizes}/>
            </Grid>
        </Paper>
        </div>
    );
  }
}
// const mapStateToProps = state => ({
//     data: state.searchResult.data,
//     error: state.searchResult.error,
//     message:  state.searchResult.message
// });
// export default connect(mapStateToProps)(DataGridTrackingInfo);
export default DataGridTrackingInfo;
