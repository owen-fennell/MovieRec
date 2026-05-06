const ENGINES = [
  { id: 'cbf', label: 'Content-Based', description: 'Based on movie features' },
  { id: 'cf',  label: 'Collaborative', description: 'Based on similar users' },
  { id: 'hybrid', label: 'Hybrid',     description: 'Blend of both' },
];

export default function EngineSelector({ selected, onChange }) {
  return (
    <div className="flex gap-3 flex-wrap">
      {ENGINES.map(engine => (
        <button
          key={engine.id}
          onClick={() => onChange(engine.id)}
          className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors
            ${selected === engine.id
              ? 'bg-blue-600 text-white border-blue-600'
              : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'
            }`}
        >
          <span>{engine.label}</span>
          <span className={`block text-xs font-normal mt-0.5
            ${selected === engine.id ? 'text-blue-100' : 'text-gray-400'}`}>
            {engine.description}
          </span>
        </button>
      ))}
    </div>
  );
}