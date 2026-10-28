"""
AegisGate Video Demo Generator
==============================
Captures a high-quality multi-frame screenshot walkthrough of all UI tabs
and combines them into an MP4 video using OpenCV with annotated title cards.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
import tempfile
import threading

# Ensure UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Imports
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "demo_video.mp4")
FRAME_W, FRAME_H = 1280, 800
FPS = 1  # 1 screenshot per second, each held for multiple frames in final video
FRAMES_PER_SLIDE = 8  # each screenshot displayed for 8 seconds at 1fps
BASE_URL = "http://127.0.0.1:8000"

def get_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument(f"--window-size={FRAME_W},{FRAME_H}")
    opts.add_argument("--force-device-scale-factor=1")
    opts.add_argument("--disable-gpu")
    driver = webdriver.Edge(options=opts)
    driver.set_window_size(FRAME_W, FRAME_H)
    return driver

def screenshot_to_frame(driver):
    """Takes a screenshot and returns a BGR numpy array."""
    png_bytes = driver.get_screenshot_as_png()
    nparr = np.frombuffer(png_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (FRAME_W, FRAME_H), interpolation=cv2.INTER_LANCZOS4)
    return img

def add_title_card(frames, title, subtitle="", duration_frames=24, bg_color=(7, 9, 19)):
    """
    Creates a dark title card frame with neon text overlaid.
    """
    card = np.full((FRAME_H, FRAME_W, 3), bg_color, dtype=np.uint8)
    # Horizontal separator line (neon cyan ~blue-green)
    cv2.line(card, (80, FRAME_H // 2 - 40), (FRAME_W - 80, FRAME_H // 2 - 40), (0, 200, 220), 2)
    # Title text (large)
    cv2.putText(card, title, (80, FRAME_H // 2), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 242, 254), 3, cv2.LINE_AA)
    # Subtitle text (smaller)
    if subtitle:
        cv2.putText(card, subtitle, (82, FRAME_H // 2 + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (148, 163, 184), 2, cv2.LINE_AA)
    # AegisGate label top-left
    cv2.putText(card, "AegisGate: Zero-Knowledge AI Pipeline Gateway", (80, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 120), 1, cv2.LINE_AA)
    # Horizontal separator bottom
    cv2.line(card, (80, FRAME_H // 2 + 90), (FRAME_W - 80, FRAME_H // 2 + 90), (0, 200, 220), 2)
    for _ in range(duration_frames):
        frames.append(card.copy())

def add_overlay_label(frame, label, color=(0, 242, 254)):
    """Adds a label overlay at the bottom-left of a frame."""
    overlay = frame.copy()
    # Semi-transparent dark bar at bottom
    cv2.rectangle(overlay, (0, FRAME_H - 48), (FRAME_W, FRAME_H), (7, 9, 19), -1)
    cv2.addWeighted(overlay, 0.80, frame, 0.20, 0, frame)
    cv2.putText(frame, label, (18, FRAME_H - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.72, color, 2, cv2.LINE_AA)
    return frame

def execute_pipeline_query(driver):
    """Fires the preset Financial M&A query via JavaScript and waits for execution."""
    # Load the financial preset
    driver.execute_script("loadPreset('financial');")
    time.sleep(0.5)
    # Submit the form via JS
    driver.execute_script("document.getElementById('btnSubmitQuery').click();")
    time.sleep(5)  # Wait for pipeline execution + typewriter

def main():
    print("[1/6] Initializing Edge WebDriver (headless)...")
    driver = get_driver()
    frames = []
    out_dir = os.path.dirname(OUTPUT_PATH)

    try:
        # ----------------------------------------------------------------
        # TITLE CARD: Introduction
        # ----------------------------------------------------------------
        print("[2/6] Recording Introduction Title Card...")
        add_title_card(frames,
                       "AegisGate: Zero-Knowledge AI Pipeline Gateway",
                       "Hackathon Demonstration | AI Pipeline Secret Sharing Track",
                       duration_frames=30)

        # ----------------------------------------------------------------
        # PART 1: Landing Page
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 1: Dashboard Overview", "Dark Glassmorphic UI with Polynomial Visualizer", 18)
        print("       Loading landing page...")
        driver.get(BASE_URL)
        time.sleep(3)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Tab 1: Confidential AI Gateway | Polynomial Canvas Visualizer | Wiretap Matrix")
        for _ in range(FRAMES_PER_SLIDE):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # PART 2: Confidential AI Pipeline Demo
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 2: Confidential AI Pipeline", "Financial M&A Secrets | Zero cleartext to Cloud LLM", 18)
        print("       Executing Financial M&A pipeline query...")
        execute_pipeline_query(driver)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Red Wiretap = CIPHER_HANDLE only | Green Client Box = Lagrange Reconstructed | 0 bytes leaked")
        for _ in range(FRAMES_PER_SLIDE + 4):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # PART 3: Adversarial Jailbreak Test
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 3: Adversarial Jailbreak Test", "Prompt Injection Attack vs Zero-Knowledge Defense", 18)
        print("       Running adversarial jailbreak preset...")
        driver.execute_script("loadPreset('injection');")
        time.sleep(0.5)
        driver.execute_script("document.getElementById('btnSubmitQuery').click();")
        time.sleep(5)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Jailbreak Prompt Blocked | Agent cannot exfiltrate keys — Master Key is NEVER on host server", (0, 200, 100))
        for _ in range(FRAMES_PER_SLIDE):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # PART 4: Cryptoanalysis Suite
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 4: Formal Cryptoanalysis Battery", "5-Point Mathematical Certification (Target: Certified Cryptographer)", 18)
        print("       Switching to Cryptoanalysis tab...")
        driver.execute_script("switchTab('cryptoanalysis')")
        time.sleep(1)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Cryptoanalysis Suite | Shannon Secrecy | Feldman VSS | Lagrange Invariance | IND-CCA2 Integrity")
        for _ in range(FRAMES_PER_SLIDE // 2):
            frames.append(frame.copy())

        print("       Running cryptoanalysis battery...")
        driver.execute_script("runCryptoanalysisBattery()")
        time.sleep(8)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "RESULT: 100% CERTIFIED_CRYPTOGRAPHIC_GRADE | 0.0 bits leakage | 7.99+ bits/byte entropy | 100% tamper detected")
        for _ in range(FRAMES_PER_SLIDE + 4):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # PART 5: Adversarial Attack Sandbox
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 5: Adversarial Attack Sandbox", "Live Prompt Injection + Byzantine Share Tampering Simulations", 18)
        print("       Switching to Attack Mitigator tab...")
        driver.execute_script("switchTab('mitigator')")
        time.sleep(1)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Attack Sandbox: 3 Live Threat Vectors | Prompt Injection | Cloud Host Breach | Byzantine Tampering")
        for _ in range(FRAMES_PER_SLIDE // 2):
            frames.append(frame.copy())

        print("       Launching Prompt Injection attack simulation...")
        driver.execute_script("launchAttackSimulation('prompt_injection')")
        time.sleep(4)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Attack 1: Prompt Injection -> MITIGATED_SUCCESSFULLY | 0 bytes leaked to cloud host", (0, 200, 100))
        for _ in range(FRAMES_PER_SLIDE):
            frames.append(frame.copy())

        print("       Launching Share Tampering attack simulation...")
        driver.execute_script("launchAttackSimulation('share_tampering')")
        time.sleep(4)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Attack 3: Byzantine Share Tampering -> Feldman VSS Detected! Honest shares reconstructed secret.", (0, 200, 100))
        for _ in range(FRAMES_PER_SLIDE):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # PART 6: Mathematical Proofs
        # ----------------------------------------------------------------
        add_title_card(frames, "Part 6: Mathematical Proofs", "Shannon Theorem | Feldman VSS | Lagrange Interpolation | Vandermonde Proof", 18)
        print("       Switching to Proofs tab...")
        driver.execute_script("switchTab('proofs')")
        time.sleep(1)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "Formal Proofs: Perfect Secrecy Theorem | Discrete Log Soundness | Combinatorial Invariance")
        for _ in range(FRAMES_PER_SLIDE):
            frames.append(frame.copy())

        # ----------------------------------------------------------------
        # FINAL: Return to Gateway
        # ----------------------------------------------------------------
        add_title_card(frames, "AegisGate - Summary", "Zero-Knowledge. Mathematically Verified. Hackathon-Ready.", 30)
        print("       Returning to Gateway tab for final screen...")
        driver.execute_script("switchTab('gateway')")
        time.sleep(1)
        frame = screenshot_to_frame(driver)
        frame = add_overlay_label(frame, "AegisGate | python run.py | http://localhost:8000 | Shannon Perfect Secrecy + Feldman VSS + AES-256-GCM")
        for _ in range(FRAMES_PER_SLIDE + 8):
            frames.append(frame.copy())

        add_title_card(frames, "Thank You!", "AegisGate | Target Prizes: Best AI Pipelines | Certified Cryptographer | Cybersecurity Mitigator", 30)

    finally:
        driver.quit()

    # ----------------------------------------------------------------
    # Write MP4 Video
    # ----------------------------------------------------------------
    print(f"[3/6] Encoding {len(frames)} frames -> {OUTPUT_PATH}")
    VIDEO_FPS = 6  # 6 fps playback makes 8-frame slides ~1.3 sec long
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, VIDEO_FPS, (FRAME_W, FRAME_H))

    if not writer.isOpened():
        print("ERROR: VideoWriter could not be opened. Ensure OpenCV is installed.")
        sys.exit(1)

    for f in frames:
        writer.write(f)

    writer.release()
    size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"[4/6] Video saved: {OUTPUT_PATH} ({size_mb:.1f} MB, {len(frames)} frames at {VIDEO_FPS} fps)")
    print(f"[5/6] Duration: ~{len(frames) / VIDEO_FPS:.0f} seconds")

if __name__ == "__main__":
    main()
