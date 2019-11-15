import React, {Component} from 'react';
import {Row, Col} from 'antd';
import {Button} from 'antd';
import mskcc_logo from '../assets/mskcc_logo.png';
import { connect } from 'react-redux';
import {withRouter} from 'react-router';
import {logout} from '../actions/userActions';

class HeaderBarLoginPage extends Component{

  logout = (user) =>{
    var config = {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Authorization': "Bearer " + this.props.user.access_token
      }
    };
    this.props.logout(user, config, this.props.history);
  };
    
    render(){
        return(
            <div>
            <Row  style = {{backgroundColor:'#007CBA', maxHeight:65, overflow:'hidden'}}>
              <Col span={10}>
                <div>
                    <img alt="example" src= {mskcc_logo} style={{maxHeight:65}}/>
                </div>
              </Col>
              <Col span={10} style={{padding:'auto', color:'white', fontSize:35, fontFamily:'sans-serif', overflow:'hidden'}}>
                Sample Tracker
              </Col>
              <Col span={4} style={{padding:'auto', color:'black', fontSize:35, fontFamily:'sans-serif'}}>
                {this.props.user && this.props.user.username ?
                <Button ghost icon="logout" onClick={()=> this.logout()}>LOG OUT</Button> : null}
              </Col> 
            </Row>
          </div>
        );
    }
}
const mapStateToProps = state => ({
    user: state.user.userData
});

const mapDispatchToProps = dispatch => ({
    logout: (data, config, history) => dispatch(logout(data, config, history))
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(HeaderBarLoginPage));