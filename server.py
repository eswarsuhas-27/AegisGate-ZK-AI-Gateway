"""
AegisGate Web Application Server
================================
FastAPI server hosted on the loopback machine (http://localhost:8000).
Serves the cryptographic dashboard and REST endpoints.
"""

import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from core.blind_pipeline import BlindPipelineOrchestrator
from core.cryptoanalysis import CryptoanalysisSuite
from core.attack_simulator import AdversarialAttackSimulator
from core.llm_gateway import LLMGateway

app = FastAPI(
    title="AegisGate Cryptographic AI Pipeline",
    description="Zero-Knowledge Secret-Sharing & Verifiable AI Pipeline Gateway",
    version="1.0.0"
)

# Core Instances
orchestrator = BlindPipelineOrchestrator()
cryptoanalysis_suite = CryptoanalysisSuite()
attack_simulator = AdversarialAttackSimulator()

# Request Models
class QueryRequest(BaseModel):
    prompt: str
    threshold_k: int = 3
    total_shares_n: int = 5
    is_adversarial: bool = False

class ApiKeyRequest(BaseModel):
    gemini_key: Optional[str] = None
    openai_key: Optional[str] = None

class AttackRequest(BaseModel):
    attack_type: str  # prompt_injection, host_breach, share_tampering

# API Endpoints
@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "field": "GF(q) Safe Prime Group (255-bit)",
        "generator": 4,
        "llm_gateway": orchestrator.llm.get_status()
    }

@app.post("/api/set-keys")
async def set_keys(req: ApiKeyRequest):
    orchestrator.llm.set_keys(req.gemini_key, req.openai_key)
    return {"status": "updated", "config": orchestrator.llm.get_status()}

@app.post("/api/query")
async def process_query(req: QueryRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        result = orchestrator.process_secure_query(
            user_prompt=req.prompt,
            threshold_k=req.threshold_k,
            total_shares_n=req.total_shares_n,
            is_adversarial=req.is_adversarial
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cryptoanalysis")
async def run_cryptoanalysis():
    try:
        # Run with 25 samples for fast web response
        results = cryptoanalysis_suite.run_full_cryptoanalysis(num_samples=25)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/simulate-attack")
async def simulate_attack(req: AttackRequest):
    if req.attack_type == "prompt_injection":
        return attack_simulator.run_prompt_injection_attack()
    elif req.attack_type == "host_breach":
        return attack_simulator.run_host_breach_simulation()
    elif req.attack_type == "share_tampering":
        return attack_simulator.run_rogue_share_tampering_attack()
    else:
        raise HTTPException(status_code=400, detail="Unknown attack type.")

# Serve Static UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🛡️  AegisGate Zero-Knowledge AI Pipeline Gateway")
    print("🌐  Loopback Web Dashboard: http://localhost:8000")
    print("="*60 + "\n")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
