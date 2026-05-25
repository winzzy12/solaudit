from typing import List, Dict, Any
from app.agents.base import BaseAgent
from app.models.schemas import Vulnerability, Severity


class AccessControlAgent(BaseAgent):
    """Detects access control vulnerabilities"""
    
    def __init__(self):
        super().__init__(
            name="Access Control Analyzer",
            description="Detects missing modifiers, privilege escalation, and centralization risks"
        )
    
    async def analyze(self, source_code: str, metadata: Dict[str, Any]) -> List[Vulnerability]:
        vulnerabilities = []
        
        prompt = f"""You are a smart contract security expert specializing in access control.

Analyze this contract for access control vulnerabilities:

1. **Missing Access Control**: Critical functions without modifiers
2. **Privilege Escalation**: Users gaining unauthorized permissions
3. **Centralization Risks**: Single admin with excessive power
4. **Incorrect Modifier Logic**: Flawed onlyOwner/onlyRole implementations
5. **Front-running Admin Functions**: Unprotected initialization

Contract:
```solidity
{source_code}
```

For EACH vulnerability, provide JSON:
{{
  "vulnerabilities": [
    {{
      "title": "Missing Access Control on mint()",
      "severity": "critical",
      "location": "Token.sol:78",
      "code_snippet": "function mint(address to, uint256 amount) public {{ ... }}",
      "description": "mint() lacks access control, anyone can mint tokens",
      "impact": "Unlimited token inflation, total value destruction",
      "recommendation": "Add onlyOwner or onlyRole(MINTER_ROLE) modifier",
      "remediation_code": "function mint(address to, uint256 amount) public onlyOwner {{ ... }}",
      "cwe_id": "CWE-284"
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
                    title="Access Control Analysis Failed",
                    severity=Severity.INFO,
                    description=f"Agent error: {str(e)}",
                    location="N/A",
                    code_snippet="",
                    impact="Analysis incomplete",
                    recommendation="Manual review required"
                )
            )
        
        return vulnerabilities
