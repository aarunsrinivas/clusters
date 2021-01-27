import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {ChatPanel} from '../panels/ChatPanel';
import {
    Card,
    Button,
    Tab,
    Row,
    Col,
    Nav
} from 'react-bootstrap';

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

    function renderPool(){
        if (pool.length == 0) {
            return (
                <h4>No available applicants!</h4>
            );
        }
        return pool.map(applicant => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{applicant.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(applicant.features.skills)}
                                <br/>
                                {formatCourses(applicant.features.courses)}
                            </Card.Text>
                            <Button variant="primary" onClick={() => handleSubmitReach(applicant.id)}>Contact</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{applicant.name}</h3>
                //     <li>{applicant.features.skills}</li>
                //     <button onClick={() => handleSubmitReach(applicant.id)}>Reach</button>
                // </div>
            )
        })
    }

    function renderReached(){
        if (reached.length == 0) {
            return (
                <h4>You haven't contacted any students yet!</h4>
            );
        }
        return reached.map(applicant => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{applicant.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(applicant.features.skills)}
                                <br/>
                                {formatCourses(applicant.features.courses)}
                            </Card.Text>
                            <Button variant="danger" onClick={() => handleCancelReach(applicant.id)}>Cancel</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{applicant.name}</h3>
                //     <li>{applicant.features.skills}</li>
                //     <button onClick={() => handleCancelReach(applicant.id)}>Reach</button>
                // </div>
            )
        })
    }

    function renderReceived(){
        if (received.length == 0) {
            return (
                <h4>You haven't received any applications yet!</h4>
            );
        }
        return received.map(applicant => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{applicant.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(applicant.features.skills)}
                                <br/>
                                {formatCourses(applicant.features.courses)}
                            </Card.Text>
                            <Button variant="primary" onClick={() => handleAcceptApply(applicant.id)}>Accept</Button>
                            <Button variant="danger" onClick={() => handleDeclineApply(applicant.id)}>Decline</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{applicant.name}</h3>
                //     <li>{applicant.features.skills}</li>
                //     <button onClick={() => handleAcceptApply(applicant.id)}>Accept</button>
                //     <button onClick={() => handleDeclineApply(applicant.id)}>Decline</button>
                // </div>
            )
        })
    }

    // *** Replaced by ChatPanel and Chat tab ***
    // function renderInterested(){
    //     return interested.map(applicant => {
    //         return (
    //             <div>
    //                 <h3>{applicant.name}</h3>
    //                 <li>{applicant.features.skills}</li>
    //                 <button onClick={() => handleOfferInterest(applicant.id)}>Offer</button>
    //                 <button onClick={() => handleDeclineInterest(applicant.id)}>Decline</button>
    //             </div>
    //         )
    //     })
    // }

    function renderOffered(){
        if (offered.length == 0) {
            return (
                <h4>You haven't offered any applicants a position yet!</h4>
            );
        }
        return offered.map(applicant => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{applicant.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(applicant.features.skills)}
                                <br/>
                                {formatCourses(applicant.features.courses)}
                            </Card.Text>
                            <Button variant="danger" onClick={() => handleRescindOffer(applicant.id)}>Rescind Offer</Button>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{applicant.name}</h3>
                //     <li>{applicant.features.skills}</li>
                //     <button onClick={() => handleRescindOffer(applicant.id)}>Rescind</button>
                // </div>
            )
        })
    }

    function renderAccepted(){
        if (accepted.length == 0) {
            return (
                <h4>You haven't accepted any applicants yet!</h4>
            );
        }
        return accepted.map(applicant => {
            return (
                <div className="single-card-container">
                    <Card style={{width: '16rem'}}>
                        <Card.Body>
                            <Card.Title>{applicant.name}</Card.Title>
                            <Card.Text>
                                {formatSkills(applicant.features.skills)}
                                <br/>
                                {formatCourses(applicant.features.courses)}
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </div>
                // <div>
                //     <h3>{applicant.name}</h3>
                //     <li>{applicant.features.skills}</li>
                // </div>
            )
        })
    }

    return (

        <div>
            <Tab.Container defaultActiveKey="available">
                <Row>
                    <Col sm={2}>
                        <Nav variant="pills" className="flex-column">
                            <Nav.Item>
                                <Nav.Link eventKey="available">Available</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="reached">Contacted</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="received">Received</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="chats">Chats</Nav.Link>
                            </Nav.Item>
                            <Nav.Item>
                                <Nav.Link eventKey="offers">Offered</Nav.Link>
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
                            <Tab.Pane eventKey="reached">
                                <h2>Contacted</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderReached()}
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
                                <h2>Offered</h2>
                                <hr/>
                                <div className="all-cards-container">
                                    {renderOffered()}
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

        // <div>
        //     <h2>Pool</h2>
        //     {renderPool()}
        //     <br/>
        //     <h2>Reached</h2>
        //     {renderReached()}
        //     <h2>Received</h2>
        //     {renderReceived()}
        //     <h2>Interested</h2>
        //     <ChatPanel />
        //     <h2>Offered</h2>
        //     {renderOffered()}
        //     <h2>Accepted</h2>
        //     {renderAccepted()}
        // </div>
    );
}

