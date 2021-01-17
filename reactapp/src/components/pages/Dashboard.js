import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateForm} from '../forms/UpdateForm';
import {ActiveDashboard} from './sub-pages/ActiveDashboard';
import {DormantDashboard} from './sub-pages/DormantDashboard';
import {useHistory} from 'react-router-dom';

export function Dashboard(){

    const {userData, logoutUser, deleteUser} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();


    async function handleLogoutUser(){
        try {
            setError('Logged Out');
            setLoading(true);
            await logoutUser();
            history.push('/');
        } catch {
            setError('Failed to log out');
        }
        setLoading(false);
        console.log(error);
    }

    async function handleDeleteUser(){
        try {
            setError('Successfully deleted');
            setLoading(true);
            await deleteUser();
            history.push('/');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(error);
    }


    return (
        <div>
            <h1>Dashboard</h1>
            {userData &&
                <div>
                    {!userData.clusterId && <DormantDashboard/>}
                    {userData.clusterId && <ActiveDashboard/>}
                    <button disabled={loading} onClick={handleLogoutUser}>Logout</button>
                    <button disabled={loading} onClick={handleDeleteUser}>Delete User</button>
                </div>
            }
        </div>
    );
}