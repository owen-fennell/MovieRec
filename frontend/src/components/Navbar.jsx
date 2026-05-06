import { NavLink } from 'react-router-dom';

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'bg-blue-600 text-white'
        : 'text-gray-600 hover:bg-gray-100'
    }`;

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <span className="font-bold text-gray-800 text-lg">🎬 MovieRec</span>
      <div className="flex gap-2">
        <NavLink to="/"         className={linkClass}>Home</NavLink>
        <NavLink to="/recommend" className={linkClass}>Recommend</NavLink>
        <NavLink to="/compare"   className={linkClass}>Compare</NavLink>
      </div>
    </nav>
  );
}