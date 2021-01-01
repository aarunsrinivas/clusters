import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom'

export function PeelButton({children}){

    const {currentUser, peelFromCluster} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleClick(){
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

    return (
        <button onClick={() => handleClick()}>{children}</button>
    )

}