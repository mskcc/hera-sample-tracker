import React, {Component} from 'react';
import DataGridEditTrackingInfo from './dataGridEditTrackingInfo';

class DataTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'data':this.props.data,
        }
    }

    render() {
        return(
            <div>
                <DataGridEditTrackingInfo rowdata = {this.state.data}/>
            </div>
        );
    }
    }
    export default DataTable;


