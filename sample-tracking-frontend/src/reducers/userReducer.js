
const initialState = {
    userData: null,
    isFetching: false,
    isError: false,
    error:''
  };
  
  const userReducer = (state = initialState, action) => {
      switch (action.type) {
        case 'LOGIN_USER_BEGIN':
          return Object.assign({}, state,{
            isFetching: true,
            isError: false
          });
        case 'LOGIN_USER_SUCCESS':
          return Object.assign({}, state,{
            userData: action.data,
            isFetching: false,
            isError: false,
            error:action.error,
          });
        case 'LOGIN_USER_FAILURE':
          return Object.assign({}, state,{
            isError: true,
            error: action.error,
            isFetching: false
          });
        case 'LOGIN_USER_INVALID':
          return Object.assign({}, state,{
            userData:action.data,
            error: action.error,
            isFetching: false
        });
        case 'LOGOUT_USER_BEGIN':
          return Object.assign({}, state,{
            isFetching: true,
            isError: false
          });
        case 'LOGOUT_USER_SUCCESS':
          return Object.assign({}, state,{
            userData: action.data,
            isFetching: false,
            isError: false,
          });
        case 'LOGOUT_USER_FAILURE':
          return Object.assign({}, state,{
            userData: action.data,
            isError: true,
            error: action.error,
            isFetching: false
          });
        case 'SESSION_END_SUCCESS':
          return Object.assign({}, state,{
            userData: action.data,
            isError: true,
            error: action.error,
            isFetching: false
          });

        default:
          return state;
      }
    };
  export default userReducer;
  