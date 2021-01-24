import React from 'react';
import {LoginForm} from '../forms/LoginForm';
import {NavBar} from '../modules/NavBar';

export function LoginPage() {
    return (
        <div>
            <NavBar />
            <LoginForm />
        </div>
    )
}