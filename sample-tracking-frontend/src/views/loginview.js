import React, {Component} from 'react';
// import Navigation from '../components/navigation';
import HeaderBarLoginPage from '../components/headerBarLoginPage';
import LoginForm from '../components/loginform';
import {withRouter} from 'react-router-dom';
import DevTools from '../components/devtools';

class LoginView extends Component{
    render(){
        return(
            <div>
                <HeaderBarLoginPage/>
                <LoginForm/>
                {/* <DevTools/> */}
            </div>
        );
    }
}

export default withRouter(LoginView);
