import React, {useContext, useState, useEffect} from 'react';
import bcrypt from 'bcryptjs';

const AuthContext = React.createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({children}){

    const [currentUser, setCurrentUser] = useState();
    const [loading, setLoading] = useState(true);

    async function registerApplicant(name, email, password, confirmPassword, major, standing, gpa, skills) {
        if(!name || !email || !password || !confirmPassword || !major.length
            || !standing.length || !gpa || !skills.length) {
            throw 'Fields not filled out';
        } else if(password !== confirmPassword){
            throw 'Passwords do not match';
        } else {
            const temp = await fetch(`/applicants?email=${email}`).then(response => {
                if(response.ok){
                    return response.json();
                }
             });
             if(temp.length > 0){
                throw 'This email has already been taken';
             } else {
                return fetch('/applicants', {
                    method: 'POST',
                    body: JSON.stringify({
                        name,
                        email,
                        password: bcrypt.hashSync(password, 10),
                        features: {
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
                }).then(data => {
                    setCurrentUser(data);
                    setLoading(false);
                });
             }
        }
    }

    async function logInApplicant(email, password) {
        if(!email || !password){
            throw 'Fields are required';
        } else {
            const temp = await fetch(`/applicants?email=${email}`).then(response => {
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
    }

    async function registerBusiness(name, email, password, confirmPassword, major, standing, gpa, skills) {
        if(!name || !email || !password || !confirmPassword || !major.length
            || !standing.length || !gpa || !skills.length) {
            throw 'Fields not filled out';
        } else if(password !== confirmPassword){
            throw 'Passwords do not match';
        } else {
            const temp = await fetch(`/businesses?email=${email}`).then(response => {
                if(response.ok){
                    return response.json();
                }
             });
             if(temp.length > 0){
                throw 'This email has already been taken';
             } else {
                return fetch('/businesses', {
                    method: 'POST',
                    body: JSON.stringify({
                        name,
                        email,
                        password: bcrypt.hashSync(password, 10),
                        features: {
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
                }).then(data => {
                    setCurrentUser(data);
                    setLoading(false);
                });
             }
        }
    }

    async function logInBusiness(email, password) {
        if(!email || !password){
            throw 'Fields are required';
        } else {
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
    }

    async function logOut(){
        setCurrentUser(null);
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
        logOut
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}