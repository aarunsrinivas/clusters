import './App.css';
import io from 'socket.io-client';
import {RegisterApplicantForm} from './components/forms/RegisterApplicantForm'
import {LoginApplicantForm} from './components/forms/LoginApplicantForm'
import {RegisterBusinessForm} from './components/forms/RegisterBusinessForm'
import {LoginBusinessForm} from './components/forms/LoginBusinessForm'
import {HomePage} from './components/pages/HomePage'
import {AuthProvider} from './contexts/AuthContext';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';
import {PrivateRoute} from './PrivateRoute';

export const socket = io.connect('http://127.0.0.1:5000/private');

function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <PrivateRoute exact path='/' component={HomePage}/>
                <Route path='/register/applicant' component={RegisterApplicantForm}/>
                <Route path='/login/applicant' component={LoginApplicantForm}/>
                <Route path='/register/business' component={RegisterBusinessForm}/>
                <Route path='/login/business' component={LoginBusinessForm}/>
            </Switch>
        </AuthProvider>
    </Router>
  );
}

export default App;
