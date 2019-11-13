
import React, { Component } from 'react';
import { Form, Icon, Input, Button, Select, Row, Col, Spin } from 'antd';
import { search_data } from '../actions/searchActions';
import { connect } from 'react-redux';
import DataGridEditTrackingInfo from '../components/dataGridEditTrackingInfo';
import { withRouter } from 'react-router';
import {ADMIN_EMAIL} from '../configs/react.configs';
import DevTools from '../components/devtools';

let styles = {
    notification_div: {
      color:'black',
      textAlign:'center',
      fontFamily: 'sans-serif',
      fontSize:15,
      margin :20,
    }
  }

class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'searchtext': '',
            'searchtype': '',
            'data': this.props.data
        }

    }

    componentDidMount() {
        if (!this.props.user || !this.props.user.access_token) {
            this.props.history.push("/");
        }
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            const data = {
                'searchtext': values.searchtext,
                'searchtype': values.searchtype,
                'role': this.props.user.role
            }
            if (!err) {
                this.props.searchData(data, this.props.user.access_token);
            }
        });
    };

    handleSearchTypeSelectChange = (value, name) => {
        this.setState({ [name]: value });
    }

    handleInputChange = (e) => {
        const fieldname = e.target.name;
        const value = e.target.value
        this.setState({ [fieldname]: value });
    }

    render() {
        const { getFieldDecorator } = this.props.form;
        return (
            <div>
                <Form layout="inline" onSubmit={this.handleSubmit} style={{ marginTop: 40, marginBottom: 20 }}>
                    <Row type='flex' justify="center">
                        <Col>
                            <Form.Item>
                                {getFieldDecorator('searchtext', {
                                    rules: [{ required: true, message: "Required MRN's or Tumor Type to search." }],
                                    onChange: this.handleInputChange
                                })(
                                    <Input
                                        prefix={<Icon type="search" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                        size="large"
                                        name="searchtext"
                                        placeholder="search using comma separated mrn's or tumor type"
                                        style={{ width: 450 }}
                                    />,
                                )}
                            </Form.Item>
                        </Col>
                        <Col>
                            <Form.Item>
                                {getFieldDecorator('searchtype', {
                                    rules: [{
                                        required: true, message: 'Please chose searchtype!',
                                    }],
                                    initialValue: "",
                                })(
                                    <Select placeholder="Search Type" size="large" style={{ minWidth: 150 }} onChange={(value) => this.handleSearchTypeSelectChange(value, 'searchtype')}>
                                        <Select.Option value="MRN">MRN</Select.Option>
                                        <Select.Option value="TUMOR TYPE">TUMOR TYPE</Select.Option>
                                        {this.props.user && this.props.user.role === 'admin' && <Select.Option value="DMPID">DMP ID</Select.Option>}
                                    </Select>
                                )}
                            </Form.Item>
                        </Col>
                        <Col>
                            <Form.Item>
                                <Button type="primary" size="large" htmlType="submit">
                                    <Icon type="search" />Search
                                </Button>
                            </Form.Item>
                        </Col>

                    </Row>

                </Form>
                {this.props.user && this.props.user.role === 'user' &&
                    <div style={styles.notification_div}>
                        You are logged in as a regular user. If you are clinician or an admin please email Admins group at '{ADMIN_EMAIL}'' to get access to data.
                    </div>
                }
                {this.props.isFetching ? <div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Loading..." size='large' /></div> :
                    this.props.data && <DataGridEditTrackingInfo rowdata={this.props.data}/>
                }
                <DevTools />
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
    searchData: (data, token) => dispatch(search_data(data, token))
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Form.create()(SearchForm)));
