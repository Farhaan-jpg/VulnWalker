import os
from datetime import datetime

class Reporter:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
        
    def generate(self):
        """
        Generates a Markdown report.
        """
        try:
            with open(self.filename, 'w') as f:
                f.write(f"# VulnWalker Report\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Services Found:** {len(self.data)}\n\n")
                f.write("---\n")
                
                for item in self.data:
                    f.write(f"## Port {item['port']} ({item['protocol']})\n")
                    f.write(f"- **Service:** {item['name']}\n")
                    f.write(f"- **Product:** {item['product']}\n")
                    f.write(f"- **Version:** {item['version']}\n")
                    f.write(f"- **Full Name:** {item['full_name']}\n\n")
                    
                    if item.get('exploits'):
                        f.write(f"### ⚠️ Potential Exploits\n")
                        for exploit in item['exploits']:
                            f.write(f"#### {exploit['title']}\n")
                            f.write(f"- **Path:** `{exploit['path']}`\n")
                            f.write(f"- **Command to mirror:** `searchsploit -m {exploit['path']}`\n")
                            f.write(f"- **Steps/Usage Hint:** {exploit['steps']}\n")
                            f.write("\n")
                    else:
                        f.write(f"*No immediate exploits found in local database.*\n")
                    
                    f.write("---\n")
                    
            print(f"[+] Report successfully saved to {os.path.abspath(self.filename)}")
            return True
            
        except Exception as e:
            print(f"[!] Error writing report: {e}")
            return False
