import React from 'react';
import { HotTable } from '@handsontable/react';
import Handsontable from 'handsontable';
import { Paper } from '@material-ui/core';

class DataGridEditTrackingInfo extends React.Component {
  constructor(props) {
    super(props);
    this.data = this.jsonToArray(this.props.rowdata);
    this.headers = ["Hello", "How","are", "you","by"];
  }
  
  jsonToArray(jsonData){
      var jData = JSON.parse(jsonData);
      console.log(jData);
      var gridData = [];
      var sampledata = [];
    for (var i = 0; i < jData.length; i++){
        sampledata.push(jData[i]["sampleid"]);
        sampledata.push(jData[i]["other_sampleid"]);
        sampledata.push(jData[i]["pi"]);
        sampledata.push(jData[i]["request_id"]);
        sampledata.push(jData[i]["date_igo_complete"]);
        gridData.push(sampledata);
        sampledata = [];
        
    }
    return gridData;
  }

  setGridHeight(data){
    return (data.length * 24)+24;
  }

  render() {
    console.log(this.data);
    return (
      <div style={{height:'100%', marginTop:'15px', marginLeft:'15px', marginRight:'15px', alignContent:'center'}}>
            <Paper>
                <HotTable
                    data = {this.data}
                    colHeaders={this.headers}
                    stretchH= 'all'
                    licenseKey = "non-commercial-and-evaluation"
                    height={this.setGridHeight(this.data)}
                />
            </Paper>
      </div>
    );
  }
}

export default DataGridEditTrackingInfo;