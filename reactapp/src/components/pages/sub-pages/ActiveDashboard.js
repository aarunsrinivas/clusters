import React, {useState, useEffect} from 'react';
import {useAuth} from '../../../contexts/AuthContext';
import {ApplicantForm} from '../../forms/ApplicantForm';
import {BusinessForm} from '../../forms/BusinessForm';
import {useHistory} from 'react-router-dom';

export function ActiveDashboard(){

    const {userData, peelFromCluster, leaveCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();


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
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(error);
    }


    return (
        <div>
            {userData.type === 'applicant' && <ApplicantForm/>}
            {userData.type === 'business' && <BusinessForm/>}
            <button disabled={loading} onClick={handlePeelFromCluster}>Peel From Cluster</button>
            <button disabled={loading} onClick={handleLeaveCluster}>Leave Cluster</button>

        </div>
    );
}

