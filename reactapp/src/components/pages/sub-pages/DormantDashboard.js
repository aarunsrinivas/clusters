import React, {useState} from 'react';
import {useAuth} from '../../../contexts/AuthContext';
import {UpdateForm} from '../../forms/UpdateForm';
import {useHistory} from 'react-router-dom';

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
        console.log(error);
    }

    return (
        <div>
            <UpdateForm/>
            <button disabled={loading} onClick={handleJoinCluster}>Join Cluster</button>
        </div>
    );
}