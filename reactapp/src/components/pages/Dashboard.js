import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateForm} from '../forms/UpdateForm';
import {ActiveDashboard} from './sub-pages/ActiveDashboard';
import {DormantDashboard} from './sub-pages/DormantDashboard';
import {NavBar} from '../modules/NavBar';

export function Dashboard(){

    const {userData, logoutUser, deleteUser} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();

    async function handleLogoutUser(){
        try {
            setError('Logged Out');
            setLoading(true);
            await logoutUser();
        } catch {
            setError('Failed to log out');
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


    return (
        <div>
            <NavBar/>
            {!userData.clusterId && <DormantDashboard/>}
            {userData.clusterId && <ActiveDashboard/>}
            <button disabled={loading} onClick={handleLogoutUser}>Logout</button>
            <button disabled={loading} onClick={handleDeleteUser}>Delete User</button>
        </div>
    );
}