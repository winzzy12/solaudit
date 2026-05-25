import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Loader2, AlertTriangle, CheckCircle, Download, Code } from 'lucide-react'
import axios from 'axios'
import VulnerabilityMatrix from '../components/VulnerabilityMatrix'
import ExploitViewer from '../components/ExploitViewer'

export default function Result() {
  const { jobId } = useParams()

  const { data: result, isLoading } = useQuery({
    queryKey: ['result', jobId],
    queryFn: async () => {
      const res = await axios.get(`/api/analyze/${jobId}`)
      return res.data
    },
    refetchInterval: (data) => {
      // Poll setiap 2 detik jika masih running
      return data?.status === 'running' || data?.status === 'pending' ? 2000 : false
    }
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-dark-400 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Loading analysis result...</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="card text-center">
        <AlertTriangle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-white mb-2">Job Not Found</h2>
        <p className="text-gray-400">Job ID: {jobId}</p>
      </div>
    )
  }

  const isRunning = result.status === 'running' || result.status === 'pending'
  const isCompleted = result.status === 'completed'
  const isFailed = result.status === 'failed'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Analysis Result</h1>
            <p className="text-gray-400 font-mono text-sm">Job ID: {jobId}</p>
          </div>
          
          <div className="flex items-center space-x-3">
            {isRunning && (
              <div className="flex items-center space-x-2 text-blue-400">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span className="font-semibold">Running...</span>
              </div>
            )}
            {isCompleted && (
              <div className="flex items-center space-x-2 text-green-400">
                <CheckCircle className="w-5 h-5" />
                <span className="font-semibold">Completed</span>
              </div>
            )}
            {isFailed && (
              <div className="flex items-center space-x-2 text-red-400">
                <AlertTriangle className="w-5 h-5" />
                <span className="font-semibold">Failed</span>
              </div>
            )}
          </div>
        </div>

        {/* Progress */}
        {isRunning && (
          <div className="mt-6">
            <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
              <span>Analyzing contract...</span>
              <span>{result.agent_results?.length || 0} / 12 agents completed</span>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2">
              <div 
                className="bg-dark-400 h-2 rounded-full transition-all duration-500"
                style={{ width: `${((result.agent_results?.length || 0) / 12) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Stats */}
        {isCompleted && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div>
              <p className="text-gray-400 text-sm">Total Time</p>
              <p className="text-2xl font-bold text-white">{result.total_time?.toFixed(1)}s</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Tokens Used</p>
              <p className="text-2xl font-bold text-white">{(result.total_tokens / 1000).toFixed(1)}K</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Vulnerabilities</p>
              <p className="text-2xl font-bold text-white">{result.vulnerabilities?.length || 0}</p>
            </div>
            <div>
              <p className="text-gray-400 text-sm">Exploits Generated</p>
              <p className="text-2xl font-bold text-white">{result.exploit_vectors?.length || 0}</p>
            </div>
          </div>
        )}
      </div>

      {/* Vulnerability Matrix */}
      {isCompleted && result.vulnerabilities && result.vulnerabilities.length > 0 && (
        <VulnerabilityMatrix vulnerabilities={result.vulnerabilities} />
      )}

      {/* No Vulnerabilities */}
      {isCompleted && (!result.vulnerabilities || result.vulnerabilities.length === 0) && (
        <div className="card text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">No Vulnerabilities Found</h2>
          <p className="text-gray-400">Contract passed all security checks</p>
        </div>
      )}

      {/* Exploit Vectors */}
      {isCompleted && result.exploit_vectors && result.exploit_vectors.length > 0 && (
        <ExploitViewer exploits={result.exploit_vectors} />
      )}

      {/* Agent Results */}
      {isCompleted && result.agent_results && (
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-4">Agent Execution Details</h2>
          <div className="space-y-3">
            {result.agent_results.map((agent, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-900 rounded-lg">
                <div className="flex items-center space-x-3">
                  {agent.status === 'success' && <CheckCircle className="w-5 h-5 text-green-500" />}
                  {agent.status === 'failed' && <AlertTriangle className="w-5 h-5 text-red-500" />}
                  {agent.status === 'timeout' && <AlertTriangle className="w-5 h-5 text-yellow-500" />}
                  <span className="text-gray-300 font-medium">{agent.agent_name}</span>
                </div>
                <div className="flex items-center space-x-6 text-sm text-gray-400">
                  <span>{agent.execution_time?.toFixed(2)}s</span>
                  <span>{(agent.tokens_used / 1000).toFixed(1)}K tokens</span>
                  <span>{agent.vulnerabilities?.length || 0} vulns</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Download Reports */}
      {isCompleted && (
        <div className="card">
          <h2 className="text-xl font-semibold text-white mb-4">Download Reports</h2>
          <div className="flex flex-wrap gap-4">
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>PDF Audit Report</span>
            </button>
            <button className="btn-secondary flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Markdown Report</span>
            </button>
            <button className="btn-secondary flex items-center space-x-2">
              <Code className="w-4 h-4" />
              <span>Exploit Test Suite</span>
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
