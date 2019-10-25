import { combineReducers} from 'redux';
import userReducer from './userReducer';
import searchReducer from './searchReducer';
import saveReducer from './saveReducer';

const rootReducer = combineReducers({
    user: userReducer,
    searchResult: searchReducer,
    saveResult: saveReducer
});

export default rootReducer;