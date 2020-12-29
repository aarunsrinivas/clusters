import React, {useState, useEffect} from 'react';
import bcrypt from 'bcryptjs'


export function ApplicantLogin() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [user, setUser] = useState({});
    const [passwordHash, setPasswordHash] = useState('');

    const handleEmailChange = e => {
        e.preventDefault();
        setEmail(e.target.value);
    };

    const handlePasswordChange = e => {
        e.preventDefault();
        setPassword(e.target.value);
    };

     const handleClick = () => {
        fetch(`/applicants?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => {
            setUser(data[0]);
        });
    };


    useEffect(() => {
        if(!user || !user.password || !bcrypt.compareSync(password, user.password)){
            console.log('incorrect login');
        } else {
            console.log('logging in');
        }
        setEmail('');
        setPassword('');
    }, [user]);


    return (
        <div>
            <input value={email} onChange={e => handleEmailChange(e)}/>
            <br/>
            <input type='password' value={password} onChange={e => handlePasswordChange(e)}/>
            <button onClick={() => handleClick()}>Submit</button>
        </div>
    )
}