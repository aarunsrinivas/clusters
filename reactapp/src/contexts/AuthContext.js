import React, {useContext, useState, useEffect} from 'react';
import bcrypt from 'bcryptjs';

const AuthContext = React.createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({children}) {

    const [currentUser, setCurrentUser] = useState(JSON.parse(sessionStorage.getItem('currentUser')) || null);
    const [loading, setLoading] = useState(true);

    async function registerUser(name, email, password, type, major, standing, gpa, skills) {
        const temp = await fetch(`/users?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        if(temp.length){
            throw 'This email has already been taken';
        }
        const destination = type === 'applicant' ? '/applicants' : '/businesses';
        const data = await fetch(destination, {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                password: bcrypt.hashSync(password, 10),
                features: {
                    type,
                    major,
                    standing,
                    gpa: parseFloat(gpa),
                    skills
                }
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(data);
    }

    async function loginUser(email, password){
        const temp = await fetch(`/users?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        if(!temp.length){
            throw 'No email associated with account';
        } else if(!(await bcrypt.compare(password, temp[0].password))){
            throw 'Invalid password';
        }
        setCurrentUser(temp[0]);
        return temp[0];
    }

    async function updateUser(name, email, password, major, standing, gpa, skills){
        if(email !== currentUser.email){
            const temp = await fetch(`/users?email=${email}`).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            if(temp.length){
                throw 'This email has been taken';
            }
        }
        const data = await fetch(currentUser.links.self, {
            method: 'PUT',
            body: JSON.stringify({
                name,
                email,
                password: password ? bcrypt.hashSync(password, 10) : currentUser.password,
                features: {
                    type: 'applicant',
                    major,
                    standing,
                    gpa: parseFloat(gpa),
                    skills
                }
            })
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(data);
    }

    async function logoutUser(){
        setCurrentUser(null);
    }

    async function deleteUser(){
        if(!currentUser){
            throw 'No user to be deleted'
        }
        const temp = await fetch(currentUser.links.self, {
            method: 'DELETE'
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(null);
    }

    async function joinCluster(){
        if(!currentUser){
            throw 'No user to be joined';
        } else if(currentUser.clusterId){
            throw 'Already in a cluster';
        }
        const data = await fetch(currentUser.links.self, {
            method: 'POST',
            body: JSON.stringify({action: 'join'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(data);
    }

    async function leaveCluster(){
        if(!currentUser){
            throw 'No user to be joined';
        } else if(!currentUser.clusterId){
            throw 'Already outside cluster';
        }
        const data = await fetch(currentUser.links.self, {
            method: 'POST',
            body: JSON.stringify({action: 'leave'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(data);
    }

    async function peelFromCluster(){
        if(!currentUser){
            throw 'No user to be joined';
        } else if(!currentUser.clusterId){
            throw 'Cannot peel from outside cluster';
        }
        const data = await fetch(currentUser.links.self, {
            method: 'POST',
            body: JSON.stringify({action: 'peel'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        setCurrentUser(data);
    }

    useEffect(() => {
        !currentUser ? sessionStorage.clear() :
            sessionStorage.setItem('currentUser', JSON.stringify(currentUser));
        setLoading(false)
    }, [currentUser]);

    const value = {
        currentUser,
        registerUser,
        loginUser,
        updateUser,
        logoutUser,
        deleteUser,
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