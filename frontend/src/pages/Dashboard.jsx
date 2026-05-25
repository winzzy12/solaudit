import { useQuery } from '@tanstack/react-query'
import { BarChart3, FileCode, AlertTriangle, Clock } from 'lucide-react'
import axios from 'axios'

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const res = await axios.get('/api/stats')
      return res.data
    }
  })

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const res = await axios.get('/api/health')
      return res.data
    }
  })

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">AI-Powered Smart Contract Security Analyzer</p>
      </div>

      {/* System Status */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">System Status</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${health?.mimo_available ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-gray-300">MiMo API</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${health?.database_available ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-gray-300">Database</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${health?.redis_available ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-gray-300">Redis</span>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-gray-300">{health?.agents_loaded || 0} Agents Loaded</span>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Jobs</p>
              <p className="text-3xl font-bold text-white mt-1">{stats?.total_jobs || 0}</p>
            </div>
            <FileCode className="w-12 h-12 text-dark-400" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Tokens Used</p>
              <p className="text-3xl font-bold text-white mt-1">
                {stats?.total_tokens ? (stats.total_tokens / 1000000).toFixed(2) + 'M' : '0'}
              </p>
            </div>
            <BarChart3 className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Vulnerabilities Found</p>
              <p className="text-3xl font-bold text-white mt-1">{stats?.total_vulnerabilities || 0}</p>
            </div>
            <AlertTriangle className="w-12 h-12 text-yellow-500" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg Tokens/Job</p>
              <p className="text-3xl font-bold text-white mt-1">
                {stats?.avg_tokens_per_job ? (stats.avg_tokens_per_job / 1000).toFixed(1) + 'K' : '0'}
              </p>
            </div>
            <Clock className="w-12 h-12 text-green-500" />
          </div>
        </div>
      </div>

      {/* Quick Start */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Quick Start</h2>
        <div className="space-y-4">
          <div className="flex items-start space-x-4">
            <div className="bg-dark-400 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">1</div>
            <div>
              <h3 className="font-semibold text-white">Upload Contract</h3>
              <p className="text-gray-400 text-sm">Paste Solidity source code atau upload file .sol</p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="bg-dark-400 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">2</div>
            <div>
              <h3 className="font-semibold text-white">Run Analysis</h3>
              <p className="text-gray-400 text-sm">12 security agents analyze contract secara paralel</p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="bg-dark-400 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold flex-shrink-0">3</div>
            <div>
              <h3 className="font-semibold text-white">Review Results</h3>
              <p className="text-gray-400 text-sm">Vulnerability matrix, exploit PoCs, dan audit report</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
