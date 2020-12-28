import React from 'react';
import '../styles/Dashboard.css';
import JobCard from './JobCard';

export default function Dashboard() {
    return (
        <div>
            <h1 className='dash_title'>Dashboard</h1>
            <JobCard />
            <JobCard />
            <JobCard />
        </div>
    )
}
