import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {
    Form,
    Button
} from 'react-bootstrap';


export function AccountForm() {
    const {userData, updateAccount, deleteUser, logoutUser} = useAuth();
    const [name, setName] = useState(userData.name);
    const [email, setEmail] = useState(userData.email);
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [worldId, setWorldId] = useState(userData.worldId);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);


    async function handleUpdateAccount() {
        try {
            setError('Updated Account');
            setLoading(true);
            if(!name || !email || !worldId) {
               throw 'Fields not filled out';
            } else if(password !== confirmPassword){
                throw 'Passwords do not match';
            }
            const data = await updateAccount(name, email, password, worldId);
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    async function handleDeleteUser(){
        try {
            setError('Successfully deleted');
            setLoading(true);
            await deleteUser();
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    async function handleLogoutUser(){
        try {
            setError('Logged Out');
            setLoading(true);
            await logoutUser();
            //history.push('/'); // causing an error for some reason
        } catch {
            setError('Failed to log out');
        }
        setLoading(false);
    }

    return (
        <div>
        
            <div className="register-container">

                <h2 className="register-header">Update Account Details</h2>

                <Form>
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
                        <Button variant="primary" disabled={loading} onClick={handleUpdateAccount} block>Update Info</Button>
                    </div>
                    <hr/>
                    <div>
                        <Button variant="warning" disabled={loading} onClick={handleLogoutUser} block>Logout</Button>
                        <Button variant="danger" disabled={loading} onClick={handleDeleteUser} block>Delete Account</Button>
                    </div>
                </Form>

            </div>

        </div>
    )
}