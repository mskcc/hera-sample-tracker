import React, {Component} from 'react';
import Navigation from '../components/navigation';
import {withRouter} from 'react-router-dom';
import Home from '../components/home';
import HeaderBarLoginPage from '../components/headerBarLoginPage';

class HomeView extends React.Component{
    render(){
        return(
            <div>
            <HeaderBarLoginPage/>
            <Home/>
            </div>
        );
    }
}
export default HomeView;
