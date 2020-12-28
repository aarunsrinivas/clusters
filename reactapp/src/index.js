import React from 'react';
import ReactDOM from 'react-dom';
import './styles/index.css';
import App from './App';
import FormContainer from './components/FormContainer';
import Dashboard from './components/Dashboard';

ReactDOM.render(
  <React.StrictMode>
    <App />
    <FormContainer />
    <Dashboard />
  </React.StrictMode>,
  document.getElementById('root')
);
