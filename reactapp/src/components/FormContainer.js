import React from 'react'
import ApplicantForm from './ApplicantForm.js'
import BusinessForm from './BusinessForm.js'

const FormContainer = () => {
    return (
        <React.Fragment>
            <ApplicantForm />
            <BusinessForm />
        </React.Fragment>
    );
}

export default FormContainer;