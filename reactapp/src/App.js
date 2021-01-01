import './App.css';
import {HomePage} from './components/pages/HomePage';
import {LoginPage} from './components/pages/LoginPage';
import {RegistrationPage} from './components/pages/RegistrationPage';
import {UpdatePage} from './components/pages/UpdatePage';
import {AuthProvider} from './contexts/AuthContext';
import {
    BrowserRouter as Router,
    Switch,
    Route
} from 'react-router-dom';
import {DefaultPrivateRoute} from './routes/DefaultPrivateRoute';
import {ActivePrivateRoute} from './routes/ActivePrivateRoute';
import {DormantPrivateRoute} from './routes/DormantPrivateRoute';
import {ActiveDashBoard} from './components/pages/ActiveDashBoard';
import {DormantDashBoard} from './components/pages/DormantDashBoard';


function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <Route exact path='/' component={HomePage}/>
                <Route path='/register' component={RegistrationPage}/>
                <Route path='/login' component={LoginPage}/>
                <DefaultPrivateRoute path='/update' component={UpdatePage}/>
                <DormantPrivateRoute path='/dashboard?status=dormant' component={DormantDashBoard}/>
                <ActivePrivateRoute path='/dashboard?status=active' component={ActiveDashBoard}/>
            </Switch>
        </AuthProvider>
    </Router>
  );
}

export default App;
