import React, {useContext, useState, useEffect} from 'react';
import io from 'socket.io-client';

/*
const SocketContext = React.createContext();

export function useSock() {
    return useContext(SocketContext);
}

export function SocketProvider({children}) {

    const initSocket = io.connect('http://127.0.0.1:5000/messaging', {
        withCredentials: true
    })


    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}
*/