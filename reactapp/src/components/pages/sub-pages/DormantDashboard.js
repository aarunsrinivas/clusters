import React, {useState} from 'react';
import {useAuth} from '../../../contexts/AuthContext';
import {UpdateForm} from '../../forms/UpdateForm';
import {useHistory} from 'react-router-dom';
import {Button} from 'react-bootstrap';
import '../../../styles/Dashboard.css'

export function DormantDashboard(){

    const {userData, joinCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleJoinCluster(){
        try {
            setError('Joined Cluster');
            setLoading(true);
            const {gpa, majors, standings, skills, interests, courses} = userData.features;
            if(!gpa || !majors.length || !standings.length || !skills.length || !interests.length || !courses.length) {
               throw 'Fields not filled out';
            }
            await joinCluster();
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    return (
        <div className="dormant-container">
            <UpdateForm/>
            <hr/>
            <Button variant="primary" disabled={loading} onClick={handleJoinCluster} block>Join Cluster</Button>
        </div>
    );
}