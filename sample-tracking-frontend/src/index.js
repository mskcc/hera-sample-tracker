import React from 'react';
import ReactDOM from 'react-dom';
import 'index.scss';
import {Provider} from 'react-redux';
import store from './store/store';
import 'antd/dist/antd.css';
import App from './views/app';

ReactDOM.render(
            <Provider store = {store}>
              <App/>
            </Provider>,
  document.getElementById("root")
);