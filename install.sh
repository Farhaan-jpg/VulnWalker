#!/bin/bash

# VulnWalker Installer for Kali Linux
# Run with: sudo ./install.sh

echo "[*] checking permissions..."
if [ "$EUID" -ne 0 ]
  then echo "Please run as root (sudo ./install.sh)"
  exit
fi

echo "[*] Updating apt cache..."
apt-get update -y

echo "[*] Installing system dependencies..."
apt-get install -y nmap exploitdb python3 python3-pip python3-venv

echo "[*] Setting up Python Virtual Environment..."
# Remove old venv if it exists
rm -rf venv
python3 -m venv venv

echo "[*] Installing Python dependencies into venv..."
./venv/bin/pip install -r requirements.txt

echo "[*] Fixing line endings for Linux..."
sed -i 's/\r$//' vulnwalker.py

echo "[*] Creating entry point..."
# Create a wrapper script that uses the venv python
cat <<EOF > /usr/local/bin/vulnwalker
#!/bin/bash
cd "$(pwd)"
"$(pwd)/venv/bin/python3" vulnwalker.py "\$@"
EOF

chmod +x /usr/local/bin/vulnwalker

echo "[+] Installation complete!"
echo "    Usage: vulnwalker -t <target>"
