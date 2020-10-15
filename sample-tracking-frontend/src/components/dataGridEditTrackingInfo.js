import React from 'react';
import { HotTable } from '@handsontable/react';
import { Paper } from '@material-ui/core';
import { Button, Spin, Modal, Icon, Input } from 'antd';
import { save_changes } from '../actions/saveActions';
import { connect } from 'react-redux';
import '../styles/styles.css';
import { column_mappings } from '../configs/download-data-mappings';
import FileSaver from "file-saver";
import XLSX from "xlsx";
import axios from 'axios';
import { BASE_URL } from '../configs/react.configs';


let styles = {
  button: {
    margin: 15,
  },
  disclaimer: {
    fontSize: '25px',
    textAlign: 'center'
  },
  icon: {
    fontSize: '25px',
    color: 'orange',
    marginRight: '30px'
  },
  searchbox: {
    marginLeft: '20px',
    width: 200
  }
  ,
  searchresults: {
    marginLeft: '20px',
    color: 'black',
  },
  handsontable: {
    paddingBottom: 20,
  }
}

const { Search } = Input;

class DataGridEditTrackingInfo extends React.Component {
  constructor(props) {
    super(props);
    this.tabledata = this.props.rowdata;
    this.state = {
      isSaveButtonDisabled: true,
      searchData: JSON.parse(this.props.rowdata.data),
      tableData: JSON.parse(this.props.rowdata.data),
      colHeaders: this.props.rowdata.colHeaders,
      columnDef: this.props.rowdata.columns,
      settings: this.props.rowdata.settings,
      searchtext: this.props.searchtext,
      searchtype: this.props.searchtype,
      role: this.props.role,
      confirmVisible: false,
      spareRowAdded: false,
      dataRowsEdited: new Set(),
    }
    
    this.downloadData = this.downloadData.bind(this);
  }

  setGridHeight(data) {
    return window.innerHeight * 0.65;
  }

  handleDownload = () => {
    this.setState({ confirmVisible: true });
  }

  //When a row cell is edited add the id of that row object to state in a Set(). We will use this Set object to filter data rows to save to DB to make save operation faster.
  handleEdit = (changes, source) => {
    // eslint-disable-next-line array-callback-return
    changes && changes.map((change) => {
      this.setState({dataRowsEdited:new Set([...this.state.dataRowsEdited, this.state.tableData[change[0]].id])});
      this.setState({ isSaveButtonDisabled: false });
    })
  }

  //First filter the table for only rows that were edited and needs to be saved. Save the filtered rows.
  saveChanges = () => {
    const rowsToSave = this.state.tableData.filter((item)=> {
      return this.state.dataRowsEdited.has(item.id);
    });
    this.props.save_changes(rowsToSave, this.props.user.access_token);
    this.setState({ isSaveButtonDisabled: true });
  }

  handleCancel = () =>{
    this.setState({confirmVisible:false});
  }

  downloadData = () => {
    this.setState({ confirmVisible: false });
    console.log(column_mappings);
    const dataArray = [];
    const headers = this.state.colHeaders;
    dataArray.push(headers);
    console.log(headers);
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
    axios.post(BASE_URL + "download_data", post_data, config)
      .then(res => {
        if (res.data.success) {
          console.log("download logged successfully.")
        }
        if (!res.data.success) {
          console.log("download logging failed.")
        }
      })
      .catch(err => {
        console.log(err);
      });
  }

  filterResults = (e) => {
    let searchtext = e.target.value;
    if (searchtext) {
      const data = this.state.searchData.filter((item) => {
        return Object.values(item).map((value) => {
          return String(value).toLowerCase();
        }).find((value) => {
          return value && value.includes(searchtext.toLowerCase());
        });
      });
      this.setState({ tableData: data });
    }
    else {
      this.setState({ tableData: this.state.searchData });
    }
  }

  render() {
    const disclaimerText = 'The information contained in this transmission from Memorial Sloan-Kettering Cancer Center is privileged, confidential and protected health information (PHI) and it is protected from disclosure under applicable law, ' +
      'including the Health Insurance Portability and Accountability Act of 1996, as amended (HIPAA).  This transmission is intended for the sole use of approved individuals with permission and training to access this information and PHI. ' +
      'If you are not the intended recipient, please CANCEL this transmission. You are notified that all the transmissions and other activities from this site are logged and closely monitored.  If you have received this transmission in error, ' +
      'please immediately delete this information and any attachments from any computer.';
    
      const data = this.state.tableData;

    return (
      <div style={{ height: '100%', margin: '15px', alignContent: 'center' }}>
        {this.props.savedata.isFetching ? <div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Saving data..." size='large' /></div> :
          <Paper>
            <div>
              {this.props.user && this.props.user.role === 'admin' &&
                <Button type="primary" disabled={this.state.isSaveButtonDisabled} icon="cloud" style={styles.button} onClick={() => this.saveChanges()}>Save Changes</Button>
              }
              <Button type="primary" icon="download" style={styles.button} onClick={() => this.handleDownload()}>Download Data</Button>
              <Search
                placeholder="find in table"
                //onSearch={value => console.log(value)}
                onChange={e => this.filterResults(e)}
                style={styles.searchbox}
              />

              <span style={styles.searchresults}> found {this.state.tableData.length} rows</span>
            </div>
            <div style={styles.handsontable}>
              <HotTable
                className="handsontable"
                data={data}
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
            </div>
          </Paper>
        }
        <Modal
          title={<div style={styles.disclaimer}><Icon type="warning" style={styles.icon} theme="outlined" />Disclaimer</div>}
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