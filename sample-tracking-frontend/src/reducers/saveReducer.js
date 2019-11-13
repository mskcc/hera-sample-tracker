const initialState = {
    data: null,
    responseData:null,
    isFetching: false,
    isError: false,
    message:''
  };
  
  const saveReducer = (state = initialState, action) => {
      switch (action.type) {
        case 'SAVE_DATA_BEGIN':
          return Object.assign({}, state,{
            isFetching: true,
            isError: false,
            message:''
          });

        case 'SAVE_DATA_SUCCESS':
          return Object.assign({}, state,{
            isFetching: false,
            isError: false,
            message: action.message,
          });

        case 'SAVE_DATA_FAILURE':
          return Object.assign({}, state,{
            isError: true,
            isFetching: false,
            message: action.message,
          });
          
        case 'OPERATION_ERROR':
          return Object.assign({}, state,{
            isError: true,
            isFetching: false,
            message: action.message,
        });
        default:
          return state;
      }
    };
  export default saveReducer;
  