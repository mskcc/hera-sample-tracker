
import React, {Component} from 'react';
import SearchForm from '../components/searchform';

class Home extends Component {
constructor(props) {
    super(props);
    this.state = {
      'username':'',
      'password': ''
    }
  }

  render() {
    return (
        <div>
          {/* <Navigation/> */}
          <SearchForm/>
        </div>
    );
  }
}

export default Home;