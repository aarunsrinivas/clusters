import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs'
import {Link, useHistory} from 'react-router-dom';


export function LoginBusinessForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {logInBusiness} = useAuth();
    const history = useHistory();

     async function handleClick() {
        try {
            setError('Logged In');
            setLoading(true);
            await logInBusiness(email, password);
            history.push('/');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        setEmail('');
        setPassword('');
    };


    return (
        <div>
            <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <button onClick={() => handleClick()}>Submit</button>
            <div>
                Need an Account? <Link to='/register/business'>Register</Link>
            </div>
        </div>
    )
}