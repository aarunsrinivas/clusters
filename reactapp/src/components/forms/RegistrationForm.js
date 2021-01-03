import React, {useState, useEffect} from 'react';
import {Link, useHistory} from 'react-router-dom';
import TagsInput from 'react-tagsinput';
import './TagsInput.css';
import {useAuth} from '../../contexts/AuthContext';
import {
    Form,
    Button
} from 'react-bootstrap';
import './Form.css';


export function RegistrationForm() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [type, setType] = useState('')
    const [major, setMajor] = useState([]);
    const [standing, setStanding] = useState([]);
    const [gpa, setGpa] = useState(0);
    const [skills, setSkills] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const {registerUser} = useAuth();
    const history = useHistory();


    async function handleRegisterUser() {
        try {
            setError('Registered');
            setLoading(true);
            if(!name || !email || !password || !confirmPassword || !type || !major.length
               || !standing.length || !gpa || !skills.length) {
               throw 'Fields not filled out';
            } else if(password !== confirmPassword){
                throw 'Passwords do not match';
            }
            await registerUser(name, email, password, type, major, standing, gpa, skills);
            history.push('/dormant-dashboard');
        } catch(err) {
            setError(err);
        }
        console.log(error);
        setLoading(false);
    }

    return (

        <div className="register-container">

            <h1 className="register-header">Create Account</h1>

            <Form>

                <span className="register-radio">
                    <input type='radio' name='type' onClick={() => setType('applicant')}/> Applicant
                    <input type='radio' name='type' onClick={() => setType('business')}/> Business
                </span>

                <Form.Group controlId="name">
                    <Form.Label>Name</Form.Label>
                    <Form.Control placeholder="Enter name" 
                    value={name} onChange={e => setName(e.target.value)} />
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

                <Form.Group controlId="gpa">
                    <Form.Label>GPA</Form.Label>
                    <Form.Control type="number" step="0.01" min="0.00" placeholder="Enter GPA out of 4.0" 
                    value={gpa} onChange={e => setGpa(e.target.value)} />
                </Form.Group>

                Major<TagsInput value={major} onChange={tags => setMajor(tags)}/>
                <br/>
                 Standing<TagsInput value={standing} onChange={tags => setStanding(tags)}/>
                <br/>
                Skills<TagsInput value={skills} onChange={tags => setSkills(tags)}/>

                <div className="register-button">
                    <Button variant="primary" disabled={loading} onClick={handleRegisterUser}>Submit</Button>
                    {/* <button disabled={loading} onClick={handleRegisterUser}>Submit</button> */}
                </div>

            </Form>
            
            <div>
                Already Have an Account? <Link to='/login'>Log In</Link>
            </div>

        </div>
        

    //     <div>
    //         Type:
    //         <input type='radio' name='type' onClick={() => setType('applicant')}/> Applicant
    //         <input type='radio' name='type' onClick={() => setType('business')}/> Business
    //         <br/>
    //         Name: <input value={name} onChange={e => setName(e.target.value)}/>
    //         <br/>
    //         Email: <input value={email} onChange={e => setEmail(e.target.value)}/>
    //         <br/>
    //         Password: <input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
    //         <br/>
    //         Confirm Password: <input type='password' value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)}/>
    //         <br/>
    //         Major: <TagsInput value={major} onChange={tags => setMajor(tags)}/>
    //         <br/>
    //         Standing: <TagsInput value={standing} onChange={tags => setStanding(tags)}/>
    //         <br/>
    //         GPA: <input value={gpa} onChange={e => setGpa(e.target.value)}/>
    //         <br/>
    //         Skills: <TagsInput value={skills} onChange={tags => setSkills(tags)}/>
    //         <button disabled={loading} onClick={handleRegisterUser}>Submit</button>
    //         <div>
    //             Already Have an Account? <Link to='/login'>Log In</Link>
    //         </div>
    //     </div>
    );
}