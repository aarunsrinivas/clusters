import logo from './logo.svg';
import './App.css';
import io from 'socket.io-client';
import {RegisterApplicantForm} from './components/forms/RegisterApplicantForm'

export const socket = io.connect('http://127.0.0.1:5000/private');

function App() {
  return (
    <div>
        <RegisterApplicantForm/>
    </div>
  );
}

export default App;
