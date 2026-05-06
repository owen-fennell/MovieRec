import MovieCard from './MovieCard';
import LoadingSpinner from './LoadingSpinner';

export default function RecommendationList({ recommendations, loading, error }) {
  if (loading) return <LoadingSpinner />;

  if (error) return (
    <div className="text-center py-12 text-red-500">
      <p className="font-medium">Something went wrong</p>
      <p className="text-sm mt-1 text-red-400">{error}</p>
    </div>
  );

  if (!recommendations.length) return (
    <div className="text-center py-12 text-gray-400">
      No recommendations yet — enter a user ID above to get started.
    </div>
  );

  return (
    <div className="flex flex-col gap-3">
      {recommendations.map((movie, i) => (
        <MovieCard key={movie.movieId} movie={movie} rank={i + 1} />
      ))}
    </div>
  );
}