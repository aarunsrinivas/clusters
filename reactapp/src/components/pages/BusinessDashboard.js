import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom';

export function BusinessDashboard(){

    const {currentUser} = useAuth();
    const [pool, setPool] = useState([]);
    const [reached, setReached] = useState(JSON.parse(sessionStorage.getItem('reached')) || []);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState();
    const history = useHistory();


    // handle peel
    useEffect(async () => {
        const data = await fetch(currentUser.links.pool).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setPool(data);
    }, [currentUser]);


    useEffect(async () => {
        sessionStorage.setItem('reached', JSON.stringify(reached));
        setLoading(false);
    }, [reached]);


    async function handleReach(applicantId){
        try {
            setError('Successfully Reached');
            setLoading(true);
            const data = await fetch(currentUser.links.reached, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'reach',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setReached(data);
        } catch (err) {
            setError('Failed to reach out');
        }
    }


    async function handleCancel(applicantId){
        try {
            setError('Successfully Canceled');
            setLoading(true);
            const data = await fetch(currentUser.links.reached, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'cancel',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setReached(data);
        } catch (err) {
            setError('Failed to cancel');
        }
    }


    function renderPool(){
        return pool.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleReach(applicant.id)}>Apply</button>
                </div>
            )
        })
    }


    function renderReached(){
        return reached.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleCancel(applicant.id)}>Cancel</button>
                </div>
            )
        })
    }

    return (
        <div>
            <h2>Pool</h2>
            {renderPool()}
            <br/>
            <h2>Reached</h2>
            {renderReached()}
        </div>
    );
}

