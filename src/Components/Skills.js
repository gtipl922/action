import React from 'react';
import { Grid, Cell, ProgressBar } from 'react-mdl';

const Skills = ({ skill, progress }) => (
  <Grid>
    <Cell col={4}>
      <p>{skill}</p>
    </Cell>
    <Cell col={8}>
      <ProgressBar progress={progress} />
    </Cell>
  </Grid>
);

export default Skills;
