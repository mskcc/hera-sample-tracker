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

class DataGridSampleInfo extends React.PureComponent {
    constructor(props) {
        super(props);
        console.log(this.props.rowdata.columns);
        console.log(this.props.rowdata.colHeaders);
        console.log(this.props.rowdata.settings);
        this.state = {
        defaultColumnWidths: [
                {
                    columnName: 'sampleid',
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
                    columnName: 'request_id',
                    width: 150
                },
                {
                    columnName: 'pi',
                    width: 200
                },
                {
                    columnName: 'tumor_type',
                    width: 200
                },
                {
                    columnName: 'parental_tumortype',
                    width: 200
                },
                {
                    columnName: 'sample_type',
                    width: 150
                },
                {
                    columnName: 'tumor_site',
                    width: 200
                },
                {
                    columnName: 'tissue_location',
                    width: 200
                },
                {
                    columnName: 'sample_class',
                    width: 175 
                },
                {
                    columnName: 'igo_sample_status',
                    width: 200   
                },
                {
                    columnName: 'date_created',
                    width: 200  
                },
                {
                    columnName: 'date_igo_received',
                    width: 200  
                },
                {
                    columnName: 'date_igo_complete',
                    width: 200  
                }
        ],
            nonPhiColumns : [
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
                    title: 'IGO Request ID',
                    name:'request_id', 
                },
                {
                    title: 'PI',
                    name: 'pi',   
                },
                {
                    title: 'Tumor Type',
                    name: 'tumor_type',
                },
                {
                    title: 'Parental Tumor Type',
                    name: 'parental_tumortype'
                },
                {
                    title:'Sample Type',
                    name: 'sample_type'
                },
                {
                    title: 'Tumor Location',
                    name: 'tumor_site',
                },
                {
                    title: 'Tissue Location',
                    name: 'tissue_location',
                },
                {
                    title: 'CMO Sample Class',
                    name: 'sample_class',   
                },
                {
                    title: 'IGO Sample Status',
                    name: 'igo_sample_status',    
                },
                {
                    title: 'Date Created',
                    name: 'date_created',    
                },
                {
                    title: 'Date IGO Received',
                    name: 'date_igo_received',    
                },
                {
                    title: 'Date IGO Complete',
                    name: 'date_igo_complete',    
                }
            ],
            rows : JSON.parse(this.props.rowdata.data),
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
    const { rows, nonPhiColumns, defaultColumnWidths, pageSizes } = this.state;
    return (
        <div style={{marginTop:'40px', marginLeft:'15px', marginRight:'15px'}}>
            <Paper elevation={5}>
                <Grid
                rows={rows}
                columns={nonPhiColumns}>
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

export default DataGridSampleInfo;
