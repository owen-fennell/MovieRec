import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function Home() {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    if (!userId) return;
    navigate(`/recommend?userId=${userId}`);
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4">
      <div className="max-w-md w-full text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-3">
          Movie Recommender
        </h1>
        <p className="text-gray-500 mb-8 p-4">
          Enter a user ID to get personalized recommendations
          using three different algorithms.
        </p>
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="number"
            min="1"
            value={userId}
            onChange={e => setUserId(e.target.value)}
            placeholder="Enter user ID (e.g. 1)"
            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors"
          >
            Go
          </button>
        </form>
        <div className="flex gap-4 mt-12 justify-center">
          {['Content-Based', 'Collaborative', 'Hybrid'].map(label => (
            <div key={label} className="px-4 py-2 bg-white rounded-lg border border-gray-200 text-sm text-gray-600 shadow-sm">
              {label}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}