
import React, { Component } from 'react';
import { Form, Icon, Input, Button, Select, Row, Col, Spin } from 'antd';
import { search_data } from '../actions/mainActions';
import { connect } from 'react-redux';
import DataTable from '../components/datatable';
import DevTools from '../components/devtools';


class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'searchtext': '',
            'searchtype': '',
            'data': this.props.data
        }
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.searchData(values, this.props.user.access_token);
                console.log(this.props.data);
                console.log(values);
                //console.log(Object.entries(this.props.data));
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
                {this.props.isFetching ? <div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Loading..." size='large' /></div> :
                    this.props.data && <DataTable data={this.props.data} />
                }
                {/* <DevTools/> */}
            </div>
        );
    }
}
const mapStateToProps = state => ({
    data: state.searchResult.data,
    isFetching: state.searchResult.isFetching,
    error: state.searchResult.error,
    message: state.searchResult.message,
    user: state.user.userData
});

const mapDispatchToProps = dispatch => ({
    searchData: (searchtext, searchtype) => dispatch(search_data(searchtext, searchtype))
});

export default connect(mapStateToProps, mapDispatchToProps)(Form.create()(SearchForm));
