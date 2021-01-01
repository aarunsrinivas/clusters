import React from 'react'
import {useAuth} from '../../contexts/AuthContext'

export function HomePage() {

    const {currentUser} = useAuth();

    return (
        <div>
            Home Page
            <br/>
            {currentUser && <u1>{JSON.stringify(currentUser)}</u1>}
        </div>
    )
}