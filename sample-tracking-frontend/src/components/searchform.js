
import React, { Component } from 'react';
import { Form, Icon, Input, Button, Select, Checkbox, Row, Col, Spin, Typography} from 'antd';
import { search_data } from '../actions/searchActions';
import { connect } from 'react-redux';
import DataGridEditTrackingInfo from '../components/dataGridEditTrackingInfo';
import { withRouter } from 'react-router';
import { ADMIN_EMAIL } from '../configs/react.configs';
// import DevTools from '../components/devtools';

let styles = {
    notification_div: {
        color: 'blue',
    }
}
const {Text} = Typography;
class SearchForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'searchtext': '',
            'searchtype': '',
            'exactmatch': false,
            'data': this.props.data
        }

    }

    componentDidMount() {
        if (!this.props.user || !this.props.user.access_token) {
            this.props.history.push("/");
        }
        if (!this.props.data){
            // this.fetchAllData();
        }
    }

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            const data = {
                'searchtext': values.searchtext,
                'searchtype': values.searchtype,
                'exactmatch': this.state.exactmatch,
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

    onChange = () => {
        this.setState({ exactmatch: !this.state.exactmatch });
    }

    fetchAllData = () =>{
        const initData = {
            'searchtext': "*",
            'searchtype': "mrn",
            'exactmatch': false,
            'role': this.props.user.role
        }
        this.props.searchData(initData, this.props.user.access_token);
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
                                    rules: [{ required: true, message: "Required MRN's or Tumor Type or DMP ID to search." }],
                                    onChange: this.handleInputChange
                                })(
                                    <Input
                                        prefix={<Icon type="search" style={{ color: 'rgba(0,0,0,.25)' }} />}
                                        size="large"
                                        name="searchtext"
                                        placeholder="enter comma separated mrn's, tumor type or dmp id's"
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
                                    //initialValue: "",
                                })(
                                    <Select placeholder="search type" size="large" style={{ minWidth: 150 }} onChange={(value) => this.handleSearchTypeSelectChange(value, 'searchtype')}>
                                        <Select.Option value="MRN">MRN</Select.Option>
                                        <Select.Option value="TUMOR TYPE">TUMOR TYPE</Select.Option>
                                        <Select.Option value="DMPID">DMP ID</Select.Option>
                                    </Select>
                                )}
                            </Form.Item>
                        </Col>

                        {
                            this.state.searchtype === "TUMOR TYPE" &&
                            <Col>
                                <Checkbox checked={this.state.exactmatch} onChange={(e)=>this.onChange(e)}>Find Exact Match</Checkbox>
                            </Col>
                        }
                        <Col>
                            <Form.Item>
                                <Button type="primary" size="large" htmlType="submit">
                                    <Icon type="search" />Search
                                </Button>
                            </Form.Item>
                        </Col>

                    </Row>
                </Form>
                <Row type="flex" justify="center">
                        <Col span={3} >
                            <Button type="link" block onClick={() => this.fetchAllData()}>
                                <Text mark underline strong style={styles.notification_div}>Click here to see all available data</Text>
                            </Button>
                        </Col>
                </Row>
                <Row type="flex" justify="center">
                        <Col span={10} >
                            <Text strong>For inquiries regarding access to the WES repository data, please contact the <a href="mailto:skicmopm@mskcc.org?subject=WES repository access enquiry.">CMO PM team</a> (skicmopm@mskcc.org)</Text>
                        </Col>
                </Row>
                {this.props.isFetching ? <div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Loading..." size='large' /></div> :
                    this.props.data && <DataGridEditTrackingInfo rowdata={this.props.data} />
                }
            
                {/* <DevTools /> */}
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
    user: state.user.userData,
    savedata: state.saveResult
});

const mapDispatchToProps = dispatch => ({
    searchData: (data, token) => dispatch(search_data(data, token))
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Form.create()(SearchForm)));
