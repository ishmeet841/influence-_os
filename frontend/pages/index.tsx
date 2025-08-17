
import { useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Home() {
  const [profile, setProfile] = useState({ name:'', headline:'', role:'', industry:'', interests:'', voice:'' });
  const [topic, setTopic] = useState('AI marketing tips for beginners');
  const [ideas, setIdeas] = useState<string[]>([]);
  const [content, setContent] = useState('');
  const [scheduledAt, setScheduledAt] = useState('');
  const [analytics, setAnalytics] = useState<any>(null);

  const saveProfile = async () => {
    const payload = { ...profile, interests: profile.interests.split(',').map(s=>s.trim()) };
    const r = await axios.post(`${API}/profile/ingest`, payload);
    alert('Profile saved');
  };
  const genIdeas = async () => {
    const r = await axios.post(`${API}/content/ideas`, { topic });
    setIdeas(r.data.ideas || []);
  };
  const schedule = async () => {
    const r = await axios.post(`${API}/content/schedule`, { content, scheduled_at: scheduledAt });
    alert('Scheduled: ' + JSON.stringify(r.data.scheduled));
  };
  const getAnalytics = async () => {
    const r = await axios.get(`${API}/analytics/summary`);
    setAnalytics(r.data);
  };

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Influence OS — LinkedIn Agent (MVP)</h1>

      <section className="p-4 border rounded mb-6">
        <h2 className="text-xl font-semibold mb-2">Profile</h2>
        <div className="grid grid-cols-2 gap-2">
          <input className="border p-2" placeholder="Name" onChange={e=>setProfile(p=>({...p, name:e.target.value}))}/>
          <input className="border p-2" placeholder="Headline" onChange={e=>setProfile(p=>({...p, headline:e.target.value}))}/>
          <input className="border p-2" placeholder="Role" onChange={e=>setProfile(p=>({...p, role:e.target.value}))}/>
          <input className="border p-2" placeholder="Industry" onChange={e=>setProfile(p=>({...p, industry:e.target.value}))}/>
          <input className="border p-2 col-span-2" placeholder="Interests (comma separated)" onChange={e=>setProfile(p=>({...p, interests:e.target.value}))}/>
          <textarea className="border p-2 col-span-2" placeholder="Brand voice" onChange={e=>setProfile(p=>({...p, voice:e.target.value}))}/>
        </div>
        <button className="mt-2 px-3 py-2 border rounded" onClick={saveProfile}>Save Profile</button>
      </section>

      <section className="p-4 border rounded mb-6">
        <h2 className="text-xl font-semibold mb-2">Generate Ideas</h2>
        <input className="border p-2 w-full mb-2" value={topic} onChange={e=>setTopic(e.target.value)}/>
        <button className="px-3 py-2 border rounded" onClick={genIdeas}>Generate</button>
        <ul className="list-disc pl-6 mt-3 space-y-2">
          {ideas.map((it, i)=>(<li key={i} className="whitespace-pre-wrap">{it}</li>))}
        </ul>
      </section>

      <section className="p-4 border rounded mb-6">
        <h2 className="text-xl font-semibold mb-2">Schedule Post</h2>
        <textarea className="border p-2 w-full h-40 mb-2" placeholder="Post content" value={content} onChange={e=>setContent(e.target.value)}/>
        <input className="border p-2 w-full mb-2" type="datetime-local" onChange={e=>setScheduledAt(e.target.value)}/>
        <button className="px-3 py-2 border rounded" onClick={schedule}>Schedule</button>
      </section>

      <section className="p-4 border rounded mb-6">
        <h2 className="text-xl font-semibold mb-2">Analytics</h2>
        <button className="px-3 py-2 border rounded mb-2" onClick={getAnalytics}>Refresh</button>
        {analytics && <pre className="bg-gray-50 p-2 rounded">{JSON.stringify(analytics, null, 2)}</pre>}
      </section>
    </div>
  );
}
