# SolAudit - Quick Start Guide

## Prerequisites

- Docker & Docker Compose
- Xiaomi MiMo API Key (Token Plan)

## Setup

1. **Clone & Configure**
```bash
cd /root/solaudit
cp backend/.env.example backend/.env
```

2. **Edit backend/.env**
```bash
nano backend/.env
# Set MIMO_API_KEY=tp-your-key-here
```

3. **Start Services**
```bash
docker-compose up -d
```

4. **Access**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MiMo API key
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Go to http://localhost:5173/analyze
2. Upload .sol file atau paste Solidity code
3. Select language & chain
4. Click "Start Analysis"
5. View results: vulnerability matrix + exploit PoCs

## Token Consumption

- Simple ERC-20 (60 LOC): ~150K tokens
- ERC-721 + marketplace (500 LOC): ~1.2M tokens
- DeFi protocol (2500 LOC): ~6M tokens

## Architecture

12 Security Agents (parallel):
1. Reentrancy Detector
2. Access Control Analyzer
3. Integer Safety Analyzer
4. Front-running Scanner (TODO)
5. Timestamp Dependency Checker (TODO)
6. Delegatecall Risk Analyzer (TODO)
7. Gas Griefing Detector (TODO)
8. Logic Bugs Hunter (TODO)
9. Oracle Manipulation Detector (TODO)
10. Upgrade Safety Analyzer (TODO)
11. MEV Extractor (TODO)
12. Formal Verification Agent (TODO)

Plus: Red Team Exploit Generator

## Current Status

✅ Backend API framework
✅ 3 security agents implemented (Reentrancy, Access Control, Integer Safety)
✅ Red Team exploit generator
✅ Frontend UI (React + Tailwind)
✅ Docker setup
⏳ 9 agents remaining (placeholders)
⏳ Database persistence (PostgreSQL)
⏳ PDF report generation
⏳ Celery async queue

## Next Steps

1. Implement remaining 9 security agents
2. Add database models & migrations (Alembic)
3. PDF report generator (ReportLab)
4. Celery worker for async processing
5. Redis job queue
6. GitHub integration
7. Continuous monitoring mode

## API Endpoints

- `GET /api/health` - System status
- `GET /api/agents` - List all agents
- `POST /api/analyze` - Start analysis
- `GET /api/analyze/{job_id}` - Get result
- `GET /api/stats` - Token usage stats

## Support

Built for Xiaomi MiMo 100T Token Plan
Target: 50-100M tokens/day for continuous security monitoring
