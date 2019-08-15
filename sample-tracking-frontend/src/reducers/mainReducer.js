const initialState = {
    data: null,
    isFetching: false,
    isError: false,
    message:''
  };
  
  const mainReducer = (state = initialState, action) => {
      switch (action.type) {
        case 'SEARCH_DATA_BEGIN':
          return Object.assign({}, state,{
            isFetching: true,
            isError: false,
            message:''
          });

        case 'SEARCH_DATA_SUCCESS':
          console.log(action)
          return Object.assign({}, state,{
            data: action.data,
            isFetching: false,
            isError: false,
            message:''
          });

        case 'SEARCH_DATA_NOTFOUND':
          return Object.assign({}, state,{
            data: null,
            isError: false,
            isFetching: false,
            message: action.message,
          });

        case 'SEARCH_DATA_FAILURE':
          return Object.assign({}, state,{
            data:null,
            isError: false,
            isFetching: false,
            message: action.message,
        });

        case 'OPERATION_ERROR':
          return Object.assign({}, state,{
            data: null,
            isError: true,
            isFetching: false,
            message: action.error,
        });
        default:
          return state;
      }
    };
  export default mainReducer;
  