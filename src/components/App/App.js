import React from 'react';
import _ from 'lodash';
import './app.css';
import PnlTable from '../PnlTable/PnlTable';
import TransTable from '../TransTable/TransTable';
import ExceptionTable from '../ExceptionTable/ExceptionTable';


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedStore: 'Company1',
      bond: 40,
      stock: 50,
      option: 60,
      json: [],
    };
    this.handleSelectChange = this.handleSelectChange.bind(this);
    this.handleNumChange = this.handleNumChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSelectChange(e) {
    this.setState({ selectedStore: e.target.value })
  }

  handleNumChange(e) {
    const { name, value } = e.target
    this.setState({ [name]: e.target.value })
  }

  handleSubmit() {
    fetch(`http://localhost:5000/data/?store=${this.state.selectedStore}&bond=${this.state.bond}&stock=${this.state.stock}&option=${this.state.option}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
      .then(jsonResponse => {
        this.setState({ json: JSON.parse(jsonResponse) });
      })
  }

  render() {
    return (
      <div className="app">
        <div className="header">
          <h1 className="header__h1">Asset Inventory</h1>
        </div>
        <main className="app__main">
          <section className="main__row1">
            <div className="main__form">
              <select className="main__select" onChange={this.handleSelectChange} name="store">
                <option value="Company1">Company1</option>
                <option value="Company2">Company2</option>
              </select>
              <p>Bonds</p>
              <input className="main__input" onChange={this.handleNumChange} type='number' name="bond" min="1" max="500" />
              <p>Stocks</p>
              <input className="main__input" onChange={this.handleNumChange} type='number' name="stock" min="1" max="500" />
              <p>Options</p>
              <input className="main__input" onChange={this.handleNumChange} type='number' name="option" min="1" max="500" />
              <input className="main__submit" type="submit" value="Submit" onClick={this.handleSubmit} />
            </div>
            <ExceptionTable json={this.state.json} />
          </section>
          <PnlTable json={this.state.json} />
          <TransTable json={this.state.json} />
        </main>
      </div>
    );
  }
}

export default App;
