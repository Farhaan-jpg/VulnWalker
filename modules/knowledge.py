# Common service descriptions and impacts for reporting
SERVICE_KNOWLEDGE = {
    'ftp': {
        'description': "File Transfer Protocol (FTP) is a standard network protocol used for the transfer of computer files between a client and server on a computer network.",
        'impact': "Attackers often target FTP to gain unauthorized access to files, upload malicious content, or leverage weak credentials (anonymous login).",
        'mitigation': "Disable anonymous access, use SFTP/FTPS instead of plain FTP, and enforce strong passwords."
    },
    'ssh': {
        'description': "Secure Shell (SSH) is a cryptographic network protocol for operating network services securely over an unsecured network.",
        'impact': "Compromised SSH access gives attackers full remote control over the system. Weak keys or passwords are common vectors.",
        'mitigation': "Disable root login, use key-based authentication, and implement Fail2Ban."
    },
    'http': {
        'description': "Hypertext Transfer Protocol (HTTP) is the foundation of data communication for the World Wide Web.",
        'impact': "Web services are the most common attack surface. Vulnerabilities include SQLi, XSS, RCE, and information disclosure.",
        'mitigation': "Regularly update web server software, use a WAF, and secure configuration (disable directory listing, remove default pages)."
    },
    'https': {
        'description': "Hypertext Transfer Protocol Secure (HTTPS) is an extension of the Hypertext Transfer Protocol (HTTP).",
        'impact': "While encrypted, HTTPS services are still vulnerable to web application attacks (SQLi, XSS, etc.) and SSL/TLS misconfigurations.",
        'mitigation': "Ensure strong cipher suites, disable old protocols (SSLv3, TLS 1.0), and keep certificates valid."
    },
    'telnet': {
        'description': "Telnet is an application protocol used on the Internet or local area network to provide a bidirectional interactive text-oriented communication facility using a virtual terminal connection.",
        'impact': "Telnet sends data (including passwords) in plain text. An attacker on the network can sniff credentials easily.",
        'mitigation': "Disable Telnet immediately and replace it with SSH."
    },
    'smb': {
        'description': "Server Message Block (SMB) is a communication protocol for providing shared access to files, printers, and serial ports between nodes on a network.",
        'impact': "SMB is a frequent target for ransomware (e.g., EternalBlue) and lateral movement within networks.",
        'mitigation': "Disable SMBv1, enforce message signing, and restrict access via firewall."
    },
    'mysql': {
        'description': "MySQL is an open-source relational database management system.",
        'impact': "Exposed databases can lead to massive data theft. Weak credentials can allow attackers to dump the entire database.",
        'mitigation': "Bind to localhost if remote access isn't needed, use strong passwords, and update regularly."
    },
    'rdp': {
        'description': "Remote Desktop Protocol (RDP) provides a user with a graphical interface to connect to another computer over a network connection.",
        'impact': "RDP is a prime target for brute-force attacks and ransomware deployment.",
        'mitigation': "Use a VPN for access, enforce NLA (Network Level Authentication), and use strong passwords."
    }
}

def get_knowledge(service_name):
    """
    Returns a dictionary with details for a given service name (fuzzy match).
    """
    service_name = service_name.lower()
    for key, info in SERVICE_KNOWLEDGE.items():
        if key in service_name:
            return info
    return {
        'description': "No specific description available for this service.",
        'impact': "Any exposed service increases the attack surface and should be audited.",
        'mitigation': "Follow 'Least Privilege' and 'Defense in Depth' principles."
    }
