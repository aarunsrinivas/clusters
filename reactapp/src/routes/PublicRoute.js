import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from '../contexts/AuthContext';

export function PublicRoute({component: Component, ...rest}){
    const {currentUser} = useAuth();

    return (
        <Route {...rest} render={props => !currentUser ? <Component {...props}/> : <Redirect to='/dashboard'/>}/>
    )
}