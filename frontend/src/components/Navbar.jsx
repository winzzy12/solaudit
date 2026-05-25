import { Link } from 'react-router-dom'
import { Shield, Activity } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="bg-dark-200 border-b border-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-dark-400" />
            <span className="text-2xl font-bold text-white">SolAudit</span>
          </Link>
          
          <div className="flex items-center space-x-6">
            <Link to="/" className="text-gray-300 hover:text-white transition-colors">
              Dashboard
            </Link>
            <Link to="/analyze" className="btn-primary">
              Analyze Contract
            </Link>
            <a 
              href="http://localhost:8000/docs" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-300 hover:text-white transition-colors flex items-center space-x-1"
            >
              <Activity className="w-4 h-4" />
              <span>API Docs</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  )
}
