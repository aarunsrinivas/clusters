import React from 'react';

export function Peel({selfLink, setSelf}){

    const handleClick = () => {
        fetch(selfLink, {
            method: 'POST',
            body: JSON.stringify({action: 'peel'})
        }).then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => setSelf(data));
    }

    return (
        <button onClick={() =>  handleClick()}>Peel</button>
    )
}