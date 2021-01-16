import './App.css';
import {HomePage} from './components/pages/HomePage';
import {LoginPage} from './components/pages/LoginPage';
import {RegistrationPage} from './components/pages/RegistrationPage';
import {AccountPage} from './components/pages/AccountPage';
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
import {ChatRoom} from './components/pages/sub-pages/ChatRoom';


function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <Route exact path='/' component={HomePage}/>
                <Route path='/register' component={RegistrationPage}/>
                <Route path='/login' component={LoginPage}/>
                <PrivateRoute path='/account' component={AccountPage}/>
                <DormantPrivateRoute path='/dormant-dashboard' component={DormantDashboard}/>
                <ActivePrivateRoute path='/active-dashboard' component={ActiveDashboard}/>
                <ActivePrivateRoute path='/chats' component={ChatRoom}/>
            </Switch>
        </AuthProvider>
    </Router>
  );
}

export default App;
