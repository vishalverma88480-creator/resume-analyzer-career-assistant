import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Analysis from './pages/Analysis';
import CareerPaths from './pages/CareerPaths';
import History from './pages/History';

export default function App() {
  return <><Navbar /><main className="app-main"><Routes><Route path="/" element={<Home />} /><Route path="/upload" element={<Upload />} /><Route path="/analysis" element={<Analysis />} /><Route path="/career-paths" element={<CareerPaths />} /><Route path="/history" element={<History />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes></main><footer className="footer"><span className="brand-mark small-mark">R</span><span>ResumeFlow</span><span className="footer-note">Clear insights. Confident next steps.</span></footer></>;
}
