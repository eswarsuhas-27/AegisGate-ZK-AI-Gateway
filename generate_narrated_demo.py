"""
AegisGate Narrated Video Demo Generator
=======================================
Generates a complete, professional, narrated demonstration video of AegisGate:
- High-fidelity voice-over using Windows SAPI TTS
- Automated Selenium Edge headless interaction across all features:
  1. Overview & Problem Statement
  2. Live Confidential AI Pipeline (Financial M&A Preset)
  3. Real-Time GF(q) Polynomial & SSS Visualizer
  4. Certified Cryptographer Audit Suite (100% Pass)
  5. Adversarial Cybersecurity Mitigation Sandbox
  6. Mathematical Proofs & Zero-Knowledge Architecture
- Clean subtitle / chapter title card overlays
- Full audio-video synchronization merged with FFmpeg
"""

import os
import sys
import time
import wave
import subprocess
import cv2
import numpy as np
import win32com.client
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

WORKSPACE = r"c:\UAI\Hackathon\Mathematics"
OUTPUT_VIDEO = os.path.join(WORKSPACE, "demo_video.mp4")
TEMP_DIR = os.path.join(WORKSPACE, "temp_demo_build")
FPS = 10
WIDTH = 1280
HEIGHT = 720

SCENES = [
    {
        "id": "scene_01_intro",
        "title": "AegisGate: Zero-Knowledge AI Pipeline Gateway",
        "tab": "gateway",
        "narration": (
            "Welcome to AegisGate, a zero-knowledge verifiable secret-sharing AI pipeline gateway. "
            "In modern enterprise workflows, sending prompts to cloud providers like OpenAI, Gemini, or AWS Bedrock "
            "leaks cleartext data and sensitive intellectual property. "
            "AegisGate completely solves this by blinding inputs with Shamir's Secret Sharing over a 255-bit Galois Field, "
            "keeping the master decryption key exclusively in local client memory."
        ),
        "subtitle": "AegisGate: Zero-Knowledge Verifiable Secret-Sharing Blind AI Pipeline Gateway",
        "action": "intro"
    },
    {
        "id": "scene_02_pipeline",
        "title": "Live Execution: Confidential Financial M&A Pipeline",
        "tab": "gateway",
        "narration": (
            "Let's execute a live confidential query. We select a sensitive financial merger and acquisition prompt. "
            "When we dispatch the query, AegisGate encrypts the payload with AES-256-GCM and splits the ephemeral key "
            "into verifiable shares. Look at the real-time cloud wiretap: host models only observe blinded cipher handles. "
            "Exactly zero bytes of cleartext leak to the cloud, and client reconstruction succeeds seamlessly via Lagrange interpolation."
        ),
        "subtitle": "Client-Side Confidential Query Dispatch & Zero-Leakage Cloud Wiretap",
        "action": "execute_pipeline"
    },
    {
        "id": "scene_03_visualizer",
        "title": "Mathematical Visualizer: GF(q) Polynomial Curves",
        "tab": "gateway",
        "narration": (
            "On the right, our live visualizer illustrates the underlying Galois Field arithmetic. "
            "The red intercept represents the secret at f of zero, held only on the client. "
            "The cyan points represent evaluated shares distributed across participating nodes. "
            "Feldman's Verifiable Secret Sharing is active, publishing discrete log commitments in a safe prime group "
            "to guarantee that any corrupted share is mathematically rejected."
        ),
        "subtitle": "Interactive Shamir Polynomial Curve & Feldman VSS Discrete Log Commitments",
        "action": "visualizer"
    },
    {
        "id": "scene_04_cryptoanalysis",
        "title": "Certified Cryptographer Audit Suite",
        "tab": "cryptoanalysis",
        "narration": (
            "Now let's switch to the Rigorous Cryptoanalysis Suite and launch the full mathematical test battery. "
            "AegisGate verifies Shannon perfect secrecy, confirming zero mutual information for any subset below the threshold k. "
            "It validates Feldman discrete log commitments, combinatorial Lagrange invariance across all combinations, "
            "and maximum Shannon entropy. Every single test passes with flying colors."
        ),
        "subtitle": "Audited Cryptographic Battery: Shannon Secrecy, Feldman VSS, and Invariance",
        "action": "run_cryptoanalysis"
    },
    {
        "id": "scene_05_attacks",
        "title": "Adversarial Cybersecurity Mitigation Sandbox",
        "tab": "mitigator",
        "narration": (
            "Next is our Adversarial Attack Sandbox, proving active defense against top enterprise threat vectors. "
            "We simulate prompt injection jailbreaks, cloud host memory dumps, and Byzantine share tampering. "
            "In every scenario, AegisGate successfully neutralizes the threat, shielding master keys and "
            "instantly detecting malicious payload mutations."
        ),
        "subtitle": "Adversarial Defense Sandbox: Prompt Injections, Host Breaches & Byzantine Attacks",
        "action": "run_attacks"
    },
    {
        "id": "scene_06_proofs",
        "title": "Formal Mathematical Proofs & Conclusion",
        "tab": "proofs",
        "narration": (
            "Finally, the Mathematical Proofs tab documents our formal proofs for Shamir's threshold scheme over GF(q), "
            "Feldman's homomorphic verifiability, and Shannon's information-theoretic zero leakage. "
            "AegisGate delivers verified, mathematically sound privacy for the future of enterprise AI systems. "
            "Thank you for reviewing our hackathon submission."
        ),
        "subtitle": "Formal Mathematical Foundations: Finite Fields, Discrete Logarithms & Shannon Proof",
        "action": "view_proofs"
    }
]


def generate_audio_file(text: str, wav_path: str) -> float:
    """Synthesizes speech to WAV using Windows SAPI SpVoice and returns exact duration."""
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    
    # Try selecting Microsoft David for clear narration
    voices = speaker.GetVoices()
    for i in range(voices.Count):
        v = voices.Item(i)
        if "David" in v.GetDescription():
            speaker.Voice = v
            break

    speaker.Rate = 0  # Natural cadence
    stream.Open(wav_path, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()

    with wave.open(wav_path, "rb") as w:
        duration = w.getnframes() / float(w.getframerate())
    return duration


def draw_overlay(frame, title: str, subtitle: str, progress: float):
    """Draws a premium dark glassmorphism subtitle banner on the frame."""
    h, w = frame.shape[:2]
    
    # Top banner bar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (15, 10, 8), -1)
    cv2.line(overlay, (0, 55), (w, 55), (200, 150, 0), 2)
    
    # Bottom caption bar
    cv2.rectangle(overlay, (0, h - 80), (w, h), (15, 10, 8), -1)
    cv2.line(overlay, (0, h - 80), (w, h - 80), (100, 50, 200), 2)
    
    # Blend overlay with 88% opacity
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)

    # Top title text
    cv2.putText(frame, "AEGISGATE | ZERO-KNOWLEDGE AI PIPELINE GATEWAY", (20, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 220, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, title.upper(), (20, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 1, cv2.LINE_AA)

    # Audio Voice-Over badge (Top Right)
    cv2.rectangle(frame, (w - 240, 15), (w - 20, 45), (40, 25, 20), -1)
    cv2.rectangle(frame, (w - 240, 15), (w - 20, 45), (0, 255, 150), 1)
    cv2.putText(frame, "VOICE-OVER ACTIVE", (w - 215, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 150), 1, cv2.LINE_AA)
    # Pulsing red recording dot
    cv2.circle(frame, (w - 228, 30), 5, (0, 0, 255), -1)

    # Bottom subtitle text
    cv2.putText(frame, subtitle, (30, h - 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Track: AI Pipeline Secret Sharing | Finite Field GF(q) | Feldman VSS", (30, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 220, 255), 1, cv2.LINE_AA)

    # Progress bar at very bottom
    prog_w = int(w * min(1.0, max(0.0, progress)))
    cv2.line(frame, (0, h - 3), (prog_w, h - 3), (0, 220, 255), 4)

    return frame


def record_scene(driver, scene: dict, duration: float, out_video_path: str):
    """Executes scene actions in browser and captures video frames matching duration."""
    total_frames = max(15, int(duration * FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_video_path, fourcc, FPS, (WIDTH, HEIGHT))

    print(f"  Recording {scene['id']}: {duration:.2f}s ({total_frames} frames)...")

    # Navigate to correct tab
    driver.execute_script(f"switchTab('{scene['tab']}');")
    time.sleep(0.5)

    action = scene.get("action", "")

    # Pre-action logic
    if action == "execute_pipeline":
        driver.execute_script("loadPreset('financial');")
        time.sleep(0.3)
        # Execute query at frame 15
    elif action == "run_cryptoanalysis":
        driver.execute_script("runCryptoanalysisBattery();")
        time.sleep(0.3)
    elif action == "run_attacks":
        driver.execute_script("launchAttackSimulation('prompt_injection');")
        time.sleep(0.3)

    for i in range(total_frames):
        # Trigger dynamic mid-scene events
        if action == "execute_pipeline" and i == int(total_frames * 0.25):
            driver.execute_script("document.getElementById('btnSubmitQuery').click();")
        elif action == "visualizer":
            # Animate sliders
            val = 3 if (i % 20 < 10) else 4
            driver.execute_script(f"""
                document.getElementById('sliderK').value = {val};
                updateSliders();
            """)
        elif action == "run_attacks":
            if i == int(total_frames * 0.35):
                driver.execute_script("launchAttackSimulation('host_breach');")
            elif i == int(total_frames * 0.70):
                driver.execute_script("launchAttackSimulation('share_tampering');")
        elif action == "view_proofs":
            # Smooth scrolling through proofs
            scroll_y = int((i / total_frames) * 600)
            driver.execute_script(f"window.scrollTo(0, {scroll_y});")

        # Capture screenshot
        png_data = driver.get_screenshot_as_png()
        img_arr = np.frombuffer(png_data, dtype=np.uint8)
        frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        # Resize to standard 1280x720
        if frame.shape[0] != HEIGHT or frame.shape[1] != WIDTH:
            frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)

        # Apply HUD overlay
        progress = (i + 1) / total_frames
        frame = draw_overlay(frame, scene["title"], scene["subtitle"], progress)

        writer.write(frame)
        time.sleep(1.0 / (FPS * 1.5))  # Smooth throttle

    writer.release()
    print("  [OK] Finished recording " + scene['id'])


def main():
    print("=" * 70)
    print("AegisGate: Building Full Narrated Walkthrough Video Demo")
    print("=" * 70)

    os.makedirs(TEMP_DIR, exist_ok=True)

    # 1. Setup Headless Edge WebDriver
    print("\n[1/4] Launching headless browser...")
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={WIDTH},{HEIGHT}")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--hide-scrollbars")

    driver = webdriver.Edge(options=opts)
    driver.set_window_size(WIDTH, HEIGHT)
    driver.get("http://127.0.0.1:8000")
    time.sleep(1.5)
    print("[OK] Browser connected to http://127.0.0.1:8000")

    synced_scene_files = []

    # 2. Process each scene: Audio -> Video -> Synced Clip
    print("\n[2/4] Generating voice narration and recording interactive scenes...")
    for idx, scene in enumerate(SCENES, 1):
        scene_id = scene["id"]
        wav_path = os.path.join(TEMP_DIR, f"{scene_id}.wav")
        raw_video_path = os.path.join(TEMP_DIR, f"{scene_id}_raw.mp4")
        synced_path = os.path.join(TEMP_DIR, f"{scene_id}_synced.mp4")

        # Generate voice audio
        print(f"\n({idx}/{len(SCENES)}) Voice Synthesis: {scene['title']}")
        dur = generate_audio_file(scene["narration"], wav_path)
        # Pad 0.5s breathing room
        dur += 0.5
        print(f"  Audio duration: {dur:.2f} seconds")

        # Record visual scene
        record_scene(driver, scene, dur, raw_video_path)

        # Merge Audio & Video using FFmpeg
        print(f"  Merging voice-over with FFmpeg into {scene_id}_synced.mp4...")
        merge_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", wav_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            synced_path
        ]
        res = subprocess.run(merge_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr)
            raise RuntimeError(f"FFmpeg failed on {scene_id}")

        synced_scene_files.append(synced_path)

    driver.quit()
    print("\n[OK] All 6 narrated scenes successfully recorded and synced!")

    # 3. Concatenate all scenes into final demo_video.mp4
    print("\n[3/4] Concatenating scenes into final master video...")
    concat_list_path = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in synced_scene_files:
            # Escape backslashes for ffmpeg concat demuxer
            clean_p = p.replace("\\", "/")
            f.write(f"file '{clean_p}'\n")

    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        OUTPUT_VIDEO
    ]
    res_concat = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res_concat.returncode != 0:
        print("Concat FFmpeg error:", res_concat.stderr)
        raise RuntimeError("Final concatenation failed")

    # 4. Verification
    print("\n[4/4] Verifying final master video...")
    if os.path.exists(OUTPUT_VIDEO):
        size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        cap = cv2.VideoCapture(OUTPUT_VIDEO)
        final_fps = cap.get(cv2.CAP_PROP_FPS)
        final_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        final_dur = final_frames / final_fps if final_fps > 0 else 0
        cap.release()

        print("=" * 70)
        print("MASTER NARRATED DEMO VIDEO CREATED SUCCESSFULLY!")
        print(f"File:     {OUTPUT_VIDEO}")
        print(f"Size:     {size_mb:.2f} MB")
        print(f"Duration: {final_dur:.1f} seconds ({final_frames} frames @ {final_fps:.1f} FPS)")
        print(f"Audio:    Synchronized SAPI Voice-Over (AAC 192k)")
        print(f"Video:    1280x720 HD H.264 MP4 with dynamic subtitles & HUD")
        print("=" * 70)
    else:
        print("Error: OUTPUT_VIDEO not found!")

if __name__ == "__main__":
    main()
