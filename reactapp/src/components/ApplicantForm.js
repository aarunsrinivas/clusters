import React from 'react';

function ApplicantForm() {

    function handleOnClick(e) {
        e.preventDefault();
        console.log("Submitted");
    }


    return(
        <div className='container'>
            <h2>Student Application</h2>
            <form>
                <fieldset>
                    <label>
                        <p>First Name:</p>
                        <input name="first_name" />
                    </label>
                    <label>
                        <p>Last Name:</p>
                        <input name="last_name" />
                    </label>
                    <label>
                        <p>Major:</p>
                        <input name="major" />
                    </label>
                    <label>
                        <p>Standing:</p>
                        <input name="standing" />
                    </label>
                    <label>
                        <p>GPA:</p>
                        <input name="gpa" />
                    </label>
                    <label>
                        <p>Skills:</p>
                        <input name="skills" />
                    </label>
                </fieldset>
                <button type="submit" onClick={handleOnClick}>Submit</button>
            </form>
        </div>
    )
}

export default ApplicantForm;