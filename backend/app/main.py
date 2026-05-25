from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import (
    AnalysisRequest, 
    AnalysisResult, 
    HealthResponse,
    AgentInfo
)
from app.core.pipeline import AnalysisPipeline
from app.core.config import get_settings
from typing import Dict
import asyncio

settings = get_settings()
app = FastAPI(
    title="SolAudit API",
    description="AI-Powered Smart Contract Security Analyzer",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance
pipeline = AnalysisPipeline()

# In-memory job storage (replace with Redis/DB in production)
jobs: Dict[str, AnalysisResult] = {}


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """System health check"""
    
    # Test MiMo connection
    mimo_available = True
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url=settings.mimo_base_url,
            api_key=settings.mimo_api_key
        )
        # Quick test call
        await asyncio.wait_for(
            client.chat.completions.create(
                model=settings.mimo_model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            ),
            timeout=5
        )
    except:
        mimo_available = False
    
    return HealthResponse(
        status="healthy" if mimo_available else "degraded",
        mimo_available=mimo_available,
        database_available=True,  # TODO: actual DB check
        redis_available=True,     # TODO: actual Redis check
        agents_loaded=len(pipeline.security_agents)
    )


@app.get("/api/agents", response_model=list[AgentInfo])
async def list_agents():
    """List all available security agents"""
    
    agents = [
        AgentInfo(
            name="Reentrancy Detector",
            description="Detects CEI violations, cross-function reentrancy, read-only reentrancy",
            vulnerability_types=["Classic Reentrancy", "Cross-function", "Read-only"],
            enabled=True
        ),
        AgentInfo(
            name="Access Control Analyzer",
            description="Missing modifiers, privilege escalation, centralization risks",
            vulnerability_types=["Missing Access Control", "Privilege Escalation", "Centralization"],
            enabled=True
        ),
        AgentInfo(
            name="Integer Safety Analyzer",
            description="Overflow/underflow, unchecked math, precision loss",
            vulnerability_types=["Overflow", "Underflow", "Division Before Multiplication"],
            enabled=True
        ),
        # TODO: Add remaining 9 agents
        AgentInfo(
            name="Front-running Scanner",
            description="Transaction ordering dependence, sandwich attacks",
            vulnerability_types=["TOD", "Sandwich Attack"],
            enabled=False
        ),
        AgentInfo(
            name="Red Team Exploit Generator",
            description="Generates attack vectors and Foundry exploit tests",
            vulnerability_types=["Exploit PoC"],
            enabled=True
        ),
    ]
    
    return agents


@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_contract(request: AnalysisRequest):
    """Run full security analysis on smart contract"""
    
    if not request.source_code.strip():
        raise HTTPException(status_code=400, detail="Source code cannot be empty")
    
    # Prepare metadata
    metadata = {
        "language": request.language.value,
        "chain": request.chain.value,
        "contract_name": request.contract_name
    }
    
    # Run analysis
    result = await pipeline.run_analysis(
        source_code=request.source_code,
        metadata=metadata,
        enable_red_team=request.enable_red_team
    )
    
    # Store result
    jobs[result.job_id] = result
    
    return result


@app.get("/api/analyze/{job_id}", response_model=AnalysisResult)
async def get_analysis_result(job_id: str):
    """Get analysis result by job ID"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/stats")
async def get_stats():
    """Get token usage statistics"""
    
    total_jobs = len(jobs)
    total_tokens = sum(job.total_tokens for job in jobs.values())
    total_vulnerabilities = sum(len(job.vulnerabilities) for job in jobs.values())
    
    return {
        "total_jobs": total_jobs,
        "total_tokens": total_tokens,
        "total_vulnerabilities": total_vulnerabilities,
        "avg_tokens_per_job": total_tokens / total_jobs if total_jobs > 0 else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
