import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {useHistory} from 'react-router-dom';

export function ApplicantDashboard(){

    const {currentUser} = useAuth();
    const [pool, setPool] = useState([]);
    const [applied, setApplied] = useState(JSON.parse(sessionStorage.getItem('applied')) || []);
    //const [reviewed, setReviewed] = useState(JSON.parse(sessionStorage.getItem('reviewed')) || []);
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
        sessionStorage.setItem('applied', JSON.stringify(applied));
        setLoading(false);
    }, [applied]);

    /*
    useEffect(async () => {
        sessionStorage.setItem('reviewed', JSON.stringify(reviewed));
        setLoading(false);
    }, [reviewed]);
    */

    async function handleSubmitApplication(businessId){
        try {
            setError('Successfully Applied');
            setLoading(true);
            const data = await fetch(currentUser.links.applied, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'apply',
                    businessId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setApplied(data);
        } catch (err) {
            setError('Failed to apply');
        }
    }

    async function handleCancelApplication(businessId){
        try {
            setError('Successfully Canceled');
            setLoading(true);
            const data = await fetch(currentUser.links.applied, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'cancel',
                    businessId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setApplied(data);
        } catch (err) {
            setError('Failed to cancel');
        }
    }

    /*
    async function handleReviewOffer(businessId){
        try {
            setError('Successfully Accepted Offer');
            setLoading(true);
            const data = await fetch(currentUser.links.reviewed, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'accept',
                    businessId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setApplied(data);
        } catch (err) {
            setError('Failed to apply');
        }
    }

    async function handleDeclineOffer(businessId){
        try {
            setError('Successfully Canceled');
            setLoading(true);
            const data = await fetch(currentUser.links.reviewed, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'decline',
                    businessId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setApplied(data);
        } catch (err) {
            setError('Failed to cancel');
        }
    }
    */

    function renderPool(){
        return pool.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleSubmitApplication(business.id)}>Apply</button>
                </div>
            )
        })
    }

    function renderApplied(){
        return applied.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleCancelApplication(business.id)}>Cancel</button>
                </div>
            )
        })
    }

    return (
        <div>
            <h2>Pool</h2>
            {renderPool()}
            <br/>
            <h2>Applied</h2>
            {renderApplied()}
        </div>
    );
}

