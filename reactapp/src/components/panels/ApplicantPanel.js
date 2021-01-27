import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import '../../styles/Dashboard.css';
import {
    Card,
    Button,
    Tab,
    Row,
    Col,
    Nav
} from 'react-bootstrap';
import {ChatPanel} from '../panels/ChatPanel';

export function ApplicantPanel(){

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
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.all}`).then(response => {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.applied}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.applied}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.received}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.received}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.interested}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.reviewed}`, {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.reviewed}`, {
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
        if (pool.length === 0) {
            return (
                <h4>No availible positions!</h4>
            );
        }
        return pool.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                                <br/>
                                {formatCourses(business.features.courses)}
                            </Card.Text>
                            <Button variant="primary" onClick={() => handleSubmitApply(business.id)}>Apply</Button>
                        </Card.Body>
                    </Card>
                </div>
            )
        })
    }

    function formatSkills(skills){
        var list = "";
        for (var i = 0; i < skills.length - 1; i++) {
            list += skills[i] + " | ";
        }
        list += skills[skills.length - 1];

        return list;
    }

    function formatCourses(courses){
        var list = "";
        for (var i = 0; i < courses.length - 1; i++) {
            list += courses[i] + " | ";
        }
        list += courses[courses.length - 1];

        return list;
    }

    function renderApplied(){
        if (applied.length === 0) {
            return (
                <h4>You haven't applied to any positions!</h4>
            )
        }
        return applied.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '14rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                            </Card.Text>
                            <Button variant="danger" onClick={() => handleCancelApply(business.id)}>Cancel</Button>
                        </Card.Body>
                    </Card>
                </div>
            )
        })
    }

    function renderReceived(){
        if (received.length === 0) {
            return(
                <h4>You haven't received any offers directly from professors!</h4>
            );
        }
        return received.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '14rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                            </Card.Text>
                            <Button variant="primary" onClick={() => handleAcceptReach(business.id)}>Accept</Button> {''} 
                            <Button variant="danger" onClick={() => handleDeclineReach(business.id)}>Decline</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{business.name}</h3>
                //     <li>{business.features.skills}</li>
                //     <button onClick={() => handleAcceptReach(business.id)}>Accept</button>
                //     <button onClick={() => handleDeclineReach(business.id)}>Decline</button>
                // </div>
            )
        })
    }

    function renderInterested(){
        if (interested.length === 0) {
            return (
                <h4>You haven't received any chats yet!</h4>
            );
        }
        return interested.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '14rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                            </Card.Text>
                            <Button variant="danger" onClick={() => handleDeclineInterest(business.id)}>Decline</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{business.name}</h3>
                //     <li>{business.features.skills}</li>
                //     <button onClick={() => handleDeclineInterest(business.id)}>Decline</button>
                // </div>
            )
        })
    }

    function renderReviewed(){
        if (reviewed.length === 0) {
            return (
                <h4>You haven't received any offers yet!</h4>
            );
        }
        return reviewed.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '14rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                            </Card.Text>
                            <Button variant="primary" onClick={() => handleAcceptOffer(business.id)}>Accept Offer</Button> 
                            <Button variant="danger" onClick={() => handleDeclineOffer(business.id)}>Decline Offer</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{business.name}</h3>
                //     <li>{business.features.skills}</li>
                //     <button onClick={() => handleAcceptOffer(business.id)}>Accept</button>
                //     <button onClick={() => handleDeclineOffer(business.id)}>Decline</button>
                // </div>
            )
        })
    }

    function renderAccepted(){
        if (accepted.length === 0) {
            return (
                <h4>You haven't accepted any offers yet!</h4>
            );
        }
        return accepted.map(business => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '14rem'}}>
                        <Card.Body>
                            <Card.Title>{business.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(business.features.skills)}
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{business.name}</h3>
                //     <li>{business.features.skills}</li>
                // </div>
            )
        })
    }

    return (
        <div className="">
            <Tab.Container defaultActiveKey="available">
                <Row>
                    <Col sm={2}>
                        <Nav variant="pills" className="flex-column">
                            <Nav.Item>
                                <Nav.Link eventKey="available">Available</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="applied">Applied</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="received">Received</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="chats">Chats</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="offers">Offers</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="accepted">Accepted</Nav.Link>
                            </Nav.Item>
                        </Nav>
                    </Col>
                    <Col sm={10}>
                        <Tab.Content>
                            <Tab.Pane eventKey="available">
                                <h2>Available</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderPool()}
                                </div>
                            </Tab.Pane>
                            <Tab.Pane eventKey="applied">
                                <h2>Applied</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderApplied()}
                                </div>
                            </Tab.Pane>
                            <Tab.Pane eventKey="received">
                                <h2>Received</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderReceived()}
                                </div>
                            </Tab.Pane>
                            <Tab.Pane eventKey="chats">
                                <h2>Chats</h2>
                                <hr/>
                                <div>
                                    <ChatPanel />
                                </div>
                            </Tab.Pane>
                            <Tab.Pane eventKey="offers">
                                <h2>Offers</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderReviewed()}
                                </div>
                            </Tab.Pane>
                            <Tab.Pane eventKey="accepted">
                                <h2>Accepted</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderAccepted()}
                                </div>
                            </Tab.Pane>
                        </Tab.Content>
                    </Col>
                </Row>
            </Tab.Container>

        </div>

        // <div className="dashboard-container">
        //     <h1>Dashboard</h1>
        //     <hr/>

            // <h2>Available Positions</h2>
            // <div className="all-cards-container">
            //     {renderPool()}
            // </div>
        //     <hr/>

            // <h2>Applied</h2>
            // <div className="all-cards-container">
            //     {renderApplied()}
            // </div>
            // <hr/>

        //     <h2>Received</h2>
        //     <div className="all-cards-container">
        //         {renderReceived()}
        //     </div>
        //     <hr/>

        //     <h2>Interested</h2>
        //     <div className="all-cards-container">
        //         {renderInterested()}
        //     </div>
        //     <hr/>

        //     <h2>Offers</h2>
        //     <div className="all-cards-container">
        //         {renderReviewed()}
        //     </div>
        //     <hr/>

        //     <h2>Accepted</h2>
        //     <div className="all-cards-container"></div>
        //     {renderAccepted()}
            
        // </div>

    );
}

