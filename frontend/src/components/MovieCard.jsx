export default function MovieCard({ movie, rank }) {
  return (
    <div className="flex items-start gap-4 p-4 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <span className="text-2xl font-bold text-gray-200 w-8 shrink-0">
        {rank}
      </span>
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-gray-800 truncate">{movie.title}</p>
        <div className="flex items-center gap-2 mt-1">
          <div className="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full"
              style={{ width: `${(movie.score * 100).toFixed(0)}%` }}
            />
          </div>
          <span className="text-xs text-gray-400 shrink-0">
            {movie.score.toFixed(3)}
          </span>
        </div>
      </div>
    </div>
  );
}