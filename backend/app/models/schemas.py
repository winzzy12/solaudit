from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Chain(str, Enum):
    ETHEREUM = "ethereum"
    BSC = "bsc"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"
    SOLANA = "solana"
    TON = "ton"


class Language(str, Enum):
    SOLIDITY = "solidity"
    RUST = "rust"
    FUNC = "func"


class AnalysisRequest(BaseModel):
    source_code: str = Field(..., description="Smart contract source code")
    language: Language = Field(default=Language.SOLIDITY)
    chain: Chain = Field(default=Chain.ETHEREUM)
    contract_name: Optional[str] = None
    enable_red_team: bool = Field(default=True)
    enable_formal_verification: bool = Field(default=False)


class Vulnerability(BaseModel):
    id: str
    title: str
    severity: Severity
    description: str
    location: str  # file:line or function name
    code_snippet: str
    impact: str
    recommendation: str
    remediation_code: Optional[str] = None
    cwe_id: Optional[str] = None
    references: List[str] = Field(default_factory=list)


class ExploitVector(BaseModel):
    vulnerability_id: str
    attack_scenario: str
    exploit_code: str  # Foundry test
    economic_impact: str
    likelihood: Literal["high", "medium", "low"]


class AgentResult(BaseModel):
    agent_name: str
    execution_time: float
    tokens_used: int
    vulnerabilities: List[Vulnerability]
    status: Literal["success", "failed", "timeout"]
    error: Optional[str] = None


class AnalysisResult(BaseModel):
    job_id: str
    status: Literal["pending", "running", "completed", "failed"]
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results
    agent_results: List[AgentResult] = Field(default_factory=list)
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)
    exploit_vectors: List[ExploitVector] = Field(default_factory=list)
    
    # Metrics
    total_tokens: int = 0
    total_time: float = 0.0
    vulnerability_count: Dict[Severity, int] = Field(default_factory=dict)
    
    # Outputs
    report_pdf_url: Optional[str] = None
    report_markdown_url: Optional[str] = None
    exploit_suite_url: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    mimo_available: bool
    database_available: bool
    redis_available: bool
    agents_loaded: int


class AgentInfo(BaseModel):
    name: str
    description: str
    vulnerability_types: List[str]
    enabled: bool
