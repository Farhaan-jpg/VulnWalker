# VulnWalker
> A Kali Linux CLI tool for automated service scanning and vulnerability correlation.

**VulnWalker** maps out the attack surface by scanning for running services and immediately correlating them with known exploits from the local Exploit-DB database. It generates actionable reports to help security researchers verify vulnerabilities efficiently.

**Note:** This tool does NOT auto-exploit. It finds the door and gives you the key, but you must turn it yourself.

## Features
- **Fast Scanning**: Wraps Nmap for reliable service detection (`-sV`).
- **Exploit Correlation**: Queries `searchsploit` (Exploit-DB) offline.
- **Actionable Reporting**: Generates Markdown reports with exploit paths and usage steps.
- **Safe**: No automatic exploitation.

## Installation (Kali Linux)
```bash
git clone https://github.com/your-username/vulnwalker.git
cd vulnwalker
sudo bash install.sh
```
*Note: This will automatically set up a virtual environment and system dependencies.*

## Usage
Basic scan:
```bash
vulnwalker -t <target-ip>
```

Save to specific file:
```bash
vulnwalker -t 192.168.1.10 -o my_scan.md
```

## Requirements
- Python 3.x
- Nmap
- Exploit-DB (`searchsploit`)
- Root privileges (for Nmap)
