import React, {useState, useEffect} from 'react';
import bcrypt from 'bcryptjs';
import TagsInput from 'react-tagsinput';

export function BusinessRegistration() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [major, setMajor] = useState([]);
    const [standing, setStanding] = useState([]);
    const [gpa, setGpa] = useState(0);
    const [skills, setSkills] = useState([]);

    const handleClick = () => {
        fetch('/businesses', {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                password: bcrypt.hashSync(password, 10),
                features: {
                    major,
                    standing,
                    gpa: parseFloat(gpa),
                    skills
                }
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => console.log(data));
    }

    return (
        <div>
            Name: <input value={name} onChange={e => setName(e.target.value)}/>
            <br/>
            Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            Password: <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
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