import subprocess
import json
import os
from rich.console import Console
from rich.progress import track
from modules.knowledge import get_knowledge

console = Console()

class Analyzer:
    def __init__(self, scan_results):
        self.scan_results = scan_results

    def analyze(self):
        """
        Iterates through scan results, looks for exploits, and enriches with KB.
        """
        analyzed_data = []

        for service in track(self.scan_results, description="Correlating Exploits..."):
            full_name = service['full_name']
            
            # Enrich with Knowledge Base
            kb_info = get_knowledge(service['name'])
            service['description'] = kb_info['description']
            service['impact'] = kb_info['impact']
            service['mitigation'] = kb_info['mitigation']

            if len(full_name) < 3: 
                analyzed_data.append(service) # Keep service even if no long name
                continue
                
            console.print(f"[dim]Checking exploits for: {full_name}[/dim]")
            
            exploits = self._search_exploits(full_name)
            
            # Update the existing service dict references
            service['exploits'] = exploits
            analyzed_data.append(service)
            
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
                        extracted_info = self._extract_steps(full_path)
                        
                        found_exploits.append({
                            'title': title,
                            'path': exploit_path,
                            'full_path': full_path,
                            'steps': extracted_info['steps'],
                            'code_snippet': extracted_info['code_snippet']
                        })
                return found_exploits
                
            except json.JSONDecodeError:
                return []

        except FileNotFoundError:
            console.print("[yellow]Warning: 'searchsploit' not found. Is it installed?[/yellow]")
            return []
            
    def _extract_steps(self, file_path):
        """
        Attempts to read the file to find usage instructions or code snippets.
        """
        info = {
            'steps': "No automated steps found. Please review the file.",
            'code_snippet': ""
        }
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', errors='ignore') as f:
                    content = f.read(4096) # Read first 4KB
                    
                    # 1. EXTRACT USAGE
                    if "Usage:" in content:
                        start = content.find("Usage:")
                        end = content.find("\n", start + 200) # Grab roughly a line or two
                        info['steps'] = content[start:end].strip()
                    elif "USAGE" in content:
                        start = content.find("USAGE")
                        end = content.find("\n", start + 200)
                        info['steps'] = content[start:end].strip()
                    
                    # 2. EXTRACT CODE SNIPPET (Python/Bash)
                    # Simple heuristic: Look for import or shebang
                    if "import " in content or "#!/bin" in content:
                        lines = content.splitlines()
                        snippet = []
                        # Grab the first non-comment code lines (simplified)
                        count = 0
                        for line in lines:
                            if count > 15: break # Max 15 lines of snippet
                            if line.strip() and not line.startswith(('#', '//', '/*')):
                                snippet.append(line)
                                count += 1
                        
                        if snippet:
                             info['code_snippet'] = "\n".join(snippet)
                             
        except Exception:
            pass
            
        return info
