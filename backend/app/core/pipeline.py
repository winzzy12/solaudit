import asyncio
import time
from typing import List, Dict, Any
from app.agents.reentrancy import ReentrancyAgent
from app.agents.access_control import AccessControlAgent
from app.agents.integer_safety import IntegerSafetyAgent
from app.agents.red_team import RedTeamAgent
from app.models.schemas import AgentResult, AnalysisResult, Vulnerability, ExploitVector, Severity
from datetime import datetime
import uuid


class AnalysisPipeline:
    """Orchestrates parallel agent execution"""
    
    def __init__(self):
        # Initialize all 12 agents (3 implemented, 9 placeholders)
        self.security_agents = [
            ReentrancyAgent(),
            AccessControlAgent(),
            IntegerSafetyAgent(),
            # TODO: Add remaining 9 agents
            # FrontrunAgent(),
            # TimestampAgent(),
            # DelegatecallAgent(),
            # GasGriefingAgent(),
            # LogicBugsAgent(),
            # OracleAgent(),
            # UpgradeSafetyAgent(),
            # MEVAgent(),
            # FormalVerificationAgent(),
        ]
        self.red_team = RedTeamAgent()
    
    async def run_analysis(
        self, 
        source_code: str, 
        metadata: Dict[str, Any],
        enable_red_team: bool = True
    ) -> AnalysisResult:
        """Run full security analysis pipeline"""
        
        job_id = str(uuid.uuid4())
        start_time = time.time()
        
        result = AnalysisResult(
            job_id=job_id,
            status="running",
            created_at=datetime.utcnow()
        )
        
        try:
            # Phase 1: Run all security agents in parallel
            agent_tasks = [
                self._run_agent(agent, source_code, metadata)
                for agent in self.security_agents
            ]
            
            agent_results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # Collect results
            all_vulnerabilities = []
            total_tokens = 0
            
            for agent_result in agent_results:
                if isinstance(agent_result, Exception):
                    continue
                
                result.agent_results.append(agent_result)
                all_vulnerabilities.extend(agent_result.vulnerabilities)
                total_tokens += agent_result.tokens_used
            
            # Phase 2: Red team exploit generation (if enabled)
            exploit_vectors = []
            if enable_red_team and all_vulnerabilities:
                vuln_dicts = [
                    {
                        "id": v.id,
                        "title": v.title,
                        "severity": v.severity.value,
                        "description": v.description,
                        "location": v.location
                    }
                    for v in all_vulnerabilities
                ]
                
                exploit_vectors = await self.red_team.generate_exploits(
                    source_code, 
                    vuln_dicts
                )
                total_tokens += self.red_team.tokens_used
            
            # Finalize result
            result.vulnerabilities = all_vulnerabilities
            result.exploit_vectors = exploit_vectors
            result.total_tokens = total_tokens
            result.total_time = time.time() - start_time
            result.status = "completed"
            result.completed_at = datetime.utcnow()
            
            # Count vulnerabilities by severity
            result.vulnerability_count = {
                Severity.CRITICAL: sum(1 for v in all_vulnerabilities if v.severity == Severity.CRITICAL),
                Severity.HIGH: sum(1 for v in all_vulnerabilities if v.severity == Severity.HIGH),
                Severity.MEDIUM: sum(1 for v in all_vulnerabilities if v.severity == Severity.MEDIUM),
                Severity.LOW: sum(1 for v in all_vulnerabilities if v.severity == Severity.LOW),
                Severity.INFO: sum(1 for v in all_vulnerabilities if v.severity == Severity.INFO),
            }
        
        except Exception as e:
            result.status = "failed"
            result.completed_at = datetime.utcnow()
            result.total_time = time.time() - start_time
        
        return result
    
    async def _run_agent(self, agent, source_code: str, metadata: Dict[str, Any]) -> AgentResult:
        """Run single agent with timeout and error handling"""
        start_time = time.time()
        
        try:
            vulnerabilities = await asyncio.wait_for(
                agent.analyze(source_code, metadata),
                timeout=300  # 5 min timeout
            )
            
            return AgentResult(
                agent_name=agent.name,
                execution_time=time.time() - start_time,
                tokens_used=agent.tokens_used,
                vulnerabilities=vulnerabilities,
                status="success"
            )
        
        except asyncio.TimeoutError:
            return AgentResult(
                agent_name=agent.name,
                execution_time=time.time() - start_time,
                tokens_used=agent.tokens_used,
                vulnerabilities=[],
                status="timeout",
                error="Agent exceeded 5 minute timeout"
            )
        
        except Exception as e:
            return AgentResult(
                agent_name=agent.name,
                execution_time=time.time() - start_time,
                tokens_used=agent.tokens_used,
                vulnerabilities=[],
                status="failed",
                error=str(e)
            )
