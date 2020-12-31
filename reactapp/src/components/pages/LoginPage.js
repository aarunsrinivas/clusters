import React from 'react';
import {LoginApplicantForm} from '../forms/LoginApplicantForm';
import {LoginBusinessForm} from '../forms/LoginBusinessForm';

export function LoginPage() {
    return (
        <div>
            <h1>Applicant Login</h1>
            <LoginApplicantForm/>
            <br/>
            <h1>Business Login</h1>
            <LoginBusinessForm/>
        </div>
    )
}