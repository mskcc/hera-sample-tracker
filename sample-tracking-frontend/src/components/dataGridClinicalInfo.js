import * as React from 'react';
import * as PropTypes from 'prop-types';
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

class DataGridClinicalInfo extends React.Component {
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
                    columnName: 'sample_type',
                    width: 150
                },
                {
                    columnName: 'tumor_type', 
                    width: 150
                },
                {
                    columnName: 'sample_class', 
                    width: 200
                },
                {
                    columnName: 'tumor_site',
                    width : 200
                },
                {
                    columnName: 'tissue_location', 
                    width: 200
                },
                {
                    columnName: 'sex', 
                    width: 150
                },
                {
                    columnName: 'mrn',
                    width: 150 
                },
                {
                    columnName: 'surgical_accession_number', 
                    width: 200
                },
                {
                    columnName: 'm_accession_number', 
                    width: 200
                },
                {
                    columnName: 'oncotree_code', 
                    width: 150
                },
                {
                    columnName: 'parental_tumortype', 
                    width: 200
                },
                {
                    columnName: 'collection_year', 
                    width: 150
                },
                {
                    columnName: 'dmp_sampleid', 
                    width: 150
                },
                {
                    columnName: 'dmp_patientid', 
                    width: 150
                },
                {
                    columnName: 'registration_12_245AC', 
                    width: 200
                },
                {
                    columnName: 'vaf', 
                    width : 100
                },
                {
                    columnName: 'facets', 
                    width: 100
                }
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
                    title: 'Sample Type',
                    name: 'sample_type', 
                },
                {
                    title: 'Tumor Type',
                    name: 'tumor_type', 
                },
                {
                    title: 'Sample Class',
                    name: 'sample_class', 
                },
                {
                    title: 'Tumor Site',
                    name: 'tumor_site', 
                },
                {
                    title: 'Tissue Location',
                    name: 'tissue_location', 
                },
                {
                    title: 'Sex',
                    name: 'sex', 
                },
                {
                    title: 'MRN',
                    name: 'mrn', 
                },
                {
                    title: 'Surgical Accession No.',
                    name: 'surgical_accession_number', 
                },
                {
                    title: 'M Accession No',
                    name: 'm_accession_number', 
                },
                {
                    title: 'Oncotree Code',
                    name: 'oncotree_code', 
                },
                {
                    title: 'Parental Tumor Type',
                    name: 'parental_tumortype', 
                },
                {
                    title: 'Collection Year',
                    name: 'collection_year', 
                },
                {
                    title: 'DMP Sample ID',
                    name: 'dmp_sampleid', 
                },
                {
                    title: 'DMP Patient ID',
                    name: 'dmp_patientid', 
                },
                {
                    title: 'Registration 12-245AC',
                    name: 'registration_12_245AC', 
                },
                {
                    title: 'VAF',
                    name: 'vaf', 
                },
                {
                    title: 'Facets',
                    name: 'facets', 
                }
                
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
export default DataGridClinicalInfo;
