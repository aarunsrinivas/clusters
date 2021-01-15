import React, {useState, useEffect} from 'react';
import {Link, useHistory} from 'react-router-dom';
import TagsInput from 'react-tagsinput';
import {useAuth} from '../../contexts/AuthContext';


export function AccountForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [worldId, setWorldId] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {updateAccount} = useAuth();
    const history = useHistory();


    async function handleUpdateAccount() {
        try {
            setError('Updated Account');
            setLoading(true);
            if(!name || !email || !password || !confirmPassword || !worldId) {
               throw 'Fields not filled out';
            } else if(password !== confirmPassword){
                throw 'Passwords do not match';
            }
            const data = await updateAccount(name, email, password, worldId);
        } catch(err) {
            setError(err);
        }
        console.log(error);
        setLoading(false);
    }

    return (
        <div>
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
            <button disabled={loading} onClick={handleUpdateAccount}>Submit</button>
            <div>
                Already Have an Account? <Link to='/login'>Log In</Link>
            </div>
        </div>
    )
}