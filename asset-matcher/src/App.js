import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [assets, setAssets] = useState([]);
  const [search, setSearch] = useState('');
  const [result, setResult] = useState(null);
  const [page, setPage] = useState(1);
  const [perPage] = useState(5); // Set items per page
  const [totalAssets, setTotalAssets] = useState(0); // Total number of assets

  useEffect(() => {
    // Fetch paginated assets when the component mounts or when the page changes
    fetchAssets();
  }, [page]);

  const fetchAssets = () => {
    axios.get(`http://localhost:5000/assets?page=${page}&per_page=${perPage}`)
      .then(response => {
        setAssets(response.data.assets);
        setTotalAssets(response.data.total);
      })
      .catch(error => {
        console.error('Error fetching assets:', error);
      });
  };

  const handleSearch = (event) => {
    setSearch(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/match', { search });
      setResult(response.data?.['IP Address'] ? response.data : null);
    } catch (error) {
      console.error('Error during search request:', error);
      setResult(null);
    }
  };

  const handleNextPage = () => {
    if (page < Math.ceil(totalAssets / perPage)) {
      setPage(page + 1);
    }
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  return (
    <div className="App">
      <h1>Assets Table</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={search}
          onChange={handleSearch}
          placeholder="Search for assets..."
        />
        <button type="submit">Search</button>
      </form>

      {result ? (
        <table>
          <thead>
            <tr>
              <th>IP Address</th>
              <th>Model</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{result['IP Address']}</td>
              <td>{result['Model']}</td>
              <td>{result['Name']}</td>
            </tr>
          </tbody>
        </table>
      ) : search ? (
        <p>No Asset Found</p>
      ) : (
        <div>
          <table>
            <thead>
              <tr>
                <th>IP Address</th>
                <th>Model</th>
                <th>Name</th>
              </tr>
            </thead>
            <tbody>
              {assets.map((asset, index) => (
                <tr key={index}>
                  <td>{asset['IP Address']}</td>
                  <td>{asset['Model']}</td>
                  <td>{asset['Name']}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div>
            <button onClick={handlePreviousPage} disabled={page === 1}>
              Previous
            </button>
            <button onClick={handleNextPage} disabled={page === Math.ceil(totalAssets / perPage)}>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;