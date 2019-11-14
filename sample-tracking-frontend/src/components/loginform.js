import React, {Component} from 'react';
import { Form, Icon, Input, Button, Row, Alert,Card} from 'antd';
import {login} from '../actions/userActions';
import {connect} from 'react-redux';
import {withRouter} from 'react-router';

class LoginForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
    
    }
  }
  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err){
        this.props.login(values, this.props.history);
    }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <Row type = "flex" justify="space-around">
        <Card style={{ width:400, margin:100}}>
        
        {/* If the user credentials are not valid show the validation error message */}
        {this.props.data !=null && !this.props.data.valid && 
          <Alert message={this.props.error} type="error" showIcon style={{marginBottom:10}}/>
        }
        {/* Validation error message end*/}

          <Form onSubmit={this.handleSubmit} className="login-form">
            <Form.Item>
              {getFieldDecorator('username', {
                rules: [{ required: true, message: 'Please input your username!' }],
              })(
                <Input
                  name="username" prefix={<Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />}
                  placeholder="Username"
                />,
              )}
            </Form.Item>
            <Form.Item>
              {getFieldDecorator('password', {
                rules: [{ required: true, message: 'Please input your Password!' }],
              })(
                <Input
                  name= "password" prefix={<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />}
                  type="password"
                  placeholder="Password"
                />,
              )}
            </Form.Item>
            <Form.Item>
              <Row type="flex" justify="space-around">
                <Button type="primary" shape="round" icon="login" htmlType="submit" className="login-form-button">
                  Log in
                </Button>
              </Row>
            </Form.Item>
          </Form>
      </Card>
      </Row>
    );
  }
}

const mapStateToProps = state => {
  return {
    data: state.user.userData,
    error: state.user.error
  }
};

const mapDispatchToProps = (dispatch) => {
  return{
    login: (username, password, history) => dispatch(login(username, password, history))
  }
};

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Form.create()(LoginForm)));
