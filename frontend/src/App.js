import './App.css';
import { Container, Box, FormGroup, Button, Autocomplete, TextField, Stack, Grid } from '@mui/material'
import { useState } from 'react';

export default function App() {
  const [options, setOptions] = useState([]);

  const onChangeFindOptions = async value => {
    const response = await fetch("http://localhost:8000/suggestions?" + new URLSearchParams({terms: value}))
    const suggestedOptions = await response.json()
    setOptions(suggestedOptions)
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 8 }}>
        <FormGroup>
          <Grid container spacing={2}>
            <Grid item xs={8}>
            <Autocomplete 
              id="search-bar"
              options={options}
              renderInput={(params) => <TextField {...params} 
                label="searchSuggestions"
                onChange={ev => {
                  if (ev.target.value !== "" || ev.target.value !== null) {
                    onChangeFindOptions(ev.target.value);
                  }
                }}
                />}
              />
            </Grid>
            <Grid item xs={4}>
              <Button id="search-button" variant="contained">Search</Button>
              <Button id="export-search-results" variant="contained">Export</Button>
            </Grid>
          </Grid>
        </FormGroup>
      </Box>

    </Container>
  );
};
