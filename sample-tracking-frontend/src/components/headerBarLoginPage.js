import React, {Component} from 'react';
import {Row, Col} from 'antd';
import mskcc_logo from '../assets/mskcc_logo.png';

class HeaderBarLoginPage extends Component{
    render(){
        return(
            <div>
            <Row  type= "flex" style = {{backgroundColor:'#007CBA', maxHeight:65, overflow:'hidden'}}>
              <Col >
                <div>
                    <img alt="example" src= {mskcc_logo} style={{maxHeight:65}}/>
                </div>
              </Col>
              <Col push={4} style={{padding:'auto', color:'black', fontSize:35, fontFamily:'sans-serif'}}>
              Sample Tracking App
              </Col>
            </Row>
          </div>
        );
    }

}

export default HeaderBarLoginPage;