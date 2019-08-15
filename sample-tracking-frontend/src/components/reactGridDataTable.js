import * as React from 'react';
import Paper from '@material-ui/core/Paper';
import * as PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
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
import {connect} from 'react-redux';
import { Col } from 'antd';

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

class ReactGridDataTable extends React.PureComponent {
    constructor(props) {
        super(props);
        this.state = {
        defaultColumnWidths: [
                {
                    columnName: 'sampleId', 
                    width: 150
                },
                {
                    columnName: 'otherSampleId',
                    width: 200
                },
                {
                    columnName: 'correctedCMOId',
                    width: 200
                    
                },
                {
                    columnName: 'mrn',
                    width: 150
                },
        
                {
                    columnName: 'accessionNumber',
                    width: 150
        
                },
                {
                    columnName: 'requestId',
                    width: 150
                    
                },
                {
                    columnName: 'pi',
                    width: 200
                    
                },
                {
                    columnName: 'tumorType',
                    width: 200
        
                },
                {
                    columnName: 'tumorSite',
                    width: 200
                },
                {
                    columnName: 'tissueLocation',
                    width: 200
                },
                {
                    columnName: 'cmoSampleClass',
                    width: 175
                    
                },
                {
                    columnName: 'oncoTreeCode',
                    width: 200
                    
                },
                {
                    columnName: 'accessStatus',
                    width: 200
                    
                },
                {
                    columnName: 'dataAvailabilityStatus',
                    width: 200
                
                },
                {
                    columnName: 'associatedClinicalTrial',
                    width: 200
                    
                },
                {
                    columnName: 'currentStatusIGO',
                    width: 200
                    
                },
                {
                    columnName: 'dateCreated',
                    width: 200
                    
                },
                {
                    columnName: 'dateIgoReceived',
                    width: 200
                    
                },
                {
                    columnName: 'dateIGOComplete',
                    width: 200
                    
                }
        ],
            columns : [
                {title: 'IGO ID', name: 'sampleId',
                },
                {
                    title: 'CMO Sample ID',
                    name: 'otherSampleId',
                },
                {
                    title: 'Corrected CMO ID',
                    name: 'correctedCMOId',
                    
                },
                {
                    title: 'MRN',
                    name: 'mrn',
                },
        
                {
                    title: 'Accession No',
                    name: 'accessionNumber',
                
                },
                {
                    title: 'IGO Request ID',
                    name:'requestId',
                    
                },
                {
                    title: 'PI',
                    name: 'pi',
                    
                },
                {
                    title: 'Tumor Type',
                    name: 'tumorType',
                    
        
                },
                {
                    title: 'Tumor Location',
                    name: 'tumorSite',
                },
                {
                    title: 'Tissue Location',
                    name: 'tissueLocation',
                },
                {
                    title: 'CMO Sample Class',
                    name: 'cmoSampleClass',
                    
                },
                {
                    title: 'Onco Tree Code',
                    name: 'oncoTreeCode',
                    
                },
                {
                    title: 'Data Access Status',
                    name: 'accessStatus',
                    
                },
                {
                    title: 'Data Available',
                    name: 'dataAvailabilityStatus',
                   
                },
                {
                    title: 'Clinical Trial',
                    name: 'associatedClinicalTrial',
                    
                },
                {
                    title: 'IGO Sample Status',
                    name: 'currentStatusIGO',
                    
                },
                {
                    title: 'Date Created',
                    name: 'dateCreated',
                    
                },
                {
                    title: 'Date IGO Received',
                    name: 'dateIgoReceived',
                    
                },
                {
                    title: 'Date IGO Complete',
                    name: 'dateIGOComplete',
                    
                }
            ],
            rows : JSON.parse(this.props.data),
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
const mapStateToProps = state => ({
    data: state.searchResult.data,
    error: state.searchResult.error,
    message:  state.searchResult.message
});
export default connect(mapStateToProps)(ReactGridDataTable);
