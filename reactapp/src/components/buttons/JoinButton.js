import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom'

export function JoinButton({children}){

    const {currentUser, joinCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleClick(){
        try {
            setError('Joined Cluster');
            setLoading(true);
            await joinCluster();
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