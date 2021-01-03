import React from 'react';
import {LoginForm} from '../forms/LoginForm';
import {NavBar} from '../NavBar';

export function LoginPage() {
    return (
        <div>
            <NavBar />
            <LoginForm/>
        </div>
    )
}