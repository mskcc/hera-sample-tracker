import axios from 'axios';
import { BASE_URL } from '../configs/react.configs';

export const search_data_begin = () => {
  return {
    type: 'SEARCH_DATA_BEGIN'
  };
};

export const search_data_success = (search_results) => {
  return {
    type: 'SEARCH_DATA_SUCCESS',
    data: search_results
  };
};

export const search_data_notfound = (message) => {
  return {
    type: 'SEARCH_DATA_NOTFOUND',
    message: message
  }
}
export const search_data_failure = (search_error) => {
  return {
    type: 'SEARCH_DATA_FAILURE',
    error: search_error
  };
};

export const operation_error = (error) => {
  return {
    type: 'OPERATION_ERROR',
    error: true,
    message: error
  };
};

export const search_data = (data, token) => {
  var config = {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authorization': "Bearer " + token
    }
  };
  return dispatch => {
    dispatch(search_data_begin());
    axios.post(BASE_URL + "search_data", data, config
    )
      .then(res => {
        if (res.data) {
          return dispatch(search_data_success(res.data));
        }
        if (res.data.success && res.data == null) {
          return dispatch(search_data_notfound(res.data));
        }
        if (res.search_error) {
          dispatch(search_data_failure(res.search_error));
        }
      })
      .catch(err => {
        return dispatch(operation_error(err));
      });
  };
};

