"""
AegisGate Interactive Terminal User Interface (TUI)
==================================================
Interactive CLI built with Rich providing:
- Real-time zero-knowledge AI pipeline execution
- Live Wiretap stream inspection
- Feldman VSS mathematical verification breakdown
- Interactive Adversarial Attack Suite
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt, Confirm
from core.blind_pipeline import BlindPipelineOrchestrator
from core.cryptoanalysis import CryptoanalysisSuite
from core.attack_simulator import AdversarialAttackSimulator

console = Console()

BANNER = """
[bold cyan]    ___    ______ _____ _____ _____ _____ ___  _____ _____ [/bold cyan]
[bold cyan]   / _ \  |  ____/ ____|_   _/ ____/ ____|   \/  __ \_   _|[/bold cyan]
[bold cyan]  / /_\ \ | |__ | |  __  | || (___| |  __| |\ | /  \/ | |  [/bold cyan]
[bold cyan]  |  _  | |  __|| | |_ | | | \___ \| | |_ | |/\| |     | |  [/bold cyan]
[bold cyan]  | | | | | |___| |__| |_| |_____) | |__| | |  | \__/\ | |  [/bold cyan]
[bold cyan]  \_| |_/ |______\_____|_____|_____/\_____|_|   \____/ |_|  [/bold cyan]
[bold magenta]  Mathematical Zero-Knowledge AI Pipeline Gateway (SSS + Feldman VSS)[/bold magenta]
"""

def render_pipeline_result(res: dict):
    console.print()
    # 1. Pipeline Telemetry Table
    t_table = Table(title="⚡ Cryptographic Telemetry & Audit", style="cyan")
    t_table.add_column("Metric", style="bold white")
    t_table.add_column("Value", style="green")

    t_table.add_row("Total Time", f"{res['telemetry']['total_time_ms']} ms")
    t_table.add_row("Client Crypto Shielding", f"{res['telemetry']['client_crypto_shield_ms']} ms")
    t_table.add_row("LLM Execution Duration", f"{res['telemetry']['llm_execution_ms']} ms")
    t_table.add_row("Client Lagrange Reconstruction", f"{res['telemetry']['client_lagrange_recon_ms']} ms")
    t_table.add_row("Zero-Knowledge Secrecy", res['telemetry']['zero_knowledge_guarantee'])
    t_table.add_row("Master Key Host Leakage", res['telemetry']['master_key_host_leakage'])
    t_table.add_row("LLM Provider Active", res['llm_provider'])

    console.print(t_table)
    console.print()

    # 2. Side-by-Side Wiretap vs Reconstructed
    wiretap_panel = Panel(
        Text(res["wiretap_inspected_payload"], style="yellow"),
        title="[bold red]📡 Cloud Host Wiretap (What OpenAI/Gemini/Bedrock Saw)[/bold red]",
        border_style="red"
    )
    console.print(wiretap_panel)
    console.print()

    recon_panel = Panel(
        Text(res["final_reconstructed_response"], style="bright_white"),
        title="[bold green]🔒 Local Client Plaintext (Lagrange Reconstructed)[/bold green]",
        border_style="green"
    )
    console.print(recon_panel)
    console.print()

    # 3. Polynomial Shares Table
    if res["curve_data"]:
        shares_table = Table(title="📐 Shamir (3-of-5) Verifiable Polynomial Shares GF(q)", style="magenta")
        shares_table.add_column("Index (x)", style="bold yellow")
        shares_table.add_column("Evaluated Share Value f(x) mod q", style="white")
        shares_table.add_column("Feldman VSS Hash", style="cyan")

        for row in res["curve_data"]:
            shares_table.add_row(str(row["x"]), row["y"], row["commitment_hash"])

        console.print(shares_table)
        console.print()

def run_cryptoanalysis_menu():
    console.print("\n[bold yellow]Running Rigorous Cryptoanalysis Suite...[/bold yellow]")
    with console.status("[bold green]Computing Shannon entropy, Feldman soundness, and combinatorial tests..."):
        suite = CryptoanalysisSuite()
        res = suite.run_full_cryptoanalysis(num_samples=30)

    table = Table(title="🛡️ Formal Cryptoanalysis Certification", style="bold green")
    table.add_column("Test Battery", style="white")
    table.add_column("Result", style="cyan")
    table.add_column("Status", style="bold")

    for k, v in res.items():
        if k == "overall_certification":
            continue
        status_text = "[bold green]PASSED (100%)[/bold green]" if v["passed"] else "[bold red]FAILED[/bold red]"
        detail = f"{v.get('mutual_information_bits', '')} bits leak" if 'mutual_information_bits' in v else (
            f"{v.get('detection_rate_pct', '')}% detected" if 'detection_rate_pct' in v else (
                f"{v.get('combinations_tested', '')} subsets congruent" if 'combinations_tested' in v else (
                    f"{v.get('measured_entropy_per_byte', '')} bits/byte" if 'measured_entropy_per_byte' in v else "Tamper Rejected"
                )
            )
        )
        table.add_row(v["name"], detail, status_text)

    console.print(table)
    console.print(Panel(
        f"[bold cyan]OVERALL STATUS:[/bold cyan] {res['overall_certification']['status']}\n"
        f"[bold cyan]SCORE:[/bold cyan] {res['overall_certification']['score_percentage']}%\n"
        f"[bold cyan]FIELD:[/bold cyan] 255-bit Safe Prime Group | [bold cyan]SECURITY:[/bold cyan] {res['overall_certification']['formal_guarantee']}",
        title="🏆 Certification Award",
        border_style="gold1"
    ))

def run_attack_menu():
    console.print("\n[bold red]⚔️ Adversarial Attack Simulation & Mitigation Console[/bold red]")
    console.print("1. Prompt Injection & Master Key Exfiltration Attack")
    console.print("2. Cloud Host Provider Compromise & Log Snooping")
    console.print("3. Byzantine Rogue Share Tampering in Transit")
    console.print("4. Run All Attack Vectors")
    choice = Prompt.ask("Select attack scenario", choices=["1", "2", "3", "4", "back"], default="4")

    sim = AdversarialAttackSimulator()

    if choice in ("1", "4"):
        console.print("\n[bold yellow]Simulating Attack 1: Prompt Injection...[/bold yellow]")
        r = sim.run_prompt_injection_attack()
        console.print(Panel(
            f"[bold red]Malicious Prompt:[/bold red] {r['malicious_prompt']}\n\n"
            f"[bold yellow]Sent to Host:[/bold yellow] {r['wire_payload_sent_to_host']}\n\n"
            f"[bold green]Defense Status:[/bold green] {r['defense_status']} (Secret bytes leaked: {r['leakage_bytes']})\n"
            f"[bold cyan]Mitigation:[/bold cyan] {r['mitigation_mechanism']}",
            title="Prompt Injection Defense Report",
            border_style="green"
        ))

    if choice in ("2", "4"):
        console.print("\n[bold yellow]Simulating Attack 2: Host Cloud Breach...[/bold yellow]")
        r = sim.run_host_breach_simulation()
        console.print(Panel(
            f"[bold yellow]Simulated Host Disk Log:[/bold yellow] {r['simulated_host_log_dump']['inbound_request_payload']}\n\n"
            f"[bold cyan]Entropy Analysis:[/bold cyan] {r['entropy_analysis']}\n\n"
            f"[bold green]Defense Status:[/bold green] {r['defense_status']} (Confidentiality Preserved = {r['confidentiality_preserved']})",
            title="Cloud Host Compromise Defense Report",
            border_style="green"
        ))

    if choice in ("3", "4"):
        console.print("\n[bold yellow]Simulating Attack 3: Rogue Share Tampering...[/bold yellow]")
        r = sim.run_rogue_share_tampering_attack()
        console.print(Panel(
            f"[bold red]Tampered Share #[{r['corrupted_share_index']}]:[/bold red] {r['tampered_value_prefix']}\n\n"
            f"[bold green]Feldman VSS Detection:[/bold green] Detected Corruption = {r['feldman_vss_detected_corruption']}\n\n"
            f"[bold cyan]Fault Tolerance:[/bold cyan] {r['byzantine_fault_tolerance']}\n\n"
            f"[bold green]Defense Status:[/bold green] {r['defense_status']} (Secret Reconstructed = {r['secret_reconstruction_match']})",
            title="Byzantine Share Tampering Defense Report",
            border_style="green"
        ))

def main():
    console.print(BANNER)
    orch = BlindPipelineOrchestrator()

    while True:
        console.print("\n[bold white]Select Option:[/bold white]")
        console.print("1. [bold cyan]Send Confidential AI Query[/bold cyan] (Zero-Knowledge SSS Pipeline)")
        console.print("2. [bold magenta]Run Formal Cryptoanalysis Battery[/bold magenta] (Target: Certified Cryptographer)")
        console.print("3. [bold red]Launch Adversarial Attack Simulator[/bold red] (Target: Cybersecurity Mitigator)")
        console.print("4. [bold yellow]Start Loopback Web UI[/bold yellow] (http://localhost:8000)")
        console.print("5. [bold white]Exit[/bold white]")

        choice = Prompt.ask("Option", choices=["1", "2", "3", "4", "5"], default="1")

        if choice == "1":
            default_prompt = (
                "Strategic review for Project Titan with quarterly revenue $84.2M "
                "and CEO SSN 049-22-9912. Forecast risk and compute margin."
            )
            user_input = Prompt.ask("\nEnter prompt (or press Enter for confidential sample)", default=default_prompt)
            with console.status("[bold green]Executing Zero-Knowledge SSS Sharding & Blind Pipeline..."):
                res = orch.process_secure_query(user_input, threshold_k=3, total_shares_n=5)
            render_pipeline_result(res)

        elif choice == "2":
            run_cryptoanalysis_menu()

        elif choice == "3":
            run_attack_menu()

        elif choice == "4":
            console.print("\n[bold green]Launching FastAPI server on http://localhost:8000 ...[/bold green]")
            import subprocess
            subprocess.run([sys.executable, "server.py"])

        elif choice == "5":
            console.print("[yellow]Exiting AegisGate. Stay secure.[/yellow]")
            break

if __name__ == "__main__":
    main()
