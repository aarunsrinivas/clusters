import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs'
import {Link, useHistory} from 'react-router-dom';


export function LoginApplicantForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {logInApplicant} = useAuth();
    const history = useHistory();

     async function handleClick() {
        try {
            setError('Logged In');
            setLoading(true);
            if(!email || !password){
                throw 'Fields are required';
            }
            await logInApplicant(email, password);
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
            <button onClick={() => handleClick()}>Submit</button>
            <div>
                Need an Account? <Link to='/register'>Register</Link>
            </div>
        </div>
    )
}