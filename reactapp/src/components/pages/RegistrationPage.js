import React from 'react';
import {RegisterApplicantForm} from '../forms/RegisterApplicantForm';
import {RegisterBusinessForm} from '../forms/RegisterBusinessForm';

export function RegistrationPage() {
    return (
        <div>
            <h1>Applicant Registration</h1>
            <RegisterApplicantForm/>
            <br/>
            <h1>Business Registration</h1>
            <RegisterBusinessForm/>
        </div>
    )
}