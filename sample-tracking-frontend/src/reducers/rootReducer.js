import { combineReducers} from 'redux';
import userReducer from './userReducer';
import mainReducer from './mainReducer';

const rootReducer = combineReducers({
    user: userReducer,
    searchResult: mainReducer
});

export default rootReducer;