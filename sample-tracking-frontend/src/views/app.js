import React, {Component} from 'react';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import LoginView from './loginview';
import HomeView from '../views/homeview';
import DataGridEditTrackingInfo from '../components/dataGridEditTrackingInfo';

class App extends Component{
    render(){
        return(
            <Router>
                <Switch>
                    <Route path='/' exact component={LoginView} />
                    <Route path='/home' exact component={HomeView}/>
                </Switch>
            </Router>
        );
    }
}
export default App;