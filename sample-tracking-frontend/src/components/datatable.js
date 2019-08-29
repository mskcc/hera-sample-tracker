import React, {Component} from 'react';
import { Tabs } from 'antd';
import DataGridTrackingInfo from './dataGridTrackingInfo';
import DataGridSampleInfo from './dataGridSampleInfo';
import DataGridClinicalInfo from './dataGridClinicalInfo';
import DataGridEditTrackingInfo from './dataGridEditTrackingInfo';

const { TabPane } = Tabs;

function callback(key) {
  sessionStorage.setItem('activeTab', key);
}



class DataTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'data':this.props.data,
            'activeTab': this.getActiveTab
        }
    }

    setActiveTab = (key) => {
        console.log(key);
    }

    render() {
        console.log(this.getActiveTab);
        return(
            <div>
                <Tabs defaultActiveKey="1" onChange={this.setActiveTab} type="card">
                    <TabPane tab="Sample Info" key="1" >
                        <DataGridSampleInfo rowdata = {this.state.data}/>
                    </TabPane>
                    <TabPane tab="Clinical Info" key="2">
                        <DataGridClinicalInfo rowdata = {this.state.data}/>
                    </TabPane>
                    <TabPane tab="Tracking Info" key="3">
                        <DataGridTrackingInfo rowdata = {this.state.data}/>
                    </TabPane>
                    <TabPane tab = "Edit Info" key="4">
                        <DataGridEditTrackingInfo rowdata = {this.state.data}/>
                    </TabPane>
                </Tabs>
                {/* <DataGridEditTrackingInfo rowdata = {this.state.data}/> */}
            </div>
        );
    }
    }
    export default DataTable;


