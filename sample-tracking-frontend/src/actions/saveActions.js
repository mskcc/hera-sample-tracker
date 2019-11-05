import axios from 'axios';
import { BASE_URL} from '../configs/react.configs';

export const save_data_begin = () => {
    return {
      type: 'SAVE_DATA_BEGIN'
    };
  };
  
  export const save_data_success = (response) => {
    return {
      type: 'SAVE_DATA_SUCCESS',
      data: response
    };
  };
  
  export const save_data_failure = (save_error) => {
    return {
      type: 'SAVE_DATA_FAILURE',
      error: save_error
    };
  };
  
  export const save_operation_error = (error) => {
    return {
      type: 'SAVE_OPERATION_ERROR',
      error: error
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
        .then(res => {
            console.log(res);
          if (res.success && res.message != null) {
            console.log(res.data);
            return dispatch(save_data_success(res.message));
          }
          if (!res.success) {
              console.log(res.data);
            dispatch(save_data_failure(res.search_error));
          }
        })
        .catch(err => {
            console.log(err);
          return dispatch(save_operation_error(err));
        });
    };
  };