import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateApplicantForm} from '../forms/UpdateApplicantForm';
import {UpdateBusinessForm} from '../forms/UpdateBusinessForm';
import {useHistory} from 'react-router-dom';

export function UpdatePage(){

    const {currentUser, logOut} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleClick(){
        try {
            setError('Logged Out');
            setLoading(true);
            await logOut();
            history.push('/');
        } catch {
            setError('Failed to log out');
        }
        console.log(error);
    }

    return (
        <div>
            {currentUser.type === 'applicant' && <h1>Applicant</h1>}
            {currentUser.type === 'applicant' && <UpdateApplicantForm/>}
            {currentUser.type === 'business' && <h1>Business</h1>}
            {currentUser.type === 'business' && <UpdateBusinessForm/>}
            <br/>
            <button variant='link'onClick={() => handleClick()}>Log Out</button>
        </div>
    )
}