import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';

export function BusinessPanel(){

    const {userData, leaveCluster} = useAuth();
    const [change, setChange] = useState(false);
    const [cap, setCap] = useState(1);
    const [pool, setPool] = useState([]);
    const [reached, setReached] = useState([]);
    const [received, setReceived] = useState([]);
    const [interested, setInterested] = useState([]);
    const [offered, setOffered] = useState([]);
    const [declined, setDeclined] = useState([]);
    const [rejected, setRejected] = useState([]);
    const [accepted, setAccepted] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState();

    useEffect(async () => {
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.all}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCap(data.cap);
        setPool(data.pool);
        setReached(data.reached);
        setReceived(data.received);
        setInterested(data.interested);
        setOffered(data.offered);
        setDeclined(data.declined);
        setRejected(data.rejected);
        setAccepted(data.accepted);
        setLoading(false);
    }, [userData, change]);

    useEffect(async () => {
        if(!cap){
            try {
                setError('Left cluster');
                setLoading(true);
                await leaveCluster()
            } catch (err) {
                setError('failed to leave cluster')
            }
        }
    }, [cap])

    async function handleSubmitReach(applicantId){
        try {
            setError('Successfully Reached');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.reached}`, {
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
            setChange(!change);
        } catch (err) {
            setError('Failed to reach');
        }
    }

    async function handleCancelReach(applicantId){
        try {
            setError('Successfully Canceled');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.reached}`, {
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
            setChange(!change);
        } catch (err) {
            setError('Failed to cancel');
        }
    }

    async function handleAcceptApply(applicantId){
        try {
            setError('Successfully Accepted Apply');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.received}`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'accept',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setReceived(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to accept apply');
        }
    }

    async function handleDeclineApply(applicantId){
        try {
            setError('Successfully declined apply');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.received}`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'decline',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setReceived(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to decline apply');
        }
    }

    async function handleOfferInterest(applicantId){
        try {
            setError('Successfully offered');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.interested}`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'offer',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setInterested(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to offer');
        }
    }

    async function handleDeclineInterest(applicantId){
        try {
            setError('Successfully declined communication');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.interested}`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'decline',
                    applicantId
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

    async function handleRescindOffer(applicantId){
        try {
            setError('Successfully rescinded offer');
            setLoading(true);
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.offered}`, {
                method: 'PUT',
                body: JSON.stringify({
                    action: 'rescind',
                    applicantId
                })
            }).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setOffered(data);
            setChange(!change);
        } catch (err) {
            setError('Failed to accept reach');
        }
    }


    function renderPool(){
        return pool.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleSubmitReach(applicant.id)}>Reach</button>
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
                    <button onClick={() => handleCancelReach(applicant.id)}>Reach</button>
                </div>
            )
        })
    }

    function renderReceived(){
        return received.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleAcceptApply(applicant.id)}>Accept</button>
                    <button onClick={() => handleDeclineApply(applicant.id)}>Decline</button>
                </div>
            )
        })
    }

    function renderInterested(){
        return interested.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleOfferInterest(applicant.id)}>Offer</button>
                    <button onClick={() => handleDeclineInterest(applicant.id)}>Decline</button>
                </div>
            )
        })
    }

    function renderOffered(){
        return offered.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
                    <button onClick={() => handleRescindOffer(applicant.id)}>Rescind</button>
                </div>
            )
        })
    }

    function renderAccepted(){
        return accepted.map(applicant => {
            return (
                <div>
                    <h3>{applicant.name}</h3>
                    <li>{applicant.features.skills}</li>
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
            <h2>Received</h2>
            {renderReceived()}
            <h2>Interested</h2>
            {renderInterested()}
            <h2>Offered</h2>
            {renderOffered()}
            <h2>Accepted</h2>
            {renderAccepted()}
        </div>
    );
}

