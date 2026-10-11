export const API_URL =
  import.meta.env.VITE_API_URL || "https://resume-analyzer-career-assistant.onrender.com";
async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.details || data.error || 'Request failed. Please try again.');
  return data;
}
export const analyzeResume = (file) => { const body = new FormData(); body.append('resume', file); return request('/analyze', { method: 'POST', body }); };
export const getHistory = () => request('/history');
export const getAnalysis = (id) => request(`/history/${id}`);
export const deleteAnalysis = (id) => request(`/history/${id}`, { method: 'DELETE' });
export const getRoadmap = (career) => request(`/roadmap/${encodeURIComponent(career)}`);
export { API };
