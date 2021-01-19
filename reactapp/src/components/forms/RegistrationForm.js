import React, {useState, useEffect} from 'react';
import {Link, useHistory} from 'react-router-dom';
import TagsInput from 'react-tagsinput';
import {useAuth} from '../../contexts/AuthContext';


export function RegistrationForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [type, setType] = useState('');
    const [worldId, setWorldId] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {registerUser} = useAuth();
    const history = useHistory();


    async function handleRegisterUser() {
        try {
            setError('Registered');
            setLoading(true);
            if(!name || !email || !password || !confirmPassword || !type || !worldId) {
               throw 'Fields not filled out';
            } else if(password !== confirmPassword){
                throw 'Passwords do not match';
            }
            await registerUser(name, email, password, type, worldId);
            history.push('/dashboard');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    return (
        <div>
            Type:
            <input type='radio' name='type' onClick={() => setType('applicant')}/> Applicant
            <input type='radio' name='type' onClick={() => setType('business')}/> Business
            <br/>
            College: <input value={worldId} onChange={e => setWorldId(e.target.value)}/>
            <br/>
            Name: <input value={name} onChange={e => setName(e.target.value)}/>
            <br/>
            Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            Password: <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <br/>
            Confirm Password: <input type='password' value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}/>
            <br/>
            <button disabled={loading} onClick={handleRegisterUser}>Submit</button>
            <div>
                Already Have an Account? <Link to='/login'>Log In</Link>
            </div>
        </div>
    )
}