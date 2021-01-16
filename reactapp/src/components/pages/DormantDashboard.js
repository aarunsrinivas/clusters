import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateForm} from '../forms/UpdateForm';
import {useHistory} from 'react-router-dom';

export function DormantDashboard(){

    const {userData, logoutUser, deleteUser, joinCluster} = useAuth();
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

    async function handleJoinCluster(){
        try {
            setError('Joined Cluster');
            setLoading(true);
            const {gpa, majors, standings, skills, interests, courses} = userData.features;
            if(!gpa || !majors.length || !standings.length || !skills.length || !interests.length || !courses.length) {
               throw 'Fields not filled out';
            }
            await joinCluster();
            history.push('/active-dashboard')
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(error);
    }

    return (
        <div>
            <h1>Dormant Dashboard</h1>
            <UpdateForm/>
            <button disabled={loading} onClick={handleLogoutUser}>Logout</button>
            <button disabled={loading} onClick={handleDeleteUser}>Delete User</button>
            <button disabled={loading} onClick={handleJoinCluster}>Join Cluster</button>
        </div>
    );
}