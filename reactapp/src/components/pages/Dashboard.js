import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {ActiveDashboard} from './sub-pages/ActiveDashboard';
import {DormantDashboard} from './sub-pages/DormantDashboard';
import {NavBar} from '../modules/NavBar';

export function Dashboard(){

    const {userData} = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();

    return (
        <div>
            <NavBar/>
            {!userData.clusterId && <DormantDashboard/>}
            {userData.clusterId && <ActiveDashboard/>}
        </div>
    );
}