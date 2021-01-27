import React from 'react';
import {useAuth} from '../../contexts/AuthContext';
import {
    Navbar,
    Nav,
    Button
} from 'react-bootstrap';

export function NavBar () {

    const {currentUser, userData} = useAuth();

    function renderNav() {
        if(!currentUser || !userData){
            return (
                <Navbar bg="light" expand="lg">
                    <Navbar.Brand href="/">Clusters</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="mr-auto">
                            <Nav.Link href="/">Home</Nav.Link>
                            <Nav.Link href="/register">Register</Nav.Link>
                            <Nav.Link href="/login">Log In</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar> 
            );
        } else {
            return (
                <Navbar bg="light" expand="lg">
                    <Navbar.Brand href="/">Clusters</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="mr-auto">
                            <Nav.Link href="/">Home</Nav.Link>
                            <Nav.Link href="/dashboard">Dashboard</Nav.Link>
                            <Nav.Link href="/account">Account</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Navbar>
            );
        }
    }

    return (
        <>
            {renderNav()}
        </>
    )
}