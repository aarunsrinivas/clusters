import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {UpdateForm} from '../forms/UpdateForm';
import {ActiveDashboard} from './sub-pages/ActiveDashboard';
import {DormantDashboard} from './sub-pages/DormantDashboard';
import {useHistory} from 'react-router-dom';
import {NavBar} from '../modules/NavBar';

export function Dashboard(){

    const {userData, logoutUser, deleteUser} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();


    return (
        <div>
            <NavBar />
            {!userData.clusterId && <DormantDashboard/>}
            {userData.clusterId && <ActiveDashboard/>}
        </div>
    );
}