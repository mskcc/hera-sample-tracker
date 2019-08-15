
import axios from 'axios';
import {BASE_URL, requestHeaders} from '../configs/react.configs';

export const user_login = () => {
  return {
    type: 'LOGIN_USER_BEGIN'
  };
};

export const user_login_success = (user) => {
  return {
    type: 'LOGIN_USER_SUCCESS',
    isError:'',
    data: user,
    error:''
  };
};

export const user_login_invalid = (user) => {
  return {
    type: 'LOGIN_USER_INVALID',
    data: user,
    error: "Invalid Username or Password"
  };
};

export const user_login_failure = (error) => {
  return {
    type: 'LOGIN_USER_FAILURE',
    error: error
  };
};

export const operation_error = (error) => {
    return {
      type: 'OPERATION_ERROR',
      isError: true,
      error: error
    };
  };

  export const login = (data, history) => {
    return dispatch => {
      dispatch(user_login());
      axios.post(BASE_URL + "login",data, requestHeaders)
        .then(res => {
          if (res.data.valid){
            dispatch(user_login_success(res.data));
            history.push('/home');
          }
          if (!res.data.valid){
            dispatch(user_login_invalid(res.data));
          }
        })
        .catch(err => {
          dispatch(user_login_failure(err));
        });
    };
  };
  
