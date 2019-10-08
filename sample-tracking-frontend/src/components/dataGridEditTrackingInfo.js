import React from 'react';
import { HotTable } from '@handsontable/react';
import { Paper, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


let styles = {
  button: {
    backgroundColor: '#C24D00',
    margin: 15
  }
}


class DataGridEditTrackingInfo extends React.Component {
  constructor(props) {
    super(props);
    this.data=this.props.rowdata;
    this.gridData = JSON.parse(this.data.data);
  }

  setGridHeight(data){
    return (data.length * 24)+24;
  }

  render() {
    return (
      <div style={{height:'100%', marginTop:'15px', marginLeft:'15px', marginRight:'15px', alignContent:'center'}}>
            <Paper>
            <div>
              <Button variant="contained" color='primary' style = {styles.button} >Save Changes</Button>
            </div>
                <HotTable
                    data = {this.gridData}
                    colHeaders={this.data.colHeaders}
                    columns={this.data.columns}
                    settings={this.data.settings}
                    stretchH= 'all'
                    licenseKey = "non-commercial-and-evaluation"
                    height={this.setGridHeight(this.gridData)}
                />
            </Paper>
            
      </div>
    );
  }
}

// const mapStateToProps = state => ({
//   data: state.searchResult.data,
//   colHeaders: state.searchResult.colHeaders,
//   columns: state.searchResults.columns,
//   settings: state.searchResult.settings,
//   isFetching:state.searchResult.isFetching,
//   error: state.searchResult.error,
//   message:  state.searchResult.message,
//   user : state.user.userData
// });

export default DataGridEditTrackingInfo;