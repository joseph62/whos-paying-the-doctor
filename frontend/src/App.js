import './App.css';
import { Container, Box, FormGroup, Button, Autocomplete, TextField, Grid, ButtonGroup, List, ListItem, ListItemText, Stack, Link, DialogTitle } from '@mui/material'
import { useState } from 'react';

function searchParams(terms) {
  return "?" + new URLSearchParams({ terms: terms })
}

function suggestionUrl(terms) {
  return "http://localhost:8000/suggestions" + searchParams(terms)
}

function searchResultsUrl(terms) {
  return "http://localhost:8000/search-results" + searchParams(terms)
}

function exportSearchResultsUrl(terms) {
  return "http://localhost:8000/search-results/xls" + searchParams(terms)
}

export default function App() {
  const [options, setOptions] = useState([]);
  const [terms, setTerms] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [exportUrl, setExportUrl] = useState([]);

  const onChangeFindOptions = async value => {
    const response = await fetch(suggestionUrl(value));
    const suggestedOptions = await response.json();
    setOptions(suggestedOptions);
  }

  const onSearchClickDoSearch = async value => {
    const response = await fetch(searchResultsUrl(terms));
    const results = await response.json();
    setSearchResults(results);
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 8 }}>
        <DialogTitle>Open Payments: 2015 General Payments Search Tool</DialogTitle>
        <Stack>
          <FormGroup>
            <Grid container spacing={2}>
              <Grid item xs={10}>
                <Autocomplete
                  id="search-bar"
                  filterOptions={(options, _) => options}
                  options={options}
                  renderInput={(params) => <TextField {...params}
                    label="No search terms yet..."
                    onChange={ev => {
                      setTerms(ev.target.value)
                      if (ev.target.value !== "" || ev.target.value !== null) {
                        onChangeFindOptions(ev.target.value);
                        setExportUrl(exportSearchResultsUrl(ev.target.value))
                      }
                    }}
                  />}
                />
              </Grid>
              <Grid item xs={2}>
                <ButtonGroup>
                  <Button id="search-button" onClick={ev => {
                    onSearchClickDoSearch(terms)
                  }}
                    variant="contained">
                    Search
                  </Button>
                  <Button id="export-search-results" href={exportUrl} target="_blank">Export</Button>
                </ButtonGroup>
              </Grid>
            </Grid>
          </FormGroup>
          <List>
            {searchResults.map(result => {
              return (
                <ListItem>
                  <ListItemText>{result._all}</ListItemText>
                </ListItem>
              )
            })}
          </List>
        </Stack>
      </Box>

    </Container>
  );
};
