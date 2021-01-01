import React from 'react';
import {Route, Redirect} from 'react-router-dom';
import {useAuth} from '../contexts/AuthContext';

export function DormantPrivateRoute({component: Component, ...rest}){
    const {currentUser} = useAuth();
    return (
        <Route {...rest} render={props => {
                if(!currentUser){
                    return <Redirect to='/login'/>;
                } else if(currentUser.clusterId){
                    return <Redirect to='/dashboard?status=active'/>;
                } else {
                    return <Component {...props}/>;
                }
            }
        }/>
    )
}