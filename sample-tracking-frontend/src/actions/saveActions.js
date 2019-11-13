import {message} from 'antd';
import axios from 'axios';
import { BASE_URL } from '../configs/react.configs';


export const save_data_begin = () => {
  return {
    type: 'SAVE_DATA_BEGIN',
  };
};

export const save_data_success = (message) => {
  return {
    type: 'SAVE_DATA_SUCCESS',
    message: message,
    error:false
  };
};

export const save_data_failure = (message) => {
  return {
    type: 'SAVE_DATA_FAILURE',
    message: message,
    error:true
  };
};

export const save_operation_error = (error) => {
  return {
    type: 'SAVE_OPERATION_ERROR',
    message: error,
    error:true
  };
};

export const save_changes = (data, token) => {
  var config = {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authorization': "Bearer " + token
    }
  };
  return dispatch => {
    dispatch(save_data_begin());
    axios.post(BASE_URL + "save_sample_changes", data, config
    )
    .then (res => {
      if (res.data.success) {
        message.success({content: 'Success!\nThe Data has been saved successfully.', duration: 3});
        return dispatch(save_data_success(res.data.message));
      }
      if (!res.data.success) {
        return dispatch(save_data_failure(res.data.message));
      }
    })
    .catch(err => {
        console.log(err);
      return dispatch(save_operation_error(err));
    });
  };
};