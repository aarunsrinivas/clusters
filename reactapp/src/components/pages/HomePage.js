import React from 'react';
import {NavBar} from '../modules/NavBar';
import '../../styles/HomePage.css';

export function HomePage() {

    return (
        <div>
            <NavBar />
            <div className="home-container">
                <h1 className="home-header">Clusters</h1>
                <hr />
                <p className="home-description">An easier way to find the best fit for both students and researchers alike.</p>
            </div>
        </div>
    )
}