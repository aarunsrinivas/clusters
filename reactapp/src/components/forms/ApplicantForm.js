import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';

export function ApplicantForm(){

    const {userData, leaveCluster} = useAuth();
    const [change, setChange] = useState(false);
    const [cap, setCap] = useState(1);
    const [pool, setPool] = useState([]);
    const [applied, setApplied] = useState([]);
    const [received, setReceived] = useState([]);
    const [interested, setInterested] = useState([]);
    const [reviewed, setReviewed] = useState([]);
    const [accepted, setAccepted] = useState([]);
    const [declined, setDeclined] = useState([]);
    const [rejected, setRejected] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState();

    useEffect(async () => {
        const data = await fetch(userData.links.all).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCap(data.cap);
        setPool(data.pool);
        setApplied(data.applied);
        setReceived(data.received);
        setInterested(data.interested);
        setReviewed(data.reviewed);
        setAccepted(data.accepted);
        setDeclined(data.declined);
        setRejected(data.rejected);
        setLoading(false);
    }, [userData, change]);


    useEffect(async () => {
        if(!cap){
            try {
                setError('Left Cluster');
                setLoading(true);
                await leaveCluster();
            } catch(err) {
                setError('Failed to leave cluster')
            }
        }
    }, [cap])

    async function handleSubmitApply(businessId){
        try {
            setError('Successfully Applied');
            setLoading(true);
            const data = await fetch(userData.links.applied, {
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
            setChange(!change);
        } catch (err) {
            setError('Failed to apply');
        }
    }

    async function handleCancelApply(businessId){
        try {
            setError('Successfully Canceled');
            setLoading(true);
            const data = await fetch(userData.links.applied, {
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
            setChange(!change);
        } catch (err) {
            setError('Failed to cancel');
        }
    }

    async function handleAcceptReach(businessId){
        try {
            setError('Successfully Accepted Reach');
            setLoading(true);
            const data = await fetch(userData.links.received, {
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
            setReceived(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to accept reach');
        }
    }

    async function handleDeclineReach(businessId){
        try {
            setError('Successfully declined reach');
            setLoading(true);
            const data = await fetch(userData.links.received, {
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
            setReceived(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to decline reach');
        }
    }

    async function handleDeclineInterest(businessId){
        try {
            setError('Successfully declined communication');
            setLoading(true);
            const data = await fetch(userData.links.interested, {
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
            setInterested(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to decline communication');
        }
    }

    async function handleAcceptOffer(businessId){
        try {
            setError('Successfully Accepted offer');
            setLoading(true);
            const data = await fetch(userData.links.reviewed, {
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
            try {
                setError('Left cluster');
                setLoading(true);
                await leaveCluster();
            } catch(err) {
                setError(err);
            }
        } catch(err) {
            setError('Failed to accept reach');
        }
    }

    async function handleDeclineOffer(businessId){
        try {
            setError('Successfully declined offer');
            setLoading(true);
            const data = await fetch(userData.links.reviewed, {
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
            setReceived(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to decline offer');
        }
    }

    function renderPool(){
        return pool.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleSubmitApply(business.id)}>Apply</button>
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
                    <button onClick={() => handleCancelApply(business.id)}>Cancel</button>
                </div>
            )
        })
    }

    function renderReceived(){
        return received.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleAcceptReach(business.id)}>Accept</button>
                    <button onClick={() => handleDeclineReach(business.id)}>Decline</button>
                </div>
            )
        })
    }

    function renderInterested(){
        return interested.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleDeclineInterest(business.id)}>Decline</button>
                </div>
            )
        })
    }

    function renderReviewed(){
        return reviewed.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
                    <button onClick={() => handleAcceptOffer(business.id)}>Accept</button>
                    <button onClick={() => handleDeclineOffer(business.id)}>Decline</button>
                </div>
            )
        })
    }

    function renderAccepted(){
        return accepted.map(business => {
            return (
                <div>
                    <h3>{business.name}</h3>
                    <li>{business.features.skills}</li>
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
            <h2>Received</h2>
            {renderReceived()}
            <h2>Interested</h2>
            {renderInterested()}
            <h2>Reviewed</h2>
            {renderReviewed()}
            <h2>Accepted</h2>
            {renderAccepted()}
        </div>
    );
}

