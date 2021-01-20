import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs';
import TagsInput from 'react-tagsinput';

export function UpdateForm() {

    const {userData, updateFeatures} = useAuth();
    const [cap, setCap] = useState(userData.cap);
    const [gpa, setGpa] = useState(userData.features.gpa);
    const [majors, setMajors] = useState(userData.features.majors);
    const [standings, setStandings] = useState(userData.features.standings);
    const [skills, setSkills] = useState(userData.features.skills);
    const [interests, setInterests] = useState(userData.features.interests)
    const [courses, setCourses] = useState(userData.features.courses)
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    async function handleUpdateFeatures() {
        try {
            setError('Updated Features');
            setLoading(true);
            if(!cap || !gpa || !majors.length || !standings.length || !skills.length || !interests.length || !courses.length) {
               throw 'Fields not filled out';
            }
            await updateFeatures(cap, gpa, majors, standings, skills, interests, courses);
        } catch(err) {
            setError(err);
        }
        setLoading(false);
    }

    return (
        <div>
            Cap: <input value={cap} onChange={e => setCap(e.target.value)}/>
            <br/>
            GPA: <input value={gpa} onChange={e => setGpa(e.target.value)}/>
            <br/>
            Major: <TagsInput value={majors} onChange={tags => setMajors(tags)}/>
            <br/>
            Standing: <TagsInput value={standings} onChange={tags => setStandings(tags)}/>
            <br/>
            Skills: <TagsInput value={skills} onChange={tags => setSkills(tags)}/>
            <br/>
            Interests: <TagsInput value={interests} onChange={tags => setInterests(tags)}/>
            <br/>
            Courses: <TagsInput value={courses} onChange={tags => setCourses(tags)}/>
            <br/>
            <button onClick={handleUpdateFeatures}>Submit</button>
        </div>
    )
}