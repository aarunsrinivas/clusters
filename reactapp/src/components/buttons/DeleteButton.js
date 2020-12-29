import React from 'react';

export function Delete({selfLink}){

    const handleClick = () => {
        fetch(selfLink, {
            method: 'DELETE',
        }).then(response => console.log('Deleted Successfully'));
    }

    return (
        <button onClick={() =>  handleClick()}>Join</button>
    )
}