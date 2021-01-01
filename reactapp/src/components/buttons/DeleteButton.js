import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom'

export function DeleteButton({children}){

    const {currentUser, deleteUser} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    async function handleClick(){
        try {
            setError('Successfully deleted');
            setLoading(true);
            await deleteUser();
            history.push('/');
        } catch(err) {
            setError(err);
        }
        setLoading(false);
        console.log(true);
    }

    return (
        <button onClick={() => handleClick()}>{children}</button>
    )

}