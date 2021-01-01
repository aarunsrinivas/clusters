import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateApplicantForm} from '../forms/UpdateApplicantForm';
import {UpdateBusinessForm} from '../forms/UpdateBusinessForm';
import {DeleteButton} from '../buttons/DeleteButton';
import {JoinButton} from '../buttons/JoinButton';
import {LeaveButton} from '../buttons/LeaveButton';
import {PeelButton} from '../buttons/PeelButton';
import {useHistory} from 'react-router-dom';

export function UpdatePage(){

    const {currentUser, logOut} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleLogOut(){
        try {
            setError('Logged Out');
            setLoading(true);
            await logOut();
            history.push('/');
        } catch {
            setError('Failed to log out');
        }
        console.log(error);
        setLoading(false);
    }

    return (
        <div>
            {currentUser.features.type === 'applicant' && <h1>Applicant</h1>}
            {currentUser.features.type === 'applicant' && <UpdateApplicantForm/>}
            {currentUser.features.type === 'business' && <h1>Business</h1>}
            {currentUser.features.type === 'business' && <UpdateBusinessForm/>}
            <br/>
            <button variant='link' onClick={() => handleLogOut()}>Log Out</button>
            <br/>
            <DeleteButton>Delete Account</DeleteButton>
            <br/>
            <JoinButton>Join Cluster</JoinButton>
            <br/>
            <LeaveButton>Leave Cluster</LeaveButton>
            <br/>
            <PeelButton>Peel From Cluster</PeelButton>
        </div>
    )
}