import React, {Component} from 'react';
import Navigation from '../components/navigation';
import {withRouter} from 'react-router-dom';
import Home from '../components/home';

class HomeView extends React.Component{
    render(){
        return(
            <Home/>
        );
    }
}
export default HomeView;
