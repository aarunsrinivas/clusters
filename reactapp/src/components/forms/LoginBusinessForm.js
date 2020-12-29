import React, {useState, useEffect} from 'react';
import bcrypt from 'bcryptjs'


export function BusinessLogin() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [user, setUser] = useState({});


     const handleClick = () => {
        fetch(`/businesses?email=${email}`).then(response => {
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
            <input value={email} onChange={e => setEmail(e.target.value)}/>
            <br/>
            <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            <button onClick={() => handleClick()}>Submit</button>
        </div>
    )
}