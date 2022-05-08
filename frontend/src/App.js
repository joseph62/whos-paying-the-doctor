import './App.css';
import SearchBar from './SearchBar.js';
import ExportResultsButton from './ExportResults.js';
import ResultList from './ResultList.js';

function App() {
  return (
    <div className="App">
      <div>
        <SearchBar/>
        <ExportResultsButton/>
      </div>
      <div>
        <ResultList/>
      </div>
    </div>
  );
}

export default App;
