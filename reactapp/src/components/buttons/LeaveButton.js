import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom'

export function LeaveButton({children}){

    const {currentUser, leaveCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleClick(){
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
        <button onClick={() => handleClick()}>{children}</button>
    )

}