import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from './contexts/AuthContext';

export function PrivateRoute({component: Component, ...rest}){
    const {currentUser} = useAuth();
    console.log(currentUser);
    return (
        <Route {...rest} render={props => currentUser ? <Component {...props}/> : <Redirect to='/login'/>}/>
    )
}