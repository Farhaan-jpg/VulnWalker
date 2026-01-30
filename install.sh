
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

echo "[*] Installing system dependencies (nmap, exploitdb)..."
apt-get install -y nmap exploitdb python3 python3-pip

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages

echo "[*] Fixing line endings for Linux..."
sed -i 's/\r$//' vulnwalker.py

echo "[*] Making script executable..."
chmod +x vulnwalker.py

echo "[*] Creating symlink to /usr/local/bin/vulnwalker..."
ln -sf "$(pwd)/vulnwalker.py" /usr/local/bin/vulnwalker

echo "[+] Installation complete!"
echo "    Usage: vulnwalker -t <target>"
