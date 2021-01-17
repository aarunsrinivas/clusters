import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import io from 'socket.io-client';

const socket = io.connect('http://127.0.0.1:5000/messaging');

export function ChatForm(){

    const {userData} = useAuth();
    const [chatsList, setChatsList] = useState([]);
    const [chat, setChat] = useState({});
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    socket.on('newMessage', message => setMessages([...messages, message]));
    socket.on('message', message => setMessages([...messages, message]));

    useEffect(async () => {
        try {
            const data = await fetch(userData.links.chats).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            socket.emit('join', {userId: userData.id})
            setChatsList(data);
            setChat(data[0] || {});
        } catch(err) {
            setError('Failed to grab all chats')
        }
    }, [userData]);

    async function handleChatClick(chat){
        try {
            const data = await fetch(chat.links.messages).then(response => {
                if(response.ok){
                    return response.json();
                }
            });
            setChat(chat);
            setMessages(data);
        } catch(err) {
            setError('Failed to display chat');
        }
    }

    function handleSendMessage(){
        socket.emit('message', {senderId: chat.senderId, recipientId: chat.recipientId,
            chatId: chat.id, message});
        setMessage('');
    }

    function renderChatsList(){
        return chatsList.map(chat => {
            return (
                <div>
                    <h3>{chat.recipientName}</h3>
                    <button onClick={() => handleChatClick(chat)}>Select</button>
                </div>
            );
        });
    }

    function renderSpecificChat(){
        return (
            <div>
                <h2>{chat.recipientName}</h2>
                <div>
                    {messages.map(message => {
                        return (
                            <div>
                                <br/>
                                {message.message}
                            </div>
                        );
                    })}
                </div>
                <br/>
                <input value={message} onChange={e => setMessage(e.target.value)}/>
                <button onClick={handleSendMessage}>Send</button>
            </div>
        );
    }

    return (
        <div>
            {renderChatsList()}
            <br/>
            {renderSpecificChat()}
        </div>
    )

}