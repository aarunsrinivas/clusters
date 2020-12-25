import React, {useState, useEffect} from 'react';

export function Test() {
    const [applicants, setApplicants] = useState([])

    useEffect(() => {
        fetch('/applicants').then(response => {
            if(response.ok){
                return response.json();
            }
        }).then(data => setApplicants(data));
    }, [])

    return (
        <div>
            {applicants.map(a => {
                return (
                    <u1 key={a.id}>
                        <l1>{a.id}</l1>
                    </u1>
                );
            })}
        </div>
    )
}