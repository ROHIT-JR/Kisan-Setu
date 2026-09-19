import { Routes, Route, Link } from 'react-router-dom'
import FarmerApp from './pages/FarmerApp.jsx'
import OfficerDashboard from './pages/OfficerDashboard.jsx'
import AddDistrict from './pages/AddDistrict.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-stone-50 text-stone-900">
      <nav className="flex gap-4 border-b border-stone-200 px-6 py-3 text-sm">
        <Link to="/" className="font-semibold text-green-700">Kisan Setu</Link>
        <Link to="/">Farmer</Link>
        <Link to="/officer">Officer Dashboard</Link>
        <Link to="/officer/add-district">Add District</Link>
      </nav>
      <Routes>
        <Route path="/" element={<FarmerApp />} />
        <Route path="/officer" element={<OfficerDashboard />} />
        <Route path="/officer/add-district" element={<AddDistrict />} />
      </Routes>
    </div>
  )
}
