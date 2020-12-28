import React {useState, useEffect} from 'react'
import io from 'socket.io-client'

// needs to be instantiated elsewhere and exported in
const privateSocket = io.connect('http://127.0.0.1:5000/private')

// does not work yet still many missing pieces
export function Chat({chatLink, chatId}){

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetch(chatLink).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => setMessages(data));
    }, []);

    const handleChange = e => {
        setMessage(e.target.value);
    }

    const handleClick = () => {
        privateSocket.emit('message', {'chat_id': chatId, 'sender_id': senderId,
        'recipient_id': recipientId, 'message': message});
        setMessage('');
    }

    privateSocket.on('new_message', message => {
        setMessages([...messages, message]);
    })

}