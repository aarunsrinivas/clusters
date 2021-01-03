import React from 'react'
import {useAuth} from '../../contexts/AuthContext'
import {NavBar} from '../NavBar';

export function HomePage() {

    const {currentUser} = useAuth();

    return (
        <div>
            <NavBar />
            <h1>Clusters</h1>
            <br/>
            {currentUser && <u1>{JSON.stringify(currentUser)}</u1>}
        </div>
    )
}