import React from 'react';
import { HotTable } from '@handsontable/react';
import { Paper, Button } from '@material-ui/core';
import { save_changes } from '../actions/saveActions';
import { connect } from 'react-redux';
// import MySnackbar from '../components/MySnackbar';
import '../styles/styles.css';
// import CustomizedSnackbars from '../components/MySnackbar';


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
    this.state = {
      cancel:0,
    }
  }

  setGridHeight(data){
    if (data.length <= 50){
      return (data.length * 25)+25;
    }
    return 700;
  }
  saveChanges = () =>{
    console.log(this.gridData);
    this.props.save_changes(this.gridData, this.props.user.access_token);
  }

  cancelChanges = () => {
    this.data=this.props.rowdata;
    this.gridData = JSON.parse(this.data.data);
    this.forceUpdate();
    
  }

  render() {
    return (
      <div style={{height:'100%', marginTop:'15px', marginLeft:'15px', marginRight:'15px', alignContent:'center'}}>
            <Paper>

            <div>
              <Button variant="contained" color='primary' style = {styles.button} onClick= {() => this.saveChanges()}>Save Changes</Button>
              <Button variant="contained" color='primary' style = {styles.button} onClick= {() => this.cancelChanges()}>Cancel Changes</Button>
            </div>
                <HotTable
                    className="handsontable handsontablerow"
                    data = {this.gridData}
                    colHeaders={this.data.colHeaders}
                    columns={this.data.columns}
                    settings={this.data.settings}
                    stretchH= 'all'
                    licenseKey = "non-commercial-and-evaluation"
                    height={this.setGridHeight(this.gridData)}
                    wordWrap={false}
                    autoRowSize={false}
                />
            </Paper>
            
            {/* <CustomizedSnackbars variant="success" message = "testing"/> */}
      </div>
    );
  }
}
const mapStateToProps = state => ({
  user: state.user.userData,
  save_results: state.saveResult
});

const mapDispatchToProps = dispatch => ({
  save_changes: (data, token) => dispatch(save_changes(data, token))
});

export default connect(mapStateToProps, mapDispatchToProps)(DataGridEditTrackingInfo);