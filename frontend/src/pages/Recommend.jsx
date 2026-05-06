import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { fetchRecommendations } from '../api/recommendations';
import EngineSelector from '../components/AlgoSelector';
import RecommendationList from '../components/RecommendationList';

export default function Recommend() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [engine, setEngine]             = useState('cbf');
  const [userId, setUserId]             = useState(searchParams.get('userId') || '');
  const [recs, setRecs]                 = useState([]);
  const [loading, setLoading]           = useState(false);
  const [error, setError]               = useState(null);

  // Fetch whenever engine or userId changes
  useEffect(() => {
    if (!userId) return;
    setSearchParams({ userId });
    setLoading(true);
    setError(null);

    fetchRecommendations(engine, userId)
      .then(data => setRecs(data.recommendations))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [engine, userId]);

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Recommendations
      </h2>

      {/* User ID input */}
      <div className="flex gap-3 mb-6 justify-center items-center">
        <input
          type="number"
          min="1"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          placeholder="User ID"
          className="w-40 px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 "
        />
        <span className="text-gray-400 text-sm self-center">
          {userId ? `Showing results for user ${userId}` : 'Enter a user ID'}
        </span>
      </div>

      {/* Engine selector */}
      <div className="mb-6 flex flex-col items-center">
        <p className="text-md font-bold text-gray-800 mb-2">Algorithm</p>
        <EngineSelector selected={engine} onChange={setEngine} />
      </div>

      {/* Results */}
      <RecommendationList
        recommendations={recs}
        loading={loading}
        error={error}
      />
    </div>
  );
}