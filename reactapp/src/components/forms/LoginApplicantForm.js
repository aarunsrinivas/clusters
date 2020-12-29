import React, {useState, useEffect} from 'react';
import bcrypt from 'bcryptjs'


export function LoginApplicantForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [user, setUser] = useState({});
    const [passwordHash, setPasswordHash] = useState('');

     const handleClick = () => {
        fetch(`/applicants?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => {
            if(data.length > 0){
                setUser(data[0]);
            }
        });
    };


    useEffect(() => {
        if(!user.password || !bcrypt.compareSync(password, user.password)){
            console.log('incorrect login');
        } else {
            console.log('logging in');
        }
        setEmail('');
        setPassword('');
    }, [user]);


    return (
        <div>
            <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <button onClick={() => handleClick()}>Submit</button>
        </div>
    )
}