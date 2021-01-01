import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom';

export function ActiveDashBoard(){

    const {currentUser} = useAuth();
    const [pool, setPool] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();

    useEffect(async () => {
        if(currentUser.features.type === 'applicant'){
            const businesses = await fetch(currentUser.links.businesses).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setPool(businesses);
        } else if(currentUser.features.type === 'business'){
            const applicants = await fetch(currentUser.links.applicants).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setPool(applicants)
        }
    }, []);

    function renderPool(){
        return pool.map(user => {
            return (
                <div>
                    <h2>{user.name}</h2>
                    <u1>{user.skills}</u1>
                </div>
            )
        })
    }

    return (
        <div>
            {currentUser.features.type === 'applicant' && <h1>Businesses</h1>}
            {currentUser.features.type === 'business' && <h1>Applicants</h1>}
            {renderPool()}

        </div>
    );
}

