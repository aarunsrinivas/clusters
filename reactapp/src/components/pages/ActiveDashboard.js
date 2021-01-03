import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom';
import {NavBar} from '../NavBar';

export function ActiveDashboard(){

    const {currentUser, logoutUser, deleteUser, peelFromCluster, leaveCluster} = useAuth();
    const [pool, setPool] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    useEffect(async () => {
        const data = await fetch(currentUser.links.pool).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setPool(data);
    }, [currentUser]);

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

    async function handlePeelFromCluster(){
        try {
            setError('Peeled From Cluster');
            setLoading(true);
            await peelFromCluster();
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(error);
    }

    async function handleLeaveCluster(){
        try {
            setError('Left Cluster');
            setLoading(true);
            await leaveCluster();
            history.push('/dormant-dashboard');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(error);
    }

    function renderPool(){
        return pool.map(user => {
            return (
                <div>
                    <h2>{user.name}</h2>
                    <li>{user.features.skills}</li>
                </div>
            )
        })
    }

    return (
        <div>
            <NavBar />
            <h1>Active Dashboard</h1>
            {renderPool()}
            <button disabled={loading} onClick={handleLogoutUser}>Logout</button>
            <button disabled={loading} onClick={handleDeleteUser}>Delete User</button>
            <button disabled={loading} onClick={handlePeelFromCluster}>Peel From Cluster</button>
            <button disabled={loading} onClick={handleLeaveCluster}>Leave Cluster</button>

        </div>
    );
}

