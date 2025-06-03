import { useState } from 'react';
import axios from 'axios';

function Home() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [context, setContext] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/query', {
        query: query.trim()
      });

      setAnswer(response.data.answer);
      setContext(response.data.context);
    } catch (error) {
      setAnswer('⚠️ Error fetching data. Please try again.');
      setContext([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto bg-white shadow-xl rounded-xl p-8 space-y-6">
        <h1 className="text-3xl font-bold text-center text-blue-800">
          RAG Course Catalog Search
        </h1>

        <div className="flex gap-4">
          <input
            type="text"
            className="flex-1 p-3 border border-gray-300 rounded-md shadow-sm"
            placeholder="Enter your academic query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={handleSearch}
            className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700"
            disabled={loading}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        {answer && (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Answer:</h2>
            <p className="bg-green-50 border border-green-200 p-4 rounded-md text-gray-700 whitespace-pre-line">
              {answer}
            </p>
          </div>
        )}

        {context.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Context:</h2>
            <ul className="space-y-2">
              {context.map((doc, idx) => (
                <li key={idx} className="bg-gray-50 border border-gray-200 p-3 rounded-md">
                  <p className="text-gray-800">{doc.text}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    📄 {doc.source}, Page {doc.page}
                  </p>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;
