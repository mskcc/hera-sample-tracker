import React, {Component} from 'react';
import Home from '../components/home';
import HeaderBarLoginPage from '../components/headerBarLoginPage';
import {withRouter} from 'react-router';
import {endsession} from '../actions/userActions';
import { connect } from 'react-redux';
import {BASE_ROUTE} from '../configs/react.configs';
import IdleTimer from 'react-idle-timer'

class HomeView extends Component{
    constructor(props){
        super(props);
        this.onIdle = this._onIdle.bind(this)
    }

    _onIdle(e) {
    console.log('user is idle', e);
    console.log('last active', this.idleTimer.getLastActiveTime());
    var config = {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': "Bearer " + this.props.user.access_token
        }
        };
    this.props.user && this.props.user.access_token && this.props.endsession(this.props.user, config, this.props.history);
    }

    componentWillMount(){
        console.log(this.props.user);
        !this.props.user && this.props.history.push(`${BASE_ROUTE}/`);
    }
    componentDidMount(){
        !this.props.user && this.props.history.push(`${BASE_ROUTE}/`);
    }

    render(){
        return(
            <div>
                <IdleTimer
                    ref={ref => { this.idleTimer = ref }}
                    element={document}
                    onIdle={this.onIdle}
                    debounce={250}
                    timeout={1000 * 60 * 15} />
                <HeaderBarLoginPage/>
                <Home/>
            </div>
        );
    }
}

const mapStateToProps = state => ({
    state: state,
    data: state.searchResult.data,
    isFetching: state.searchResult.isFetching,
    error: state.searchResult.error,
    message: state.searchResult.message,
    user: state.user.userData
});

const mapDispatchToProps = dispatch => ({
    endsession: (data, configs, token) => dispatch(endsession(data, configs, token))
});

export default withRouter(connect(mapStateToProps,mapDispatchToProps)(HomeView));
