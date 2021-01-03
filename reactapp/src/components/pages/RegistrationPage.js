import React from 'react';
import {RegistrationForm} from '../forms/RegistrationForm';
import {NavBar} from '../NavBar';

export function RegistrationPage() {
    return (
        <div>
            <NavBar />
            <RegistrationForm/>
        </div>
    )
}