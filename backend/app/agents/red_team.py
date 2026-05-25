from typing import List, Dict, Any
from app.agents.base import BaseAgent
from app.models.schemas import ExploitVector


class RedTeamAgent(BaseAgent):
    """Adversarial agent that generates exploit PoCs"""
    
    def __init__(self):
        super().__init__(
            name="Red Team Exploit Generator",
            description="Synthesizes attack vectors and generates Foundry exploit tests"
        )
    
    async def generate_exploits(
        self, 
        source_code: str, 
        vulnerabilities: List[Dict[str, Any]]
    ) -> List[ExploitVector]:
        """Generate exploit PoCs for discovered vulnerabilities"""
        
        if not vulnerabilities:
            return []
        
        exploits = []
        
        # Group critical/high severity vulns
        critical_vulns = [v for v in vulnerabilities if v.get("severity") in ["critical", "high"]]
        
        for vuln in critical_vulns[:5]:  # Limit to top 5
            prompt = f"""You are a white-hat security researcher writing exploit PoCs.

Vulnerability:
- Title: {vuln.get('title')}
- Severity: {vuln.get('severity')}
- Description: {vuln.get('description')}
- Location: {vuln.get('location')}

Original Contract:
```solidity
{source_code}
```

Generate a complete Foundry test that demonstrates the exploit:

1. **Attack Scenario**: Step-by-step narrative
2. **Exploit Code**: Full Foundry test with setup, attack, and assertions
3. **Economic Impact**: Estimated loss in USD/ETH
4. **Likelihood**: high/medium/low based on attack complexity

Output JSON:
{{
  "attack_scenario": "1. Attacker deploys malicious contract...",
  "exploit_code": "// SPDX-License-Identifier: MIT\\npragma solidity ^0.8.0;\\n\\nimport \\"forge-std/Test.sol\\";\\n...",
  "economic_impact": "Attacker can drain $500K in single transaction",
  "likelihood": "high"
}}"""

            try:
                response = await self._call_llm([
                    {"role": "system", "content": "You are a security researcher. Output valid JSON only."},
                    {"role": "user", "content": prompt}
                ], temperature=0.2)
                
                import json
                result = json.loads(response)
                
                exploits.append(ExploitVector(
                    vulnerability_id=vuln.get("id", "unknown"),
                    attack_scenario=result["attack_scenario"],
                    exploit_code=result["exploit_code"],
                    economic_impact=result["economic_impact"],
                    likelihood=result["likelihood"]
                ))
            
            except Exception as e:
                # Skip failed exploit generation
                continue
        
        return exploits
