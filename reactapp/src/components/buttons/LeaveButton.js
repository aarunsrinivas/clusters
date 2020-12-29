import React from 'react';

export function Leave({selfLink, setSelf}){

    const handleClick = () => {
        fetch(selfLink, {
            method: 'POST',
            body: JSON.stringify({action: 'leave'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => setSelf(data));
    }

    return (
        <button onClick={() =>  handleClick()}>Leave</button>
    )
}