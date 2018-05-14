import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      searchActive: false,
    };
  }
  render() {
    return (
      <div className="app">
       <div className="header">
        <h1 className="header__h1">Album Library</h1>
      </div>
        <main className="app__main">
        </main>
      </div>
    );
  }
}

export default App;