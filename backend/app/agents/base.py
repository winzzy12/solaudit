from openai import AsyncOpenAI
from typing import List, Dict, Any
from app.core.config import get_settings
from app.models.schemas import Vulnerability, Severity
from tenacity import retry, stop_after_attempt, wait_exponential
import time

settings = get_settings()


class BaseAgent:
    """Base class for all security agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.client = AsyncOpenAI(
            base_url=settings.mimo_base_url,
            api_key=settings.mimo_api_key
        )
        self.tokens_used = 0
        self.execution_time = 0.0
    
    @retry(
        stop=stop_after_attempt(settings.max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.1) -> str:
        """Call LLM with retry logic"""
        response = await self.client.chat.completions.create(
            model=settings.mimo_model,
            messages=messages,
            temperature=temperature,
            max_tokens=4096
        )
        
        self.tokens_used += response.usage.total_tokens
        return response.choices[0].message.content
    
    async def analyze(self, source_code: str, metadata: Dict[str, Any]) -> List[Vulnerability]:
        """Override this in subclasses"""
        raise NotImplementedError
    
    def _create_vulnerability(
        self,
        title: str,
        severity: Severity,
        description: str,
        location: str,
        code_snippet: str,
        impact: str,
        recommendation: str,
        remediation_code: str = None,
        cwe_id: str = None
    ) -> Vulnerability:
        """Helper to create vulnerability objects"""
        return Vulnerability(
            id=f"{self.name.lower().replace(' ', '_')}_{int(time.time() * 1000)}",
            title=title,
            severity=severity,
            description=description,
            location=location,
            code_snippet=code_snippet,
            impact=impact,
            recommendation=recommendation,
            remediation_code=remediation_code,
            cwe_id=cwe_id
        )
