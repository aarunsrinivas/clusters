import React from 'react'
import {useAuth} from '../../contexts/AuthContext';

export function HomePage() {
    const {currentUser} = useAuth();
    return (
        <div>
            {JSON.stringify(currentUser)}
        </div>
    )
}