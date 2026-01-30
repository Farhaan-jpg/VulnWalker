import nmap
import sys
from rich.console import Console

console = Console()

class Scanner:
    def __init__(self, target):
        self.target = target
        self.nm = nmap.PortScanner()
        
    def run_scan(self):
        """
        Runs nmap -sV (Service Version Detection) on the target.
        Returns a list of dictionaries with service info.
        """
        try:
            # -sV: Service Version
            # -T4: Faster timing
            # --open: Only show open ports
            console.print(f"[dim]Running: nmap -sV -T4 --open {self.target}[/dim]")
            self.nm.scan(self.target, arguments='-sV -T4 --open')
            
            results = []
            
            for host in self.nm.all_hosts():
                console.print(f"[+] Host found: {host} ({self.nm[host].hostname()})")
                
                for proto in self.nm[host].all_protocols():
                    lport = self.nm[host][proto].keys()
                    for port in lport:
                        service = self.nm[host][proto][port]
                        service_name = service.get('product', 'unknown')
                        version = service.get('version', '')
                        full_name = f"{service_name} {version}".strip()
                        
                        results.append({
                            'port': port,
                            'protocol': proto,
                            'name': service.get('name', 'unknown'),
                            'product': service_name,
                            'version': version,
                            'full_name': full_name
                        })
                        console.print(f"    - Port {port}: [bold]{full_name}[/bold]")
                        
            return results

        except Exception as e:
            console.print(f"[bold red]Error during scan:[/bold red] {e}")
            return []
