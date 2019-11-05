
import axios from 'axios';
import {BASE_URL, requestHeaders} from '../configs/react.configs';

const user_login = () => {
  return {
    type: 'LOGIN_USER_BEGIN'
  };
};

const user_login_success = (user) => {
  return {
    type: 'LOGIN_USER_SUCCESS',
    isError:'',
    data: user,
    error:''
  };
};

const user_login_invalid = (user) => {
  return {
    type: 'LOGIN_USER_INVALID',
    data: user,
    error: "Invalid Username or Password"
  };
};

const user_login_failure = (error) => {
  return {
    type: 'LOGIN_USER_FAILURE',
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

  const user_logout = () => {
    return {
      type: 'LOGOUT_USER_BEGIN'
    };
  };
  
  const user_logout_success = (user) => {
    return {
      type: 'LOGOUT_USER_SUCCESS',
      isError:'',
      data: user,
      error:''
    };
  };
  
  const user_logout_failure = (error) => {
    return {
      type: 'LOGIN_USER_FAILURE',
      error: error
    };
  };

  export const logout = (data, configs, history) => {
    return dispatch => {
      dispatch(user_logout());
      axios.post(BASE_URL + "logout",data, configs)
        .then(res => {
          if (res.data.success){
            console.log("logout success");
            console.log(res.data);
            dispatch(user_logout_success(res.data));
            localStorage.clear();
            localStorage.removeItem('persist:root');
            history.push('/');
          }
        })
        .catch(err => {
          dispatch(user_logout_failure(err));
        });
    };
  };
  
