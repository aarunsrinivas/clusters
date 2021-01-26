import React, {useState} from 'react';
import {Link, useHistory} from 'react-router-dom';
import {useAuth} from '../../contexts/AuthContext';
import '../../styles/Form.css';
import {
    Form,
    Button,
    ToggleButtonGroup,
    ToggleButton
} from 'react-bootstrap';


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
            await registerUser(name, email, password, type, worldId)
            history.push('/dashboard');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    return (
        
        <div className="register-container">

            <h1 className="register-header">Create Account</h1>

            <Form>
                <div className="radio-container">
                    <ToggleButtonGroup type="radio" name="type">
                        <ToggleButton value={1} onClick={() => setType('applicant')}>Student</ToggleButton>
                        <ToggleButton value={2} variant="secondary" onClick={() => setType('business')}>Faculty </ToggleButton> 
                    </ToggleButtonGroup>
                </div>

                {/* <div className="radio-container">
                    <input type='radio' name='type' onClick={() => setType('applicant')}/> Student {' '}
                    <input type='radio' name='type' onClick={() => setType('business')}/> Faculty
                </div> */}

                <Form.Group controlId="name">
                    <Form.Label>Name</Form.Label>
                    <Form.Control placeholder="Enter name" 
                    value={name} onChange={e => setName(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="worldId">
                    <Form.Label>College</Form.Label>
                    <Form.Control placeholder="Enter college" 
                    value={worldId} onChange={e => setWorldId(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" 
                    value={email} onChange={e => setEmail(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password" 
                    value={password} onChange={e => setPassword(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="confirmPassword">
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control type="password" placeholder="Confirm password" 
                    value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
                </Form.Group>

                <div className="register-button">
                    <Button variant="primary" disabled={loading} onClick={handleRegisterUser} block>Sign up</Button>
                </div>

            </Form>
            
            <div className="form-register-redirect">
                Already Have an Account? <Link to='/login'>Sign in</Link>
            </div>

        </div>



        // <div>
        //     Type:
        //     <input type='radio' name='type' onClick={() => setType('applicant')}/> Applicant
        //     <input type='radio' name='type' onClick={() => setType('business')}/> Business
        //     <br/>
        //     College: <input value={worldId} onChange={e => setWorldId(e.target.value)}/>
        //     <br/>
        //     Name: <input value={name} onChange={e => setName(e.target.value)}/>
        //     <br/>
        //     Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
        //     <br/>
        //     Password: <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
        //     <br/>
        //     Confirm Password: <input type='password' value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}/>
        //     <br/>
        //     <button disabled={loading} onClick={handleRegisterUser}>Submit</button>
        //     <div>
        //         Already Have an Account? <Link to='/login'>Log In</Link>
        //     </div>
        // </div>
    )
}