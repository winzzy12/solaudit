from typing import List, Dict, Any
from app.agents.base import BaseAgent
from app.models.schemas import Vulnerability, Severity


class ReentrancyAgent(BaseAgent):
    """Detects reentrancy vulnerabilities"""
    
    def __init__(self):
        super().__init__(
            name="Reentrancy Detector",
            description="Detects CEI violations, cross-function reentrancy, and read-only reentrancy"
        )
    
    async def analyze(self, source_code: str, metadata: Dict[str, Any]) -> List[Vulnerability]:
        vulnerabilities = []
        
        prompt = f"""You are a smart contract security expert specializing in reentrancy attacks.

Analyze this Solidity contract for ALL types of reentrancy vulnerabilities:

1. **Classic Reentrancy**: External calls before state updates (CEI pattern violation)
2. **Cross-function Reentrancy**: State shared between functions with external calls
3. **Read-only Reentrancy**: View functions called during state inconsistency
4. **Cross-contract Reentrancy**: Reentrancy through multiple contracts

Contract:
```solidity
{source_code}
```

For EACH vulnerability found, provide:
- Function name and line number
- Exact code snippet (5-10 lines)
- Attack scenario with step-by-step exploit
- Economic impact estimation
- Remediation code using ReentrancyGuard or CEI pattern
- CWE-107 reference

Output format (JSON):
{{
  "vulnerabilities": [
    {{
      "title": "Classic Reentrancy in withdraw()",
      "severity": "critical",
      "location": "Contract.sol:45-52",
      "code_snippet": "...",
      "description": "...",
      "impact": "Attacker can drain entire contract balance",
      "recommendation": "Apply CEI pattern: update state before external call",
      "remediation_code": "...",
      "cwe_id": "CWE-107"
    }}
  ]
}}

If no vulnerabilities found, return {{"vulnerabilities": []}}"""

        try:
            response = await self._call_llm([
                {"role": "system", "content": "You are a security auditor. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ])
            
            # Parse JSON response
            import json
            result = json.loads(response)
            
            for vuln in result.get("vulnerabilities", []):
                vulnerabilities.append(
                    self._create_vulnerability(
                        title=vuln["title"],
                        severity=Severity(vuln["severity"]),
                        description=vuln["description"],
                        location=vuln["location"],
                        code_snippet=vuln["code_snippet"],
                        impact=vuln["impact"],
                        recommendation=vuln["recommendation"],
                        remediation_code=vuln.get("remediation_code"),
                        cwe_id=vuln.get("cwe_id")
                    )
                )
        
        except Exception as e:
            # Fallback: create error vulnerability
            vulnerabilities.append(
                self._create_vulnerability(
                    title="Reentrancy Analysis Failed",
                    severity=Severity.INFO,
                    description=f"Agent error: {str(e)}",
                    location="N/A",
                    code_snippet="",
                    impact="Analysis incomplete",
                    recommendation="Manual review required"
                )
            )
        
        return vulnerabilities
