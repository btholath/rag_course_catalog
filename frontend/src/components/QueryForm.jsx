import { useState } from 'react';
import { submitQuery } from '../api';

export default function QueryForm({ onResult }) {
  const [query, setQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await submitQuery(query);
    onResult(res.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Ask about the course catalog..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        required
      />
      <button type="submit">Search</button>
    </form>
  );
}
