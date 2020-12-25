import React, {useState, useEffect} from 'react';

export function Test() {
    const [applicants, setApplicants] = useState([])

    useEffect(() => {
        fetch('/applicants').then(response => {
            if(response.ok){
                console.log(response.json())
            }
        }).then(data => setApplicants(data));
    }, [])

    console.log(applicants);

    return (
        <div>
            HELLO
        </div>
    )
}