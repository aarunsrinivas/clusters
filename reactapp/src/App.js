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
import {PublicRoute} from './routes/PublicRoute';
import {Dashboard} from './components/pages/Dashboard';
import {ActivePrivateRoute} from './routes/ActivePrivateRoute';
import {ChatPanel} from './components/panels/ChatPanel';


function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <Route exact path='/' component={HomePage}/>
                <PublicRoute path='/register' component={RegistrationPage}/>
                <PublicRoute path='/login' component={LoginPage}/>
                <PrivateRoute path='/account' component={AccountPage}/>
                <PrivateRoute path='/dashboard' component={Dashboard}/>
                <ActivePrivateRoute path='/chats' component={ChatPanel}/>
            </Switch>
        </AuthProvider>
    </Router>
  );
}

export default App;
