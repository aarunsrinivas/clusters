import React from 'react';

export function Join({selfLink, setSelf}){

    const handleClick = () => {
        fetch(selfLink, {
            method: 'POST',
            body: JSON.stringify({action: 'join'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => setSelf(data));
    }

    return (
        <button onClick={() =>  handleClick()}>Join</button>
    )
}