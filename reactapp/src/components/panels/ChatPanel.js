import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import io from 'socket.io-client';
import '../../styles/Chat.css';
import {
    InputGroup,
    FormControl,
    Button
} from 'react-bootstrap';

const socket = io.connect(`${process.env.REACT_APP_BACKEND_URL}/messaging`)

export function ChatPanel(){

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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${userData.links.chats}`).then(response => {
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
            const data = await fetch(`${process.env.REACT_APP_BACKEND_URL}${chat.links.messages}`).then(response => {
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
                <div className="single-recipient-container">
                    <h4>{chat.recipientName}</h4>
                    <Button variant="primary" onClick={() => handleChatClick(chat)}> Select</Button>
                </div>
            );
        });
    }

    function renderSpecificChat(){
        return (
            <div className="chat-container">
                <h2 className="recipient-name">{chat.recipientName}</h2>
                <hr/>
                <div className="specific-chat-container">
                    {messages.map(message => {
                        // console.log("User ID: " + userData.id); 
                        // console.log("Message Origin: " + message.origin)
                        if (userData.id == message.origin) {
                            return (
                                <div>
                                    <p className="sent-message">{message.message}</p>
                                </div>
                            );
                        }
                        return (
                            <div className="received-message">
                                {message.message}
                            </div>
                        );
                    })}
                </div>
                <br/>
                <InputGroup className="mb-3">
                    <FormControl
                    placeholder="Enter message"
                    aria-label="Enter message"
                    aria-describedby="basic-addon2"
                    value={message} 
                    onChange={e => setMessage(e.target.value)}
                    />
                    <InputGroup.Append>
                        <Button variant="secondary" onClick={handleSendMessage}>Send</Button>
                    </InputGroup.Append>
                </InputGroup>
                {/* <input value={message} onChange={e => setMessage(e.target.value)}/>
                <button onClick={handleSendMessage}>Send</button> */}
            </div>
        );
    }

    function renderIfChat() {
        if (chatsList.length == 0) {
            return (
                <h4>You have no chats yet!</h4>
            );
        }
        return (
            <div className="entire-chat-container">
                {renderSpecificChat()}
    
                <div className="all-recipients-container">
                    <h2>Contacts</h2>
                    {renderChatsList()}
                </div>
    
            </div>
        );
    }

    return (
        <div>
            {renderIfChat()}
        </div>
    );

}