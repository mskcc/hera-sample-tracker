import store from '../store/store';
export const BASE_URL = "http://127.0.0.1:5000/";

export const requestHeaders = { headers: {  
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Authorization' : store.getState().user.access_token
}
}
