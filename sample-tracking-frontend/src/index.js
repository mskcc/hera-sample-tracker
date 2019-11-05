import React from 'react';
import ReactDOM from 'react-dom';
import 'index.scss';
import {Provider} from 'react-redux';
import {persistor, store}  from './store/store';
import { PersistGate } from 'redux-persist/integration/react'
import {Spin} from 'antd';
import 'antd/dist/antd.css';
import App from './views/app';

ReactDOM.render(
            <Provider store = {store}>
              <PersistGate loading={<div style={{ marginLeft: '47%', marginTop: '15%', marginRight: '47%' }}><Spin tip="Loading..." size='large' /></div>} persistor={persistor}>
                <App/>
              </PersistGate>
            </Provider>,
  document.getElementById("root")
);