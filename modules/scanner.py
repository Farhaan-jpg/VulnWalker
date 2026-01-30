import nmap
import sys
from rich.console import Console

console = Console()

class Scanner:
    def __init__(self, target, deep_scan=False):
        self.target = target
        self.deep_scan = deep_scan
        self.nm = nmap.PortScanner()
        
    def run_scan(self):
        """
        Runs nmap -sV (and optionally --script vuln) on the target.
        Returns a list of dictionaries with service info.
        """
        try:
            # Basic args
            nm_args = '-sV -T4 --open'
            
            if self.deep_scan:
                console.print(f"[bold yellow][!] Deep scan enabled. This might take a while...[/bold yellow]")
                nm_args += ' --script vuln'

            console.print(f"[dim]Running: nmap {nm_args} {self.target}[/dim]")
            self.nm.scan(self.target, arguments=nm_args)
            
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
                        
                        # Extract script output (vuln scripts)
                        script_output = ""
                        if 'script' in service:
                             for script_id, output in service['script'].items():
                                 script_output += f"\n**{script_id}**:\n```\n{output}\n```\n"

                        results.append({
                            'port': port,
                            'protocol': proto,
                            'name': service.get('name', 'unknown'),
                            'product': service_name,
                            'version': version,
                            'full_name': full_name,
                            'script_output': script_output
                        })
                        console.print(f"    - Port {port}: [bold]{full_name}[/bold]")
                        
            return results

        except Exception as e:
            console.print(f"[bold red]Error during scan:[/bold red] {e}")
            return []
