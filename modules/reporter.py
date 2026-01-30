import os
import html
from datetime import datetime

class Reporter:
    def __init__(self, data, filename, target):
        self.data = data
        self.filename = filename
        self.target = target
        
    def generate(self):
        """
        Generates a professional HTML report.
        """
        try:
            html_content = self._build_html()
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"[+] Report successfully saved to {os.path.abspath(self.filename)}")
            return True
            
        except Exception as e:
            print(f"[!] Error writing report: {e}")
            return False

    def _build_html(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        service_count = len(self.data)
        
        # CSS Styling
        style = """
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --danger: #ef4444;
            --warning: #f59e0b;
            --success: #22c55e;
            --border: #334155;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        header {
            border-bottom: 1px solid var(--border);
            padding-bottom: 2rem;
            margin-bottom: 3rem;
        }
        h1 { font-size: 2.5rem; margin: 0 0 0.5rem 0; color: var(--accent); }
        .meta { color: var(--text-secondary); font-size: 0.9rem; }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        .stat-card {
            background: var(--card-bg);
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 1px solid var(--border);
            text-align: center;
        }
        .stat-val { display: block; font-size: 2rem; font-weight: bold; color: var(--success); }
        .stat-label { color: var(--text-secondary); font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em; }
        
        .service-card {
            background: var(--card-bg);
            border-radius: 1rem;
            border: 1px solid var(--border);
            margin-bottom: 2rem;
            overflow: hidden;
        }
        .service-header {
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .service-title { font-size: 1.25rem; font-weight: 600; display: flex; align-items: center; gap: 0.75rem; }
        .port-badge { 
            background: var(--accent); color: #000; 
            padding: 0.25rem 0.75rem; border-radius: 999px; 
            font-size: 0.875rem; font-weight: bold;
        }
        .service-body { padding: 1.5rem; }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .section-title {
            color: var(--accent);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        .info-box { background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 0.5rem; }
        
        .exploit-section { margin-top: 2rem; border-top: 1px dashed var(--border); padding-top: 1.5rem; }
        .exploit-card {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .exploit-title { color: var(--danger); font-weight: bold; margin-bottom: 0.5rem; display: block; }
        
        pre {
            background: #000;
            padding: 1rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            font-size: 0.875rem;
            color: #ccc;
            border: 1px solid #333;
        }
        code { font-family: 'Consolas', 'Monaco', monospace; }
        
        .tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; background: #334155; }
        .tag-vuln { background: #7f1d1d; color: #fca5a5; }
        </style>
        """
        
        # HTML Header
        doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VulnWalker Report - {self.target}</title>
    <style>{style}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>VulnWalker Report</h1>
            <div class="meta">
                Target: <strong>{self.target}</strong> &bull; Date: {timestamp}
            </div>
        </header>
        
        <div class="summary-grid">
            <div class="stat-card">
                <span class="stat-val">{service_count}</span>
                <span class="stat-label">Open Ports</span>
            </div>
            <div class="stat-card">
                <span class="stat-val">{sum(1 for i in self.data if i.get('exploits'))}</span>
                <span class="stat-label">Vulnerable Services</span>
            </div>
             <div class="stat-card">
                <span class="stat-val">{sum(len(i.get('exploits', [])) for i in self.data)}</span>
                <span class="stat-label">Potential Exploits</span>
            </div>
        </div>
        """
        
        # Service Cards
        for item in self.data:
            doc += self._build_service_card(item)
            
        doc += """
        <footer style="text-align: center; color: var(--text-secondary); margin-top: 4rem; padding-bottom: 2rem;">
            Generated by <strong>VulnWalker Pro</strong>
        </footer>
    </div>
</body>
</html>
        """
        return doc

    def _build_service_card(self, item):
        product_ver = f"{item['product']} {item['version']}".strip()
        
        # Sanitize text
        desc = html.escape(item.get('description', 'N/A'))
        impact = html.escape(item.get('impact', 'N/A'))
        mitigation = html.escape(item.get('mitigation', 'N/A'))
        
        card = f"""
        <div class="service-card">
            <div class="service-header">
                <div class="service-title">
                    <span class="port-badge">{item['port']}/{item['protocol']}</span>
                    {html.escape(item['name'].upper())}
                </div>
                <div style="color: var(--text-secondary);">{html.escape(product_ver)}</div>
            </div>
            <div class="service-body">
                <div class="info-grid">
                    <div class="info-box">
                        <div class="section-title">Description</div>
                        {desc}
                    </div>
                    <div class="info-box">
                        <div class="section-title">Potential Impact</div>
                        {impact}
                    </div>
                    <div class="info-box">
                        <div class="section-title">Mitigation</div>
                        {mitigation}
                    </div>
                </div>
        """
        
        # Deep Scan Output
        if item.get('script_output'):
            safe_output = html.escape(item['script_output']).replace("\n", "<br>")
            # Simple markdown-like bold parsing for nmap output key/vals
            safe_output = safe_output.replace("**", "") 
            card += f"""
            <div style="margin-top: 1.5rem;">
                <div class="section-title">🔍 Deep Scan Evidence (Nmap NSE)</div>
                <pre>{safe_output}</pre>
            </div>
            """

        # Exploits
        if item.get('exploits'):
            card += f"""<div class="exploit-section">
                <div class="section-title" style="color: var(--danger);">💣 Potential Exploits ({len(item['exploits'])})</div>"""
                
            for exploit in item['exploits']:
                card += f"""
                <div class="exploit-card">
                    <span class="exploit-title">{html.escape(exploit['title'])}</span>
                    <div style="margin-bottom: 0.5rem; font-size: 0.9rem;">
                        <span class="tag">Path: {exploit['path']}</span>
                        <span class="tag">Mirror: searchsploit -m {exploit['path']}</span>
                    </div>
                """
                
                if exploit.get('steps'):
                    card += f"""
                    <div style="margin-top: 0.5rem; background: rgba(0,0,0,0.3); padding: 0.5rem; border-radius: 4px; font-size: 0.9rem;">
                        <strong>Usage Hint:</strong> {html.escape(exploit['steps'])}
                    </div>
                    """
                    
                if exploit.get('code_snippet'):
                    card += f"""
                    <div style="margin-top: 0.5rem;">
                        <details>
                            <summary style="cursor: pointer; color: var(--accent); font-size: 0.9rem;">View Exploit Snippet</summary>
                            <pre style="margin-top: 0.5rem;">{html.escape(exploit['code_snippet'])}</pre>
                        </details>
                    </div>
                    """
                
                card += "</div>"
            card += "</div>"
            
        card += """
            </div>
        </div>
        """
        return card
