import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {Link, useHistory} from 'react-router-dom';


export function LoginForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {loginUser, userData} = useAuth();
    const history = useHistory();

     async function handleLoginUser() {
        try {
            setError('Logged In');
            setLoading(true);
            if(!email || !password){
                throw 'Fields are required';
            }
            await loginUser(email, password);
            history.push('/dashboard');
        } catch(err) {
            setError(err);
        }
        console.log(error);
        setLoading(false);
    };


    return (
        <div>
            <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <button onClick={handleLoginUser}>Submit</button>
            <div>
                Need an Account? <Link to='/register'>Register</Link>
            </div>
        </div>
    )
}