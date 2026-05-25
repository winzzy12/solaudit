from typing import List, Dict, Any
from app.agents.base import BaseAgent
from app.models.schemas import Vulnerability, Severity


class IntegerSafetyAgent(BaseAgent):
    """Detects integer overflow/underflow and arithmetic issues"""
    
    def __init__(self):
        super().__init__(
            name="Integer Safety Analyzer",
            description="Detects overflow/underflow, unchecked math, and precision loss"
        )
    
    async def analyze(self, source_code: str, metadata: Dict[str, Any]) -> List[Vulnerability]:
        vulnerabilities = []
        
        prompt = f"""You are a smart contract security expert specializing in arithmetic vulnerabilities.

Analyze this contract for integer safety issues:

1. **Overflow/Underflow**: Unchecked arithmetic operations (Solidity <0.8.0)
2. **Unchecked Blocks**: Dangerous use of unchecked {{ }} in Solidity >=0.8.0
3. **Division Before Multiplication**: Precision loss in calculations
4. **Zero Division**: Missing checks before division
5. **Type Casting Issues**: Unsafe downcasting (uint256 → uint8)

Contract:
```solidity
{source_code}
```

For EACH vulnerability, provide JSON:
{{
  "vulnerabilities": [
    {{
      "title": "Integer Overflow in calculateReward()",
      "severity": "high",
      "location": "Staking.sol:123",
      "code_snippet": "reward = amount * multiplier;",
      "description": "Unchecked multiplication can overflow",
      "impact": "Incorrect reward calculation, potential fund loss",
      "recommendation": "Use SafeMath or check Solidity version >=0.8.0",
      "remediation_code": "reward = amount.mul(multiplier); // SafeMath",
      "cwe_id": "CWE-190"
    }}
  ]
}}"""

        try:
            response = await self._call_llm([
                {"role": "system", "content": "You are a security auditor. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ])
            
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
            vulnerabilities.append(
                self._create_vulnerability(
                    title="Integer Safety Analysis Failed",
                    severity=Severity.INFO,
                    description=f"Agent error: {str(e)}",
                    location="N/A",
                    code_snippet="",
                    impact="Analysis incomplete",
                    recommendation="Manual review required"
                )
            )
        
        return vulnerabilities
