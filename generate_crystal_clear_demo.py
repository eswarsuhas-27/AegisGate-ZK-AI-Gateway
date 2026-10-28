"""
AegisGate Ultra-Clear 1080p Studio Demo Generator
=================================================
Produces a crystal-clear, Full HD 1080p (1920x1080) walkthrough:
- ZERO artificial overlays, bars, or badges blocking the UI
- Pixel-perfect CDP (Chrome DevTools Protocol) 1920x1080 viewport
- High-clarity synchronized voice narration (Windows SAPI SpVoice)
- High-performance keyframe capture + FFmpeg H.264 CRF 18
- Complete interactive walkthrough of all 5 tabs and features
"""

import os
import sys
import time
import wave
import subprocess
import shutil
import cv2
import numpy as np
import win32com.client
from selenium import webdriver
from selenium.webdriver.edge.options import Options

WORKSPACE = r"c:\UAI\Hackathon\Mathematics"
OUTPUT_VIDEO = os.path.join(WORKSPACE, "demo_video.mp4")
TEMP_DIR = os.path.join(WORKSPACE, "temp_studio_build")
FPS = 15
WIDTH = 1920
HEIGHT = 1080

SCENES = [
    {
        "id": "scene_01_intro",
        "tab": "gateway",
        "narration": (
            "Welcome to AegisGate, a Zero-Knowledge Verifiable Secret-Sharing AI Pipeline Gateway "
            "engineered for the Mathematics for Systems Security Hackathon. "
            "In modern enterprise workflows, sending prompts to cloud providers like OpenAI, Gemini, or AWS Bedrock "
            "exposes sensitive cleartext data in transit and on host servers. "
            "AegisGate eliminates this vulnerability entirely. By blinding inputs with Shamir's Secret Sharing over a 255-bit Galois Field, "
            "the host model never sees the cleartext, and the master decryption key never leaves client memory."
        ),
        "steps": [
            {"action": "init", "hold_ratio": 1.0}
        ]
    },
    {
        "id": "scene_02_pipeline",
        "tab": "gateway",
        "narration": (
            "Let's execute a live confidential query. We click the Financial M and A preset to load a sensitive acquisition prompt. "
            "When we dispatch the query, AegisGate's cryptographic engine shards the ephemeral AES-256-GCM master key into verifiable shares. "
            "Look at the side-by-side comparison matrix. On the left, the cloud host wiretap shows exactly what the provider receives: "
            "only blinded cipher handles. Zero bytes of sensitive plaintext are leaked. "
            "On the right, the client locally reconstructs the full synthesis in under ten milliseconds using Lagrange polynomial interpolation."
        ),
        "steps": [
            {"action": "click_preset", "script": "loadPreset('financial');", "hold_ratio": 0.20},
            {"action": "submit_query", "script": "document.getElementById('btnSubmitQuery').click();", "wait": 0.8, "hold_ratio": 0.35},
            {"action": "scroll_wiretap", "script": "window.scrollTo(0, 320);", "hold_ratio": 0.45}
        ]
    },
    {
        "id": "scene_03_visualizer",
        "tab": "gateway",
        "narration": (
            "Here in the interactive visualizer, we observe the finite field arithmetic in real time. "
            "The red point at f of zero represents the secret, stored exclusively in client memory. "
            "The cyan markers are the evaluated polynomial shares distributed across nodes. "
            "Notice Feldman's Verifiable Secret Sharing badge: discrete logarithm commitments in a safe prime group "
            "ensure that any malicious or corrupted share is mathematically rejected before reconstruction."
        ),
        "steps": [
            {"action": "scroll_top", "script": "window.scrollTo(0, 0);", "hold_ratio": 0.30},
            {"action": "slider_4", "script": "document.getElementById('sliderK').value = 4; updateSliders();", "hold_ratio": 0.35},
            {"action": "slider_3", "script": "document.getElementById('sliderK').value = 3; updateSliders();", "hold_ratio": 0.35}
        ]
    },
    {
        "id": "scene_04_cryptoanalysis",
        "tab": "cryptoanalysis",
        "narration": (
            "Next, we navigate to the Certified Cryptographer Audit Suite and run the comprehensive mathematical battery. "
            "AegisGate validates Shannon perfect secrecy, confirming zero mutual information for any coalition with fewer than k shares. "
            "It verifies Feldman discrete logarithm commitments, combinatorial Lagrange invariance across all subsets, "
            "and maximum statistical share entropy. Every test passes with one hundred percent mathematical exactness."
        ),
        "steps": [
            {"action": "init", "script": "window.scrollTo(0, 0);", "hold_ratio": 0.18},
            {"action": "run_battery", "script": "runCryptoanalysisBattery();", "wait": 0.7, "hold_ratio": 0.42},
            {"action": "scroll_down", "script": "window.scrollTo(0, 260);", "hold_ratio": 0.40}
        ]
    },
    {
        "id": "scene_05_attacks",
        "tab": "mitigator",
        "narration": (
            "In the Adversarial Attack Sandbox, we test our gateway against top enterprise threat vectors. "
            "First, prompt injection jailbreaks attempt to force key dumps: AegisGate blocks the exploit, revealing zero keys. "
            "Second, when simulating a complete cloud host server breach, the adversary finds only blind cipher handles. "
            "Third, when an active Byzantine actor injects a corrupted share, Feldman VSS instantly catches the invalid evaluation. "
            "All threats are mitigated in real time."
        ),
        "steps": [
            {"action": "init", "script": "window.scrollTo(0, 0);", "hold_ratio": 0.15},
            {"action": "attack_injection", "script": "launchAttackSimulation('prompt_injection');", "wait": 0.4, "hold_ratio": 0.28},
            {"action": "attack_breach", "script": "launchAttackSimulation('host_breach');", "wait": 0.4, "hold_ratio": 0.28},
            {"action": "attack_tampering", "script": "launchAttackSimulation('share_tampering');", "wait": 0.4, "hold_ratio": 0.29}
        ]
    },
    {
        "id": "scene_06_proofs",
        "tab": "proofs",
        "narration": (
            "Finally, the Mathematical Proofs tab details our rigorous cryptographic foundations: "
            "Shamir's threshold scheme over Galois Field GF of q, Feldman's safe prime discrete logarithm commitments, "
            "and Shannon's proof of zero mutual information leakage. "
            "AegisGate unites mathematical provability, cryptographic integrity, and enterprise zero-trust security. "
            "Thank you for reviewing our hackathon submission."
        ),
        "steps": [
            {"action": "init", "script": "window.scrollTo(0, 0);", "hold_ratio": 0.30},
            {"action": "scroll_mid", "script": "window.scrollTo(0, 300);", "hold_ratio": 0.35},
            {"action": "scroll_bot", "script": "window.scrollTo(0, 600);", "hold_ratio": 0.35}
        ]
    }
]


def generate_audio_file(text: str, wav_path: str) -> float:
    """Synthesizes speech to WAV using Windows SAPI SpVoice and returns exact duration."""
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    
    voices = speaker.GetVoices()
    for i in range(voices.Count):
        v = voices.Item(i)
        if "David" in v.GetDescription():
            speaker.Voice = v
            break

    speaker.Rate = 0
    stream.Open(wav_path, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()

    with wave.open(wav_path, "rb") as w:
        duration = w.getnframes() / float(w.getframerate())
    return duration


def capture_clean_frame(driver) -> np.ndarray:
    """Captures uncompressed, razor-sharp 1080p frame directly from browser."""
    png_data = driver.get_screenshot_as_png()
    img_arr = np.frombuffer(png_data, dtype=np.uint8)
    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    if frame.shape[0] != HEIGHT or frame.shape[1] != WIDTH:
        frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_LANCZOS4)
    return frame


def record_choreographed_scene(driver, scene: dict, duration: float, out_video_path: str):
    """Executes scene steps, takes clean 1080p screenshots, and duplicates frames to match duration."""
    total_frames = max(15, int(duration * FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_video_path, fourcc, FPS, (WIDTH, HEIGHT))

    print(f"  Recording {scene['id']}: {duration:.2f}s ({total_frames} frames @ {FPS} FPS)...")

    # Navigate to target tab
    driver.execute_script(f"switchTab('{scene['tab']}');")
    time.sleep(0.4)

    steps = scene["steps"]
    written_frames = 0

    for step_idx, step in enumerate(steps):
        # Calculate frame allocation for this step
        if step_idx == len(steps) - 1:
            step_frames = total_frames - written_frames
        else:
            step_frames = int(total_frames * step["hold_ratio"])

        # Execute step action if present
        script = step.get("script")
        if script:
            driver.execute_script(script)
            wait_time = step.get("wait", 0.15)
            time.sleep(wait_time)

        # Take ONE pristine 1080p screenshot of this state
        frame = capture_clean_frame(driver)

        # Write frame repeatedly to maintain smooth FPS without lag
        for _ in range(step_frames):
            writer.write(frame)
            written_frames += 1

    writer.release()
    print(f"  [OK] Completed {scene['id']} ({written_frames} frames)")


def main():
    print("=" * 70)
    print("AegisGate: Building Ultra-Clear 1080p Studio Demo Video")
    print("=" * 70)

    if os.path.exists(OUTPUT_VIDEO):
        os.remove(OUTPUT_VIDEO)

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

    # 1. Setup Headless Edge with exact 1080p CDP override
    print("\n[1/4] Launching Edge with 1920x1080 Full HD viewport...")
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--hide-scrollbars")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(options=opts)
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": WIDTH,
        "height": HEIGHT,
        "deviceScaleFactor": 1,
        "mobile": False
    })
    driver.get("http://127.0.0.1:8000")
    time.sleep(1.5)
    print("[OK] Connected to http://127.0.0.1:8000 in crisp 1080p")

    synced_scene_files = []

    # 2. Record scenes
    print("\n[2/4] Generating studio audio narration & recording crisp 1080p scenes...")
    for idx, scene in enumerate(SCENES, 1):
        scene_id = scene["id"]
        wav_path = os.path.join(TEMP_DIR, f"{scene_id}.wav")
        raw_video_path = os.path.join(TEMP_DIR, f"{scene_id}_raw.mp4")
        synced_path = os.path.join(TEMP_DIR, f"{scene_id}_synced.mp4")

        # Synthesize audio
        dur = generate_audio_file(scene["narration"], wav_path)
        dur += 0.4  # Clean spacing
        print(f"\n({idx}/{len(SCENES)}) Scene {idx}: {dur:.2f}s audio generated")

        # Record choreographed clean 1080p video
        record_choreographed_scene(driver, scene, dur, raw_video_path)

        # Merge Audio & Video with FFmpeg (CRF 18 = crisp, broadcast quality, fast encode)
        print(f"  Encoding {scene_id} with H.264 CRF 18...")
        merge_cmd = [
            "ffmpeg", "-y",
            "-i", raw_video_path,
            "-i", wav_path,
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
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
    print("\n[OK] All 6 scenes recorded and encoded with high fidelity!")

    # 3. Concatenate all scenes into final master video
    print("\n[3/4] Assembling final master demo_video.mp4...")
    concat_list_path = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in synced_scene_files:
            clean_p = p.replace("\\", "/")
            f.write(f"file '{clean_p}'\n")

    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_path,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        OUTPUT_VIDEO
    ]
    res_concat = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res_concat.returncode != 0:
        print("Concat FFmpeg error:", res_concat.stderr)
        raise RuntimeError("Final concatenation failed")

    # Clean up temp files
    try:
        shutil.rmtree(TEMP_DIR)
    except Exception:
        pass

    # 4. Verification
    print("\n[4/4] Verifying master video...")
    if os.path.exists(OUTPUT_VIDEO):
        size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        cap = cv2.VideoCapture(OUTPUT_VIDEO)
        final_fps = cap.get(cv2.CAP_PROP_FPS)
        final_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        final_dur = final_frames / final_fps if final_fps > 0 else 0
        final_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        final_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        print("=" * 70)
        print("STUDIO 1080P DEMO VIDEO CREATED SUCCESSFULLY!")
        print(f"File:       {OUTPUT_VIDEO}")
        print(f"Size:       {size_mb:.2f} MB")
        print(f"Resolution: {final_w}x{final_h} Full HD 1080p")
        print(f"Duration:   {final_dur:.1f} seconds ({final_frames} frames @ {final_fps:.1f} FPS)")
        print(f"Overlays:   ZERO (Pure website UI, uncluttered)")
        print(f"Audio:      Synchronized Studio Voice-Over (AAC 192k)")
        print("=" * 70)
    else:
        print("Error: OUTPUT_VIDEO not found!")

if __name__ == "__main__":
    main()
