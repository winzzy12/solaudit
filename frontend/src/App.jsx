import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Analyze from './pages/Analyze'
import Result from './pages/Result'

function App() {
  return (
    <div className="min-h-screen bg-dark-100">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/result/:jobId" element={<Result />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
