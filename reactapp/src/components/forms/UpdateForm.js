import React, {useState, useEffect} from 'react';
import {useAuth} from '../../contexts/AuthContext';
import bcrypt from 'bcryptjs';
import TagsInput from 'react-tagsinput';
import '../../styles/Form.css';
import '../../styles/TagsInput.css';
import {
    Form,
    Button
} from 'react-bootstrap';

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

            <h2 className="register-header">Set User Details</h2>

            <Form>
                <Form.Group controlId="cap">
                    <Form.Label>Cap</Form.Label>
                    <Form.Control type="number" step="1" min="1" placeholder="Enter cap" 
                    value={cap} onChange={e => setCap(e.target.value)} />
                </Form.Group>

                <Form.Group controlId="gpa">
                    <Form.Label>GPA</Form.Label>
                    <Form.Control type="number" step="0.01" min="0.00" placeholder="Enter GPA out of 4.0" 
                    value={gpa} onChange={e => setGpa(e.target.value)} />
                </Form.Group>

                Major(s)<TagsInput value={majors} onChange={tags => setMajors(tags)}/>
                <br/>
                Standing(s)<TagsInput value={standings} onChange={tags => setStandings(tags)}/>
                <br/>
                Skills<TagsInput value={skills} onChange={tags => setSkills(tags)}/>
                <br/>
                Interests<TagsInput value={interests} onChange={tags => setInterests(tags)}/>
                <br/>
                Courses<TagsInput value={courses} onChange={tags => setCourses(tags)}/>
                <br/>

                <div className="register-button">
                    <Button variant="primary" disabled={loading} onClick={handleUpdateFeatures} block>Set User Info</Button>
                </div>

            </Form>


        </div>

        // <div>
        //     Cap: <input value={cap} onChange={e => setCap(e.target.value)}/>
        //     <br/>
        //     GPA: <input value={gpa} onChange={e => setGpa(e.target.value)}/>
        //     <br/>
        //     Major: <TagsInput value={majors} onChange={tags => setMajors(tags)}/>
        //     <br/>
        //     Standing: <TagsInput value={standings} onChange={tags => setStandings(tags)}/>
        //     <br/>
        //     Skills: <TagsInput value={skills} onChange={tags => setSkills(tags)}/>
        //     <br/>
        //     Interests: <TagsInput value={interests} onChange={tags => setInterests(tags)}/>
        //     <br/>
        //     Courses: <TagsInput value={courses} onChange={tags => setCourses(tags)}/>
        //     <br/>
        //     <button onClick={handleUpdateFeatures}>Submit</button>
        // </div>
    )
}