import React, {useState, useEffect} from 'react';
import {Link, useHistory} from 'react-router-dom';
import TagsInput from 'react-tagsinput';
import {useAuth} from '../../contexts/AuthContext';
import {socket} from '../../App';

export function RegisterApplicantForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [major, setMajor] = useState([]);
    const [standing, setStanding] = useState([]);
    const [gpa, setGpa] = useState(0);
    const [skills, setSkills] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {registerApplicant} = useAuth();
    const history = useHistory();


    async function handleClick() {
        try {
            setError('');
            setLoading(true);
            await registerApplicant(name, email, password,
                confirmPassword, major, standing, gpa, skills);
            history.push('/');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        setName('');
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setMajor([]);
        setStanding([]);
        setGpa(0);
        setSkills([]);
    }

    return (
        <div>
            Name: <input value={name} onChange={e => setName(e.target.value)}/>
            <br/>
            Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            Password: <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <br/>
            Confirm Password: <input type='password' value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}/>
            <br/>
            Major: <TagsInput value={major} onChange={tags => setMajor(tags)}/>
            <br/>
            Standing: <TagsInput value={standing} onChange={tags => setStanding(tags)}/>
            <br/>
            GPA: <input value={gpa} onChange={e => setGpa(e.target.value)}/>
            <br/>
            Skills: <TagsInput value={skills} onChange={tags => setSkills(tags)}/>
            <button disabled={loading} onClick={() => handleClick()}>Submit</button>
            <div>
                Already Have an Account? <Link to='/login/applicant'>Log In</Link>
            </div>
        </div>
    )
}