import subprocess
import json
import os
from rich.console import Console
from rich.progress import track

console = Console()

class Analyzer:
    def __init__(self, scan_results):
        self.scan_results = scan_results

    def analyze(self):
        """
        Iterates through scan results and looks for exploits using searchsploit.
        """
        analyzed_data = []

        for service in track(self.scan_results, description="Correlating Exploits..."):
            full_name = service['full_name']
            if len(full_name) < 3: # Skip empty or too short names
                continue
                
            console.print(f"[dim]Checking exploits for: {full_name}[/dim]")
            
            exploits = self._search_exploits(full_name)
            
            entry = service.copy()
            entry['exploits'] = exploits
            analyzed_data.append(entry)
            
            if exploits:
                console.print(f"    [bold red]![/bold red] Found {len(exploits)} potential exploits for {full_name}")

        return analyzed_data

    def _search_exploits(self, query):
        """
        Uses searchsploit --json to find exploits.
        """
        try:
            # Run searchsploit query
            cmd = ['searchsploit', '--json', query]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return []
                
            try:
                data = json.loads(result.stdout)
                found_exploits = []
                
                # Retrieve the top 5 most relevant exploits
                if 'RESULTS_EXPLOIT' in data:
                    for exploit in data['RESULTS_EXPLOIT'][:5]:
                        exploit_path = exploit.get('Path', '')
                        title = exploit.get('Title', 'Unknown')
                        
                        # Get full path to read file content later if needed
                        # usually in /usr/share/exploitdb/exploits/
                        full_path = f"/usr/share/exploitdb/{exploit_path}"
                        
                        # If possible, read the file to extract comments/steps (simplified here)
                        steps = self._extract_steps(full_path)
                        
                        found_exploits.append({
                            'title': title,
                            'path': exploit_path,
                            'full_path': full_path,
                            'steps': steps
                        })
                return found_exploits
                
            except json.JSONDecodeError:
                return []

        except FileNotFoundError:
            console.print("[yellow]Warning: 'searchsploit' not found. Is it installed?[/yellow]")
            return []
            
    def _extract_steps(self, file_path):
        """
        Attempts to read the beginning of the exploit file to find usage instructions.
        """
        steps = "Steps not automatically extracted. Check the file header."
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read(2048) # Read first 2KB
                    # Heuristic: verify if it has a 'Usage' or 'Steps' section
                    if "Usage:" in content or "USAGE" in content:
                        steps = "Usage instructions found in file header."
                    elif "#" in content or "/*" in content:
                         steps = "Review file comments for execution steps."
        except Exception:
            pass
        return steps
