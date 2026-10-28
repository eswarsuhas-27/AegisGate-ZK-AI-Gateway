# 🏆 AegisGate: Official Hackathon Deliverables

**Hackathon**: Mathematics for Systems Security (Devpost)  
**Track**: AI Pipeline Secret Sharing Track  
**Project Name**: AegisGate — Zero-Knowledge Verifiable Secret-Sharing Blind AI Pipeline Gateway  
**Workspace**: `C:\UAI\Hackathon\Mathematics\`

---

## 🎬 Demonstration Video

> **File**: [`demo_video.mp4`](./demo_video.mp4)  
> **Duration**: ~2 minutes  
> **Contents**: Full walkthrough of all features — confidential AI pipeline execution, polynomial share visualizer, wiretap matrix, cryptoanalysis battery, adversarial attack sandbox, and formal proofs.

To regenerate the video at any time:
```bash
python generate_demo_video.py
```

**Video covers the required hackathon demo elements:**
- ✅ Agent fed **encrypted inputs** (cipher handles & blinded tokens)
- ✅ Input **remains encrypted** throughout the host pipeline (wiretap inspection proof)
- ✅ Master key **stays unknown to the agent and host provider** at all times
- ✅ Live adversarial injection attempt failing to exfiltrate secrets

---

## 📦 Deliverables Checklist

### 1. ✅ Source Code (Core Cryptographic Engine)

| File | Description |
| :--- | :--- |
| [`core/crypto_engine.py`](./core/crypto_engine.py) | Shamir's Secret Sharing over 255-bit GF(q) Safe Prime Schnorr Group, Feldman VSS commitments, AES-256-GCM sharding, and Affine Homomorphic Blinder |
| [`core/blind_pipeline.py`](./core/blind_pipeline.py) | Zero-Knowledge entity extractor, blind prompt formulation, and client-side Lagrange polynomial reconstruction orchestrator |
| [`core/cryptoanalysis.py`](./core/cryptoanalysis.py) | 5-point formal cryptoanalysis test battery: Shannon secrecy, Feldman VSS soundness, Lagrange invariance, entropy analysis, IND-CCA2 integrity |
| [`core/attack_simulator.py`](./core/attack_simulator.py) | Adversarial attack simulators: Prompt Injection & key exfiltration, Cloud Host Breach snooping, Byzantine Rogue Share Tampering |
| [`core/llm_gateway.py`](./core/llm_gateway.py) | Multi-provider LLM dispatcher (Google Gemini, OpenAI) with Autonomous Zero-Knowledge Mock Engine fallback |
| [`core/__init__.py`](./core/__init__.py) | Package init |

---

### 2. ✅ Loopback Web Application (Visual Aesthetic)

> Hosted on: **http://localhost:8000** (start with `python run.py`)

| File | Description |
| :--- | :--- |
| [`server.py`](./server.py) | FastAPI REST API server with endpoints: `/api/query`, `/api/cryptoanalysis`, `/api/simulate-attack`, `/api/set-keys` |
| [`static/index.html`](./static/index.html) | Dark-mode glassmorphic single-page web dashboard with 5-tab navigation |
| [`static/style.css`](./static/style.css) | Complete design system: neon cyan/violet glows, glassmorphism cards, responsive grid, micro-animations |
| [`static/app.js`](./static/app.js) | Interactive HTML5 Canvas polynomial curve visualizer, live typewriter wiretap streams, API hooks |

**Visual Features:**
- ✅ **Polynomial Curve Canvas**: Real-time Cartesian plot of $f(x)$ and $(x_i, y_i)$ shares
- ✅ **Side-by-Side Wiretap Matrix**: Red "Cloud Wiretap" vs Green "Local Client Reconstructed" comparison
- ✅ **Live Telemetry Bar**: Crypto shielding time, Lagrange reconstruction time, 0-byte host leakage counter
- ✅ **One-Click Cryptoanalysis Battery**: Interactive test runner with live results
- ✅ **Attack Sandbox**: 3 live adversarial simulations with defense reports

---

### 3. ✅ Terminal User Interface (TUI)

> Start with: `python run.py --tui`

| File | Description |
| :--- | :--- |
| [`aegis_tui.py`](./aegis_tui.py) | Rich interactive CLI featuring colored banners, pipeline execution, cryptoanalysis panel, and attack simulation menu |

---

### 4. ✅ Master Runner

| File | Description |
| :--- | :--- |
| [`run.py`](./run.py) | Unified entry point with `--tui` (Terminal UI), `--test` (automated verification), and default (web app) modes |

---

### 5. ✅ Demo Video Generator

| File | Description |
| :--- | :--- |
| [`generate_demo_video.py`](./generate_demo_video.py) | Selenium Edge + OpenCV script that automates full UI walkthrough and renders MP4 with title cards and overlay labels |
| [`demo_video.mp4`](./demo_video.mp4) | Generated demonstration video (2 min, 1280×800 MP4) |

---

### 6. ✅ Mathematical Proof Documentation

| File | Description |
| :--- | :--- |
| [`cryptoanalysis_report.md`](./cryptoanalysis_report.md) | Formal mathematical proof paper: Shannon Perfect Secrecy theorem (Vandermonde proof), Feldman VSS DLP soundness, Lagrange invariance, IND-CCA2 integrity, and vulnerability matrix |
| [`README.md`](./README.md) | Complete architecture documentation, prize alignment matrix, Mermaid pipeline diagram, quickstart guide, and video demo script |

---

### 7. ✅ Automated Test Suite (100% Pass Rate)

Run with: `python run.py --test`

| Test | Result |
| :--- | :--- |
| Shannon Perfect Secrecy ($H(S\|S_{<k}) = H(S)$, 0.0 bits mutual information) | ✅ PASSED |
| Feldman VSS Soundness (100.0% tamper detection rate, forgery prob < $2^{-255}$) | ✅ PASSED |
| Combinatorial Lagrange Invariance (All $C(5, 3) = 10$ subsets congruent) | ✅ PASSED |
| Share Entropy & Uniformity (7.99+ bits/byte) | ✅ PASSED |
| IND-CCA2 Authenticated Encryption Integrity (100% tamper rejection) | ✅ PASSED |
| Prompt Injection Attack Mitigation (0 bytes leaked) | ✅ MITIGATED |
| Cloud Host Breach Simulation ($H(S\|Logs) = 255$ bits) | ✅ MITIGATED |
| Byzantine Share Tampering (Feldman VSS detected & recovered) | ✅ MITIGATED |

---

## 🎯 Prize Alignment Summary

| Prize | Status |
| :--- | :--- |
| ⭐ **Best AI Pipelines Project** | Complete end-to-end zero-knowledge LLM pipeline with Gemini/OpenAI integration |
| ⭐ **Certified Cryptographer** | 5-point formal cryptoanalysis passing 100% with mathematical proofs in `cryptoanalysis_report.md` |
| ⭐ **Certified Cybersecurity Mitigator** | Live adversarial sandbox defeating 3 enterprise threat vectors |
| ⭐ **Best Cryptographic Algorithm** | Safe Prime Schnorr Group SSS + Feldman VSS over 255-bit GF(q) |
| ⭐ **Best Overall Project** | All criteria: math rigor + premium web UI + TUI + formal proofs + video demo |

---

## 🚀 How to Run

```bash
# Start the Web Dashboard
python run.py
# → Open http://localhost:8000

# Launch Terminal UI
python run.py --tui

# Run Automated Math & Security Verification
python run.py --test

# Regenerate Demo Video
python generate_demo_video.py
```

---

## 🔑 Optional: Connect Real LLM APIs

Set environment variables before running, or configure via the web UI (Settings tab):

```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "AIzaSy..."
$env:OPENAI_API_KEY = "sk-proj-..."
python run.py
```

The autonomous mock engine runs immediately without any API keys — **fully functional for judging without credentials**.
