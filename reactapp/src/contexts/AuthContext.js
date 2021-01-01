import React, {useContext, useState, useEffect} from 'react';
import bcrypt from 'bcryptjs';

const AuthContext = React.createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({children}) {

    const [currentUser, setCurrentUser] = useState();
    const [loading, setLoading] = useState(true);

    async function registerApplicant(name, email, password, major, standing, gpa, skills) {
        const temp = await fetch(`/applicants?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        if(temp.length){
            throw 'This email has already been taken';
        }
        const data = await fetch('/applicants', {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                password: bcrypt.hashSync(password, 10),
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
        setLoading(false);
    }

    async function logInApplicant(email, password){
        const temp = await fetch(`/applicants?email=${email}`).then(response => {
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
        setLoading(false);
    }

    async function registerBusiness(name, email, password, major, standing, gpa, skills){
        const temp = await fetch(`/businesses?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        if(temp.length){
            throw 'This email has already been taken';
        }
        const data = await fetch('/businesses', {
            method: 'POST',
            body: JSON.stringify({
                name,
                email,
                password: bcrypt.hashSync(password, 10),
                features: {
                    type: 'business',
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
        setLoading(false);
    }

    async function logInBusiness(email, password){
        const temp = await fetch(`/businesses?email=${email}`).then(response => {
            if(response.ok){
                return response.json();
            }
        });
        if(!temp.length){
            throw 'No email associated with account';
        } else if(!(await bcrypt.compare(password, temp[0].password))){
            throw 'Invalid password';
        } else {
            setCurrentUser(temp[0]);
            setLoading(false);
        }
    }

    async function updateApplicant(name, email, password, major, standing, gpa, skills){
        if(email !== currentUser.email){
            const temp = await fetch(`/applicants?email=${email}`).then(response => {
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
        setLoading(false);

    }

    async function updateBusiness(name, email, password, major, standing, gpa, skills){
        if(email !== currentUser.email){
            const temp = await fetch(`/businesses?email=${email}`).then(response => {
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
                    type: 'business',
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
        setLoading(false);
    }

    async function logOut(){
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
        setLoading(false);
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
        setLoading(false);
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
        setLoading(false);
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
        setLoading(false);
    }

    useEffect(() => {
        setLoading(false)
    }, [currentUser]);

    const value = {
        currentUser,
        registerApplicant,
        registerBusiness,
        logInApplicant,
        logInBusiness,
        updateApplicant,
        updateBusiness,
        logOut,
        deleteUser,
        joinCluster,
        leaveCluster,
        peelFromCluster,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}