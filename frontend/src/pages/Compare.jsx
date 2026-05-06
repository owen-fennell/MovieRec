import { useState } from 'react';
import { fetchRecommendations } from '../api/recommendations';
import RecommendationList from '../components/RecommendationList';

const ENGINES = [
  { id: 'cbf',    label: 'Content-Based', color: 'blue' },
  { id: 'cf',     label: 'Collaborative', color: 'purple' },
  { id: 'hybrid', label: 'Hybrid',        color: 'green' },
];

const colorMap = {
  blue:   'bg-blue-600',
  purple: 'bg-purple-600',
  green:  'bg-green-600',
};

export default function Compare() {
  const [userId, setUserId]   = useState('');
  const [results, setResults] = useState({ cbf: [], cf: [], hybrid: [] });
  const [loading, setLoading] = useState({ cbf: false, cf: false, hybrid: false });
  const [errors, setErrors]   = useState({ cbf: null, cf: null, hybrid: null });

  function handleCompare() {
    if (!userId) return;

    // Set all three engines to loading simultaneously
    setLoading({ cbf: true, cf: true, hybrid: true });
    setErrors({ cbf: null, cf: null, hybrid: null });

    // Fire all three requests in parallel
    ENGINES.forEach(({ id }) => {
      fetchRecommendations(id, userId, 10)
        .then(data => {
          setResults(prev => ({ ...prev, [id]: data.recommendations }));
        })
        .catch(err => {
          setErrors(prev => ({ ...prev, [id]: err.message }));
        })
        .finally(() => {
          setLoading(prev => ({ ...prev, [id]: false }));
        });
    });
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-2">
        Compare Engines
      </h2>
      <p className="text-gray-500 mb-6 p-4">
        See how each algorithm ranks movies differently for the same user.
      </p>

      {/* User ID input + trigger */}
      <div className="flex gap-3 mb-8 justify-center items-center">
        <input
          type="number"
          min="1"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          placeholder="Enter user ID"
          className="w-48 px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
        />
        <button
          onClick={handleCompare}
          disabled={!userId}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Compare all three
        </button>
      </div>

      {/* Three columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {ENGINES.map(({ id, label, color }) => (
          <div key={id} className="flex flex-col">
            <div className={`${colorMap[color]} text-white px-4 py-3 rounded-t-xl`}>
              <p className="font-semibold">{label}</p>
              <p className="text-xs opacity-80 mt-0.5">
                {id === 'cbf'    && 'Recommends based on movie features'}
                {id === 'cf'     && 'Recommends based on similar users'}
                {id === 'hybrid' && 'Blends both approaches'}
              </p>
            </div>
            <div className="flex-1 bg-gray-50 rounded-b-xl p-4 border border-gray-100 border-t-0">
              <RecommendationList
                recommendations={results[id]}
                loading={loading[id]}
                error={errors[id]}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}