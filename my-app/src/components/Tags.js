/* eslint-disable no-use-before-define */
import React from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles((theme) => ({
  root: {
    width: 500,
    '& > * + *': {
      marginTop: theme.spacing(3),
    },
  },
}));

export default function Tags() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Autocomplete
        multiple
        id="tags-standard"
        options={skills}
        getOptionLabel={(option) => option.skill}
        defaultValue={[skills[1].skill]}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="standard"
            label="Skills"
            placeholder=""  
          />
        )}
      />
    </div>
  );

}

const skills = [
    { skill: 'None' },
    { skill: 'HTML'},
    { skill: 'CSS'},
    { skill: 'JavaScript'},
    { skill: 'React.js'}
];
