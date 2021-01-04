import './App.css';
<<<<<<< HEAD
import {HomePage} from './components/pages/HomePage';
import {LoginPage} from './components/pages/LoginPage';
import {RegistrationPage} from './components/pages/RegistrationPage';
import {AuthProvider} from './contexts/AuthContext';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';
import {PrivateRoute} from './routes/PrivateRoute';
import {ActivePrivateRoute} from './routes/ActivePrivateRoute';
import {DormantPrivateRoute} from './routes/DormantPrivateRoute';
import {ActiveDashboard} from './components/pages/ActiveDashboard';
import {DormantDashboard} from './components/pages/DormantDashboard';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <Route exact path='/' component={HomePage}/>
                <Route path='/register' component={RegistrationPage}/>
                <Route path='/login' component={LoginPage}/>
                <DormantPrivateRoute path='/dormant-dashboard' component={DormantDashboard}/>
                <ActivePrivateRoute path='/active-dashboard' component={ActiveDashboard}/>
            </Switch>
        </AuthProvider>
    </Router>
=======
import {ApplicantRegistration} from './components/forms/ApplicantRegistration'

function App() {
  return (
    <div>
        <ApplicantRegistration/>
    </div>
>>>>>>> main
  );
}

export default App;
