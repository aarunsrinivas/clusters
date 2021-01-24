import React from 'react';
import {
    Navbar,
    Nav,
} from 'react-bootstrap';

export function NavBar () {


    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="http://localhost:3000/">Clusters</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="http://localhost:3000/">Home</Nav.Link>
                    <Nav.Link href="http://localhost:3000/active-dashboard">Dashboard</Nav.Link>
                    <Nav.Link href="http://localhost:3000/account">Account</Nav.Link>
                    <Nav.Link href="http://localhost:3000/register">Register</Nav.Link>
                    <Nav.Link href="http://localhost:3000/login">Log In</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}