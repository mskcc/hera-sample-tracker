import React, {Component} from 'react';
// import Navigation from '../components/navigation';
import HeaderBarLoginPage from '../components/headerBarLoginPage';
import LoginForm from '../components/loginform';
import {withRouter} from 'react-router-dom';

class LoginView extends Component{
    render(){
        return(
            <div>
                <HeaderBarLoginPage/>
                <LoginForm/>
            </div>
        );
    }
}

export default withRouter(LoginView);
