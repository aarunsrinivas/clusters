import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs';
import TagsInput from 'react-tagsinput';

export function UpdateBusinessForm() {

    const {currentUser, updateBusiness} = useAuth();
    const [name, setName] = useState(currentUser.name);
    const [email, setEmail] = useState(currentUser.email);
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [major, setMajor] = useState(currentUser.features.major);
    const [standing, setStanding] = useState(currentUser.features.standing);
    const [gpa, setGpa] = useState(currentUser.features.gpa);
    const [skills, setSkills] = useState(currentUser.features.skills);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleClick(){
        try {
            setError('Updated');
            setLoading(true);
            if(!name || !email || !major.length
               || !standing.length || !gpa || !skills.length) {
               throw 'Fields not filled out';
            } else if(password !== confirmPassword){
                throw 'Passwords do not match';
            }
            await updateBusiness(name, email, password, major, standing, gpa, skills);
        } catch(err) {
            setError(err);
        }
        console.log(error);
        setLoading(false);
    }

    return (
        <div>
            Name: <input value={name} onChange={e => setName(e.target.value)}/>
            <br/>
            Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            Password: <input type='password' placeholder='Leave blank to keep the same'
                value={password} onChange={e => setPassword(e.target.value)}/>
            <br/>
            Confirm Password: <input type='password' placeholder='Leave blank to keep the same'
                value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}/>
            <br/>
            Major: <TagsInput value={major} onChange={tags => setMajor(tags)}/>
            <br/>
            Standing: <TagsInput value={standing} onChange={tags => setStanding(tags)}/>
            <br/>
            GPA: <input value={gpa} onChange={e => setGpa(e.target.value)}/>
            <br/>
            Skills: <TagsInput value={skills} onChange={tags => setSkills(tags)}/>
            <button onClick={() => handleClick()}>Submit</button>
        </div>
    )
}