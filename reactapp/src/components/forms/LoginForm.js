import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs'
import {Link, useHistory} from 'react-router-dom';
import { 
    Form,
    Button,
    Col
} from 'react-bootstrap';
import "./Form.css"


export function LoginForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {loginUser} = useAuth();
    const history = useHistory();

     async function handleLoginUser() {
        try {
            setError('Logged In');
            setLoading(true);
            if(!email || !password){
                throw 'Fields are required';
            }
            const data = await loginUser(email, password);
            const destination = data.clusterId ? '/active-dashboard' : '/dormant-dashboard';
            history.push(destination);
        } catch(err) {
            setError(err);
        }
        console.log(error);
        setLoading(false);
    };


    return (

        <div>

            <div className="form-container">

                <h1 className="form-header">Login</h1>

                <Form>

                    <Form.Group controlId="email">
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type="email" placeholder="Enter Email" 
                        value={email} onChange={e => setEmail(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Enter Password" 
                        value={password} onChange={e => setPassword(e.target.value)} />
                    </Form.Group>
                    
                    <div className="form-button">
                        <Button variant="primary" type="submit" onClick={handleLoginUser}>
                            Submit
                        </Button>
                    </div>

                </Form>

            </div>

            <div className="form-register-redirect">
                    <span><p>Need an Account? <Link to='/register'>Register</Link></p></span>
            </div>

        </div>

        // <div>
        //     <input value={email} onChange={e => setEmail(e.target.value)}/>
        //     <br/>
        //     <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
        //     <button onClick={handleLoginUser}>Submit</button>
        //     <div>
        //         Need an Account? <Link to='/register'>Register</Link>
        //     </div>
        // </div>
    );
}