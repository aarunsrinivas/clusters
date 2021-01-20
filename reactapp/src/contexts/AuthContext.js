import React, {useContext, useState, useEffect} from 'react';
import {auth} from '../firebase';
import firebase from 'firebase/app';

const AuthContext = React.createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({children}) {

    const [currentUser, setCurrentUser] = useState(JSON.parse(sessionStorage.getItem('currentUser')) || null);
    const [userData, setUserData] = useState(JSON.parse(sessionStorage.getItem('userData')) || null);
    const [loading, setLoading] = useState(true);


    async function registerUser(name, email, password, type, worldId) {
        const fire = auth.createUserWithEmailAndPassword(email, password);
        const destination = type === 'applicant' ? `${process.env.REACT_APP_BACKEND_URL}/worlds/${worldId}/applicants`
            : `${process.env.REACT_APP_BACKEND_URL}/worlds/${worldId}/businesses`;
        const data = await fetch(destination, {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                worldId
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
        return fire;
    }

    async function loginUser(email, password){
        const fire = auth.signInWithEmailAndPassword(email, password);
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}/users?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data[0]);
        return fire;
    }

    async function updateAccount(name, email, password, worldId){
        currentUser.updateEmail(email);
        password && currentUser.updatePassword(password);
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: 'account',
                name,
                email,
                worldId
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
    }

    async function updateFeatures(cap, gpa, majors, standings, skills, interests, courses){
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: 'features',
                cap: parseInt(cap),
                gpa: parseFloat(gpa),
                majors,
                standings,
                skills,
                interests,
                courses
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
    }

    async function logoutUser(){
        const fire = auth.signOut();
        setUserData(null);
        return fire;
    }

    async function deleteUser(){
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'DELETE'
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        const fire = currentUser.delete();
        setUserData(null);
        return fire;
    }

    async function joinCluster(){
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'POST',
            body: JSON.stringify({action: 'join'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
    }

    async function leaveCluster(){
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'POST',
            body: JSON.stringify({action: 'leave'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
    }

    async function peelFromCluster(){
        const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.self}`, {
            method: 'POST',
            body: JSON.stringify({action: 'peel'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setUserData(data);
    }

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged(async user => {
            if(!user){
                sessionStorage.clear();
            } else if(user && !userData){
                const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}/users?email=${user.email}`).then(response => {
                    if(response.ok){
                        return response.json();
                    }
                });
                setUserData(data[0]);
                sessionStorage.setItem('currentUser', JSON.stringify(user));
            }
            setCurrentUser(user);
        })
        setLoading(false)
        return unsubscribe;
    }, []);

    useEffect(() => {
        userData ? sessionStorage.setItem('userData', JSON.stringify(userData))
            : sessionStorage.clear();
    }, [userData]);

    const value = {
        currentUser,
        userData,
        registerUser,
        loginUser,
        logoutUser,
        deleteUser,
        updateAccount,
        updateFeatures,
        joinCluster,
        peelFromCluster,
        leaveCluster,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}