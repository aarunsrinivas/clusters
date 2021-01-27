import React, {useState, useEffect} from 'react';
import {useAuth} from '../../../contexts/AuthContext';
import {ApplicantPanel} from '../../panels/ApplicantPanel';
import {BusinessPanel} from '../../panels/BusinessPanel';
import {useHistory} from 'react-router-dom';
import {Button} from 'react-bootstrap';

export function ActiveDashboard(){

    const {userData, peelFromCluster, leaveCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();


    // async function handlePeelFromCluster(){
    //     try {
    //         setError('Peeled From Cluster');
    //         setLoading(true);
    //         await peelFromCluster();
    //     } catch(err) {
    //         setError(err);
    //     }
    //     setLoading(false);
    // }

    async function handleLeaveCluster(){
        try {
            setError('Left Cluster');
            setLoading(true);
            await leaveCluster();
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }


    return (
        <div className="dashboard-container">
            {userData.type === 'applicant' && <ApplicantPanel/>}
            {userData.type === 'business' && <BusinessPanel/>}
            {/* <button disabled={loading} onClick={handlePeelFromCluster}>Peel From Cluster</button> */}
            <div className="leave-button-container">
                <Button variant="danger" disabled={loading} onClick={handleLeaveCluster} block>Leave Cluster</Button>
            </div>
        </div>
    );
}

