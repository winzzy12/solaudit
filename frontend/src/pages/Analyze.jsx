import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { Upload, FileCode, Loader2 } from 'lucide-react'
import axios from 'axios'

export default function Analyze() {
  const navigate = useNavigate()
  const [sourceCode, setSourceCode] = useState('')
  const [language, setLanguage] = useState('solidity')
  const [chain, setChain] = useState('ethereum')
  const [enableRedTeam, setEnableRedTeam] = useState(true)

  const analyzeMutation = useMutation({
    mutationFn: async (data) => {
      const res = await axios.post('/api/analyze', data)
      return res.data
    },
    onSuccess: (data) => {
      navigate(`/result/${data.job_id}`)
    }
  })

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        setSourceCode(event.target.result)
      }
      reader.readAsText(file)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!sourceCode.trim()) {
      alert('Source code tidak boleh kosong')
      return
    }

    analyzeMutation.mutate({
      source_code: sourceCode,
      language,
      chain,
      enable_red_team: enableRedTeam
    })
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Analyze Contract</h1>
        <p className="text-gray-400">Upload smart contract untuk security analysis</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload */}
        <div className="card">
          <label className="block text-sm font-semibold text-gray-300 mb-3">
            Upload File atau Paste Code
          </label>
          
          <div className="mb-4">
            <label className="flex items-center justify-center w-full h-32 border-2 border-dashed border-gray-700 rounded-lg cursor-pointer hover:border-dark-400 transition-colors">
              <div className="flex flex-col items-center">
                <Upload className="w-8 h-8 text-gray-400 mb-2" />
                <span className="text-sm text-gray-400">Click to upload .sol file</span>
              </div>
              <input 
                type="file" 
                className="hidden" 
                accept=".sol,.rs,.fc"
                onChange={handleFileUpload}
              />
            </label>
          </div>

          <textarea
            value={sourceCode}
            onChange={(e) => setSourceCode(e.target.value)}
            placeholder="// SPDX-License-Identifier: MIT&#10;pragma solidity ^0.8.0;&#10;&#10;contract MyContract {&#10;    // Your code here&#10;}"
            className="w-full h-96 bg-gray-900 text-gray-100 font-mono text-sm p-4 rounded-lg border border-gray-700 focus:border-dark-400 focus:outline-none resize-none"
          />
        </div>

        {/* Configuration */}
        <div className="card">
          <h3 className="text-lg font-semibold text-white mb-4">Configuration</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">
                Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full bg-gray-900 text-gray-100 p-3 rounded-lg border border-gray-700 focus:border-dark-400 focus:outline-none"
              >
                <option value="solidity">Solidity</option>
                <option value="rust">Rust (Solana)</option>
                <option value="func">FunC (TON)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2">
                Chain
              </label>
              <select
                value={chain}
                onChange={(e) => setChain(e.target.value)}
                className="w-full bg-gray-900 text-gray-100 p-3 rounded-lg border border-gray-700 focus:border-dark-400 focus:outline-none"
              >
                <option value="ethereum">Ethereum</option>
                <option value="bsc">BSC</option>
                <option value="polygon">Polygon</option>
                <option value="arbitrum">Arbitrum</option>
                <option value="optimism">Optimism</option>
                <option value="base">Base</option>
                <option value="solana">Solana</option>
                <option value="ton">TON</option>
              </select>
            </div>
          </div>

          <div className="mt-6">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={enableRedTeam}
                onChange={(e) => setEnableRedTeam(e.target.checked)}
                className="w-5 h-5 text-dark-400 bg-gray-900 border-gray-700 rounded focus:ring-dark-400"
              />
              <div>
                <span className="text-gray-300 font-semibold">Enable Red Team Exploit Generation</span>
                <p className="text-sm text-gray-500">Generate Foundry exploit PoCs untuk critical vulnerabilities</p>
              </div>
            </label>
          </div>
        </div>

        {/* Submit */}
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-400">
            <FileCode className="inline w-4 h-4 mr-1" />
            Estimasi: 150K-6M tokens tergantung ukuran contract
          </div>
          
          <button
            type="submit"
            disabled={analyzeMutation.isPending || !sourceCode.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            {analyzeMutation.isPending ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>Start Analysis</span>
              </>
            )}
          </button>
        </div>

        {analyzeMutation.isError && (
          <div className="bg-red-900/20 border border-red-500 text-red-400 p-4 rounded-lg">
            Error: {analyzeMutation.error.message}
          </div>
        )}
      </form>
    </div>
  )
}
