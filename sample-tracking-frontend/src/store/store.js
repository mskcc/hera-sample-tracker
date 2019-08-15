import { createStore, applyMiddleware, compose } from 'redux';
import rootReducer from '../reducers/rootReducer';
import thunk from 'redux-thunk';
import DevTools from '../components/devtools';

const store = createStore(rootReducer,undefined, compose(applyMiddleware(thunk), DevTools.instrument()));
export default store;