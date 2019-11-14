import React, {Component} from 'react';
import { Row, Menu, Icon } from 'antd';

export default class Navigation extends Component {
  state = {
    current: 'home',
  };

  handleClick = e => {
    console.log('click ', e);
    this.setState({
      current: e.key,
    });
  };

  render() {
    return (
        <Row type="flex" justify="space-around">
        <Menu onClick={this.handleClick} selectedKeys={[this.state.current]} mode="horizontal" >
            <Menu.Item key="home" style = {{marginLeft:10, marginRight:10}}>
                <Icon type="home" />
                    Hera Home
            </Menu.Item>
            <Menu.Item key="samples" style = {{marginLeft:10, marginRight:10}}>
                <Icon type="appstore" />
                    Samples
            </Menu.Item>
            <Menu.Item key = "dashboard" style = {{marginLeft:10, marginRight:10}}>
                <Icon type="dashboard" />
                    dashboard
            </Menu.Item>
            <Menu.Item key="status" style = {{marginLeft:10, marginRight:10}}>
                <Icon type="question-circle" />
                    Status
            </Menu.Item>
        </Menu>
        </Row>
    );
  }
}
