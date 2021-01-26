import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {Link, useHistory} from 'react-router-dom';
import {
    Form,
    Button
} from 'react-bootstrap';
import '../../styles/Form.css'


export function LoginForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {loginUser, userData} = useAuth();
    const history = useHistory();

     async function handleLoginUser() {
        try {
            setError('Logged In');
            setLoading(true);
            if(!email || !password){
                throw 'Fields are required';
            }
            await loginUser(email, password);
            history.push('/dashboard');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    };


    return (

        <div>

            <div className="form-container">

                <h1 className="form-header">Log In</h1>

                <Form>

                    <Form.Group controlId="email">
                        <Form.Label>Email Address</Form.Label>
                        <Form.Control type="email" placeholder="Enter email" 
                        value={email} onChange={e => setEmail(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Enter password" 
                        value={password} onChange={e => setPassword(e.target.value)} />
                    </Form.Group>
                    
                    <div className="form-button">
                        <Button variant="primary" onClick={handleLoginUser} block>
                            Sign in </Button>
                    </div>

                </Form>


                <div className="form-register-redirect">
                        <span><p>Need an Account? <Link to='/register'>Register</Link></p></span>
                </div>

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
    )
}