import React from 'react';
import {AccountForm} from '../forms/AccountForm';
import {NavBar} from '../modules/NavBar';

export function AccountPage() {
    return (
        <div>
            <NavBar />
            <AccountForm/>
        </div>
    )
}