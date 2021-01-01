import React, {useState} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom';

export function DormantDashBoard(){

    const {currentUser, deleteUser} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    return (
        <div>
            <h1>Dashboard</h1>
        </div>
    );
}