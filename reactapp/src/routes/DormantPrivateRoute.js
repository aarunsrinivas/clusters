import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from '../contexts/AuthContext';

export function DormantPrivateRoute({component: Component, ...rest}){
    const {currentUser, userData} = useAuth();
    return (
        <Route {...rest} render={props => {
                if(!currentUser || !userData){
                    return <Redirect to='/login'/>;
                } else if(userData.clusterId){
                    return <Redirect to='/active-dashboard'/>;
                } else {
                    return <Component {...props}/>;
                }
            }
        }/>
    )
}