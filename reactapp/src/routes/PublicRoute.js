import React, {useEffect} from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from '../contexts/AuthContext';

export function PublicRoute({component: Component, ...rest}){
    const {userData} = useAuth();

    return (
        <Route {...rest} render={props => !userData ? <Component {...props}/> : <Redirect to='/dashboard'/>}/>
    )
}