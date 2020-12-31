import './App.css';
import io from 'socket.io-client';
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
import {PrivateRoute} from './PrivateRoute';


function App() {
  return (
    <Router>
        <AuthProvider>
            <Switch>
                <Route exact path='/' component={HomePage}/>
                <Route path='/register' component={RegistrationPage}/>
                <Route path='/login' component={LoginPage}/>
                <PrivateRoute path='/dashboard' component={UpdatePage}/>
            </Switch>
        </AuthProvider>
    </Router>
  );
}

export default App;
