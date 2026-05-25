# SolAudit — AI-Powered Smart Contract Security Analyzer

> 12-agent adversarial security system that performs deep vulnerability analysis, exploit generation, and formal verification on smart contracts. Built for Xiaomi MiMo 100T token plan.

## Why This Exists

Traditional auditing tools catch 40-60% of vulnerabilities. Manual audits are expensive ($50K-200K per protocol) and slow (2-4 weeks). SolAudit combines **12 specialized security agents** with an **adversarial red team** to achieve 85%+ vulnerability detection while generating comprehensive audit reports, exploit PoCs, and remediation code.

This is designed for extreme token consumption. A single DeFi protocol (5 contracts, 2500 LOC) triggers 60+ LLM calls and consumes 3-5M tokens. Continuous security monitoring across a portfolio naturally hits 50-100M tokens per day.

## Architecture — 12 Specialized Security Agents

```
Solidity/Rust/FunC source
   │
   ▼
┌──────────────────────────────────────┐
│  Preprocessor + Multi-chain Parser   │
│  - Detect language (Solidity/Rust/FunC)│
│  - Extract metadata + dependencies    │
│  - Build call graph + state diagram   │
└──────────────────────────────────────┘
   │
   ▼ (parallel fan-out — 12 agents)
┌─────────┬─────────┬─────────┬─────────┐
│Reentrancy│ Access │ Integer │Front-run│
│ Detector│ Control│Overflow │ Scanner │
├─────────┼─────────┼─────────┼─────────┤
│Timestamp│Delegatecall│ Gas  │ Logic  │
│Dependency│  Risk  │Griefing│  Bugs  │
├─────────┼─────────┼─────────┼─────────┤
│ Oracle  │ Upgrade │  MEV   │ Formal │
│Manipulation│Safety│Extractor│Verifier│
└─────────┴─────────┴─────────┴─────────┘
   │
   ▼ (adversarial red team)
┌──────────────────────────────────────┐
│  Red Team Exploit Generator          │
│  - Synthesize attack vectors         │
│  - Generate Foundry exploit tests    │
│  - Estimate economic impact          │
└──────────────────────────────────────┘
   │
   ▼ (synthesis)
┌──────────────────────────────────────┐
│  Audit Report Compiler               │
│  - Severity matrix (Critical→Info)   │
│  - Remediation code patches          │
│  - Gas optimization recommendations  │
│  - PDF + Markdown + JSON outputs     │
└──────────────────────────────────────┘
```

## Features

### Security Analysis
- **Reentrancy Detection:** CEI pattern violations, cross-function reentrancy, read-only reentrancy
- **Access Control:** Missing modifiers, privilege escalation, centralization risks
- **Integer Safety:** Overflow/underflow, unchecked math, precision loss
- **Front-running:** Transaction ordering dependence, sandwich attack vectors
- **Timestamp Manipulation:** Block.timestamp dependencies, miner manipulation
- **Delegatecall Risks:** Storage collision, uninitialized proxies, selfdestruct
- **Gas Griefing:** Unbounded loops, DoS vectors, gas limit attacks
- **Logic Bugs:** State inconsistencies, incorrect assumptions, edge cases
- **Oracle Manipulation:** Price feed attacks, flash loan exploits, stale data
- **Upgrade Safety:** Storage layout conflicts, initialization gaps, proxy patterns
- **MEV Extraction:** Arbitrage opportunities, liquidation risks, value leakage
- **Formal Verification:** Invariant checking, symbolic execution, property testing

### Multi-chain Support
- **EVM:** Solidity (Ethereum, BSC, Polygon, Arbitrum, Optimism, Base)
- **Solana:** Rust/Anchor programs
- **TON:** FunC contracts

### Output Formats
- **Audit Report:** PDF + Markdown with severity matrix
- **Exploit PoCs:** Foundry test files demonstrating vulnerabilities
- **Remediation Patches:** Git-compatible diffs with fixes
- **Gas Optimization:** Line-by-line recommendations
- **Deployment Checklist:** Pre-launch security verification

### Token Consumption Target: 100T/month

| Contract Type | LOC | Estimated Tokens | Analysis Time |
|---|---:|---:|---:|
| Simple ERC-20 | 60 | ~150K | 8 min |
| ERC-721 + marketplace | 500 | ~1.2M | 25 min |
| DeFi protocol (5 contracts) | 2,500 | ~6M | 90 min |
| Complex protocol (15 contracts) | 10,000 | ~25M | 6 hours |
| Continuous monitoring (daily) | 50,000+ | ~100M+ | 24/7 |

## Quick Start

### Backend (FastAPI + PostgreSQL + Redis)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: MIMO_API_KEY=tp-xxxxx, DATABASE_URL, REDIS_URL
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React + TailwindCSS)

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

### Docker Compose (full stack)

```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | System status + provider health |
| `/api/agents` | GET | List all 12 agents + red team |
| `/api/analyze` | POST | Run full security analysis |
| `/api/analyze/{job_id}` | GET | Get analysis status/results |
| `/api/reports/{job_id}/pdf` | GET | Download PDF audit report |
| `/api/reports/{job_id}/exploits` | GET | Download exploit test suite |
| `/api/stats` | GET | Token usage breakdown |
| `/api/history` | GET | Past audit jobs |

## Provider Configuration

All LLM calls via `AsyncOpenAI`. Swap providers in `.env`:

```env
# Xiaomi MiMo 100T Plan (default)
MIMO_BASE_URL=https://token-plan-sgp.xiaomimimo.com/v1
MIMO_API_KEY=tp-xxxxx
MIMO_MODEL=mimo-v2.5-pro

# OpenAI
MIMO_BASE_URL=https://api.openai.com/v1
MIMO_API_KEY=sk-xxxxx
MIMO_MODEL=gpt-4-turbo

# Any OpenAI-compatible endpoint
```

## Repo Layout

```
solaudit/
├── backend/
│   ├── app/
│   │   ├── agents/              # 12 security agents + red team
│   │   │   ├── reentrancy.py
│   │   │   ├── access_control.py
│   │   │   ├── integer_safety.py
│   │   │   ├── frontrun.py
│   │   │   ├── timestamp.py
│   │   │   ├── delegatecall.py
│   │   │   ├── gas_griefing.py
│   │   │   ├── logic_bugs.py
│   │   │   ├── oracle.py
│   │   │   ├── upgrade_safety.py
│   │   │   ├── mev.py
│   │   │   ├── formal_verification.py
│   │   │   └── red_team.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── pipeline.py
│   │   │   ├── preprocessor.py
│   │   │   ├── tracker.py
│   │   │   └── report_generator.py
│   │   ├── models/
│   │   │   ├── schemas.py
│   │   │   └── database.py
│   │   ├── api/
│   │   │   └── routes.py
│   │   └── main.py
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisForm.tsx
│   │   │   ├── ResultsView.tsx
│   │   │   ├── VulnerabilityMatrix.tsx
│   │   │   └── ExploitViewer.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENTS.md               # Agent specifications
│   └── EXAMPLE_AUDIT.md
├── examples/
│   ├── vulnerable_erc20.sol
│   └── defi_protocol/
├── docker-compose.yml
├── .gitignore
└── LICENSE
```

## Roadmap

- [x] 12-agent parallel architecture
- [x] Adversarial red team exploit generation
- [x] Multi-chain support (EVM/Solana/TON)
- [x] PDF + Markdown audit reports
- [x] PostgreSQL audit history
- [ ] Real-time streaming analysis (SSE)
- [ ] GitHub integration (PR comments)
- [ ] Continuous monitoring mode
- [ ] Historical exploit pattern database
- [ ] Formal verification with Z3/SMT solvers
- [ ] Economic impact simulation

## License

MIT — see [LICENSE](./LICENSE)

---

Built for Xiaomi MiMo 100T Token Plan · 2026
