import React from 'react';
import { HotTable } from '@handsontable/react';
import { Paper } from '@material-ui/core';
import { Button, Spin, Modal, Icon } from 'antd';
import { save_changes } from '../actions/saveActions';
import { connect } from 'react-redux';
import '../styles/styles.css';
import { column_mappings } from '../configs/download-data-mappings';
import FileSaver from "file-saver";
import XLSX from "xlsx";
import axios from 'axios';
import {BASE_URL} from '../configs/react.configs';


let styles = {
  button: {
    margin: 15,
  },
  disclaimer:{
    fontSize: '25px',
    textAlign:'center'
  },
  icon:{
    fontSize: '25px', 
    color: 'orange', 
    marginRight:'30px' 
  },
}

class DataGridEditTrackingInfo extends React.Component {
  constructor(props) {
    super(props);
    this.tabledata = this.props.rowdata;
    this.state = {
      isSaveButtonDisabled: true,
      tableData: JSON.parse(this.props.rowdata.data),
      colHeaders: this.props.rowdata.colHeaders,
      columnDef: this.props.rowdata.columns,
      settings: this.props.rowdata.settings,
      searchtext: this.props.searchtext,
      searchtype: this.props.searchtype,
      role: this.props.role,
      confirmVisible: false,
    }
    this.downloadData = this.downloadData.bind(this);
  }

  setGridHeight(data) {
    if (data.length <= 50) {
      return (data.length * 25) + 50;
    }
    return 900;
  }

  saveChanges = () => {
    this.props.save_changes(this.state.tableData, this.props.user.access_token);
    this.setState({ isSaveButtonDisabled: true });
  }

  downloadData = () => {
    this.setState({confirmVisible:false});
    const dataArray = [];
    const headers = this.state.colHeaders;
    dataArray.push(headers);
    this.state.tableData.forEach((row) => {
      var arr = [];
      headers.forEach((value) => {
        arr.push(row[column_mappings[value]]);
      })
      dataArray.push(arr);
    });
    const fileExtension = ".xlsx";
    const fileType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8';
    const today = new Date();
    const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    const fileName = `Data-${date}`;
    const ws = XLSX.utils.json_to_sheet(dataArray, { skipHeader: true });
    const wb = { Sheets: { data: ws }, SheetNames: ["data"] };
    const excelBuffer = XLSX.write(wb, {
      bookType: "xlsx",
      type: "array"
    });
    const data = new Blob([excelBuffer], { type: fileType });
    FileSaver.saveAs(data, fileName + fileExtension);

    const post_data = {
      user: this.props.user,
      data_length: this.state.tableData.length,
    }

    const token = this.props.user.access_token;
    var config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': "Bearer " + token
      }
    };
    axios.post(BASE_URL + "download_data",post_data, config)
        .then(res => {
          if (res.data.success){
            console.log("download logged successfully.")
          }
          if (!res.data.success){
            console.log("download logging failed.")
          }
        })
        .catch(err => {
          console.log(err);
        });
  }

  handleCancel = () => {
    this.setState({ confirmVisible: false });
  }

  handleDownload = () => {
    this.setState({ confirmVisible: true });
  }

  handleEdit = (changes, source) => {
    if (changes) {
      this.setState({ isSaveButtonDisabled: false });
    }
  }

  render() {
    const disclaimerText = 'The information contained in this transmission from Memorial Sloan-Kettering Cancer Center is privileged, confidential and protected health information (PHI) and it is protected from disclosure under applicable law, ' +
      'including the Health Insurance Portability and Accountability Act of 1996, as amended (HIPAA).  This transmission is intended for the sole use of approved individuals with permission and training to access this information and PHI. ' +
      'If you are not the intended recipient, please CANCEL this transmission. You are notified that all the transmissions and other activities from this site are logged and closely monitored.  If you have received this transmission in error, ' +
      'please immediately delete this information and any attachments from any computer.';

    return (
      <div style={{ height: '100%', margin: '15px', alignContent: 'center' }}>
        {this.props.savedata.isFetching ? <div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Saving data..." size='large' /></div> :
          <Paper>
            <div>
              {this.props.user && this.props.user.role === 'admin' &&
                <Button type="primary" disabled={this.state.isSaveButtonDisabled} icon="cloud" style={styles.button} onClick={() => this.saveChanges()}>Save Changes</Button>
              }
              <Button type="primary" icon="download" style={styles.button} onClick={() => this.handleDownload()}>Download Data</Button>
            </div>
            <HotTable
              className="handsontable handsontablerow"
              data={this.state.tableData}
              colHeaders={this.state.colHeaders}
              columns={this.state.columnDef}
              settings={this.state.settings}
              afterChange={(changes, source) => this.handleEdit(changes, source)}
              stretchH='all'
              licenseKey="non-commercial-and-evaluation"
              height={this.setGridHeight(this.state.tableData)}
              wordWrap={false}
              autoRowSize={false}
              search={true}
              currentRowClassName='currentRow'
              currentColClassName='currentCol'
            />
          </Paper>
        }
        <Modal
          title={<div style={styles.disclaimer}><Icon type="warning" style={styles.icon} theme="outlined"/>Disclaimer</div>}                     
          visible={this.state.confirmVisible}
          onOk={this.downloadData}
          onCancel={this.handleCancel}
          width='30%'
        >
          <p>{disclaimerText}</p>
        </Modal>
      </div>
    );
  }
}
const mapStateToProps = state => ({
  user: state.user.userData,
  data: state.searchResult.data,
  savedata: state.saveResult
});

const mapDispatchToProps = dispatch => ({
  save_changes: (data, token) => dispatch(save_changes(data, token))
});

export default connect(mapStateToProps, mapDispatchToProps)(DataGridEditTrackingInfo);