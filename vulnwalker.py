#!/usr/bin/env python3
import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from modules.scanner import Scanner
from modules.analyzer import Analyzer
from modules.reporter import Reporter

console = Console()

def main():
    parser = argparse.ArgumentParser(description="VulnWalker - Vulnerability Correlation & Exploit Assistant")
    parser.add_argument("-t", "--target", help="Target IP or Hostname", required=True)
    parser.add_argument("-o", "--output", help="Output report filename", default="vulnwalker_report.html")
    parser.add_argument("--deep", action="store_true", help="Enable deep scan (Nmap NSE scripts)")
    
    args = parser.parse_args()
    
    console.print(Panel.fit("[bold red]VulnWalker[/bold red] - [bold white]Walking the Path of Vulnerabilities[/bold white]", subtitle="[yellow]v1.0[/yellow]"))
    
    # 1. SCANNING
    scanner = Scanner(args.target, args.deep)
    with console.status(f"[bold cyan]Scanning {args.target}...[/bold cyan]", spinner="dots"):
        scan_results = scanner.run_scan()
    
    if not scan_results:
        console.print("[bold red][!] Scan failed or no info found.[/bold red]")
        sys.exit(1)
        
    console.print(f"[+] Scan complete. Found [bold green]{len(scan_results)}[/bold green] services.")

    # 2. ANALYSIS
    console.print("\n[+] Analyzing services for CVEs and Exploits...")
    analyzer = Analyzer(scan_results)
    analysis_results = analyzer.analyze()
    
    # 3. REPORTING
    console.print(f"\n[+] Generating report: [bold yellow]{args.output}[/bold yellow]...")
    reporter = Reporter(analysis_results, args.output, args.target)
    reporter.generate()
    
    console.print("\n[bold green][*] Mission Complete![/bold green] check your report for details.")

if __name__ == "__main__":
    main()
