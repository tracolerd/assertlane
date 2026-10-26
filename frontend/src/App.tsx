import { useEffect, useState } from 'react';
import { api } from './api';
interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
}
function App() {
  const [status, setStatus] = useState<string>('Checking backend...');
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const fetchProjects = () => {
    api.get('/api/projects/')
      .then(res => setProjects(res.data))
      .catch(() => setStatus('Could not load projects. Check API availability and CORS.'));
  };
  useEffect(() => {
    api.get('/api/health')
      .then(res => {
        setStatus(res.data.message);
        fetchProjects();
      })
      .catch(() => setStatus('Backend offline or CORS error. Check VITE_API_BASE_URL.'));
  }, []);
  const handleCreateProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    api.post('/api/projects/', { name, description })
      .then(() => {
        setName('');
        setDescription('');
        fetchProjects();
      })
      .catch(() => setStatus('Could not create project. Check API availability and request validation.'))
      .finally(() => setLoading(false));
  };
  return (
    <div className="min-h-screen bg-slate-100 text-slate-800 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8">
          <div>
            <h1 className="text-3xl font-extrabold text-blue-600 tracking-tight">AssertLane</h1>
            <p className="text-sm text-slate-500">Quality Engineering & Traceability Dashboard</p>
          </div>
          <div className="inline-flex items-center px-3 py-1 bg-slate-100 rounded-full text-xs font-semibold">
            <span className={`w-2.5 h-2.5 rounded-full mr-2 ${status.includes('operational') ? 'bg-green-500' : 'bg-red-500 animate-pulse'}`}></span>
            {status}
          </div>
        </div>
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Create Project Form */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 h-fit">
            <h2 className="text-lg font-bold text-slate-700 mb-4">Create New Project</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase text-slate-500 mb-1">Project Name</label>
                <input 
                  type="text" 
                  value={name} 
                  onChange={e => setName(e.target.value)} 
                  placeholder="e.g. Core Banking QA" 
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-semibold uppercase text-slate-500 mb-1">Description</label>
                <textarea 
                  value={description} 
                  onChange={e => setDescription(e.target.value)} 
                  placeholder="Optional details..." 
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                  rows={3}
                />
              </div>
              <button 
                type="submit" 
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-lg transition text-sm shadow-sm"
              >
                {loading ? 'Creating...' : 'Create Project'}
              </button>
            </form>
          </div>
          {/* Project List */}
          <div className="md:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-lg font-bold text-slate-700 mb-4">Projects ({projects.length})</h2>
            {projects.length === 0 ? (
              <p className="text-slate-400 text-sm italic">No projects found. Create your first project on the left.</p>
            ) : (
              <div className="space-y-3">
                {projects.map(p => (
                  <div key={p.id} className="p-4 border border-slate-100 bg-slate-50 rounded-lg hover:shadow-sm transition">
                    <h3 className="font-bold text-blue-600 text-base">{p.name}</h3>
                    <p className="text-slate-600 text-sm mt-1">{p.description || 'No description provided.'}</p>
                    <div className="mt-3 text-xs text-slate-400 flex justify-between items-center border-t border-slate-200 pt-2">
                      <span>ID: {p.id.slice(0, 8)}...</span>
                      <span>Created: {new Date(p.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
export default App;
