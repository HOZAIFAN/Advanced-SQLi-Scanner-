# Advanced-SQLi-Scanner-
 "Advanced SQL Injection Automation Framework for Bug Bounty &amp; Pentesting"

 
 # 🔍 SQLiAutoPwn - Advanced SQL Injection Automation Framework

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20WSL-blue.svg)

**SQLiAutoPwn** is an intelligent, automated SQL injection detection and exploitation tool that combines the power of SQLMap with smart automation. It automatically detects injection points and performs comprehensive attacks with minimal user input.

---

## 🌟 Key Features

### 🔄 Smart Detection
- Auto-detects injection types (GET, POST, Cookie, Headers, APIs)
- Multi-threaded parameter testing for faster scanning
- Intelligent vulnerability classification

### 📊 Comprehensive Enumeration
- Full database mapping (databases, tables, columns)
- Credential extraction (usernames, password hashes)
- Privilege and role enumeration

### ⚡ Advanced Exploitation
- OS-level access (shells, file read/write, command execution)
- Registry access (Windows targets)
- Custom tampering scripts for evasion
- Session management for resuming scans

### 📈 Professional Reporting
- HTML reports with visualizations
- JSON export for integration with other tools
- Markdown reports for documentation
- Organized file structure

### 🛡️ Stealth & Evasion
- Random user agents
- Request throttling
- WAF/IDS evasion techniques
- Tor support (when configured)

---

## 🚀 Quick Start

### Prerequisites
```bash
# 1. Install Python 3.7+
python3 --version

# 2. Install SQLMap (Required)
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
cd sqlmap
python3 sqlmap.py --version

# 3. Install Python dependencies
pip install requests colorama beautifulsoup4
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/sqliautopwn.git
cd sqliautopwn

# Make script executable
chmod +x sqli_autopwn.py

# Run basic scan
python3 sqli_autopwn.py http://target.com/page?id=1
```

---

## 📖 Usage Examples

### Basic Scanning
```bash
# 1. Basic GET parameter scan
python3 sqli_autopwn.py "http://vuln-site.com/product.php?id=1"

# 2. Scan with authentication cookie
python3 sqli_autopwn.py "http://admin.site.com/dashboard" --cookie "PHPSESSID=abc123; auth=xyz"

# 3. Scan POST login form
python3 sqli_autopwn.py "http://site.com/login.php" --post-data "username=admin&password=test"
```

### Advanced Scanning
```bash
# 4. Test specific parameter only
python3 sqli_autopwn.py "http://site.com/search?q=test" --param "q"

# 5. Stealth mode with delays
python3 sqli_autopwn.py "http://site.com/page?id=1" --stealth --delay 2

# 6. Maximum aggression
python3 sqli_autopwn.py "http://site.com/vuln.php" --aggressive --technique ALL
```

---

## 📁 How It Works

### Phase 1: Detection (What it finds)
1. Check if target website is online
2. Look for URL parameters (?id=1, ?user=admin)
3. Search for login forms and search boxes
4. Test cookies and headers
5. Identify API endpoints

### Phase 2: Testing (How it tests)
1. Send harmless test payloads
2. Analyze website responses
3. Identify vulnerable parameters
4. Determine database type (MySQL, PostgreSQL, etc.)

### Phase 3: Exploitation (What it extracts)
1. Get database information
2. List all databases and tables
3. Extract usernames and passwords
4. Try to get system access

### Phase 4: Reporting (What you get)
1. HTML report with all findings
2. JSON data for analysis
3. Saved database dumps
4. Session files for resuming

---

## 🛠️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `target` | Target URL (required) | `http://site.com/page?id=1` |
| `--cookie` | Authentication cookie | `--cookie "session=abc123"` |
| `--post-data` | POST request data | `--post-data "login=admin&pass=test"` |
| `--param` | Test specific parameter | `--param "id"` |
| `--stealth` | Enable stealth mode | `--stealth` |
| `--aggressive` | Enable aggressive mode | `--aggressive` |
| `--delay` | Delay between requests | `--delay 1.5` |
| `--output` | Custom output directory | `--output ./my_scan` |
| `--help` | Show help message | `--help` |

---

## 📊 Output Structure

After a scan, you'll get this organized folder structure:

```
sqli_results_abc123def/
├── 📁 detection/           # Initial detection results
│   ├── get_id.json        # GET parameter findings
│   ├── forms.log          # Form detection logs
│   └── headers.txt        # Header injection tests
│
├── 📁 enumeration/         # Database information
│   ├── databases.txt      # List of all databases
│   ├── tables.csv         # All tables found
│   └── users.json         # User accounts extracted
│
├── 📁 exploitation/        # Advanced attack results
│   ├── os_shell.log       # OS command execution
│   ├── file_read.txt      # Files read from server
│   └── data_dump/         # Full database dumps
│
├── 📁 reports/            # Generated reports
│   ├── report.html        # HTML report (open in browser)
│   ├── report.md          # Markdown report
│   └── full_report.json   # JSON data
│
├── 📁 sessions/           # SQLMap session files
│   └── session_abc.sqmap  # Resume scans later
│
└── 📁 logs/               # Detailed execution logs
    └── command_123.log    # All commands run
```

---

## 🎯 Use Cases

### 1. For Penetration Testers
```bash
# Quick security assessment
python3 sqli_autopwn.py http://client-site.com --stealth

# Comprehensive penetration test
python3 sqli_autopwn.py http://admin.client.com --cookie "admin_token=xyz"
```

### 2. For Bug Bounty Hunters
```bash
# Fast scanning of new targets
python3 sqli_autopwn.py https://*.bugbounty.com --aggressive

# Focus on specific endpoints
python3 sqli_autopwn.py https://api.target.com/v1/users --param "user_id"
```

### 3. For Security Researchers
```bash
# Study SQL injection patterns
python3 sqli_autopwn.py http://test-site.com --output ./research_data

# Test evasion techniques
python3 sqli_autopwn.py http://waf-protected.com --stealth --delay 3
```

### 4. For CTF Players
```bash
# Solve SQL injection challenges
python3 sqli_autopwn.py http://ctf.server.com/challenge1

# Extract flags automatically
python3 sqli_autopwn.py http://ctf.site.com/admin.php --cookie "token=flag"
```

---

## ⚖️ Pros and Cons

### ✅ Advantages

| Advantage | Explanation |
|-----------|-------------|
| **Fully Automated** | One command does everything |
| **Smart Detection** | Finds injection points automatically |
| **Comprehensive** | Gets databases, tables, data, and system access |
| **Professional Reports** | HTML reports with visualizations |
| **Easy to Use** | Simple commands, no complex setup |
| **Session Management** | Pause and resume scans anytime |
| **Stealth Options** | Avoid detection with built-in evasion |

### ❌ Limitations

| Limitation | Explanation |
|------------|-------------|
| **Requires SQLMap** | Must have SQLMap installed |
| **Can Be Noisy** | Generates many requests (use --stealth) |
| **False Positives** | May report non-existent vulnerabilities |
| **Learning Curve** | Beginners need to understand SQL injection basics |
| **Legal Restrictions** | Can only test authorized systems |

---

## 🚨 Legal & Ethical Use

### ⚠️ IMPORTANT WARNING

**This tool must ONLY be used for:**
- ✅ Testing your own websites
- ✅ Authorized penetration testing (with written permission)
- ✅ CTF challenges and practice labs
- ✅ Educational purposes in controlled environments

**NEVER use this tool on:**
- ❌ Websites you don't own
- ❌ Systems without explicit permission
- ❌ Production environments without authorization

### Legal Consequences
- Unauthorized testing is **illegal**
- Can result in **fines and imprisonment**
- Violates **Computer Fraud and Abuse Act**
- Considered **cybercrime** in most countries

### Safe Testing Environments
```bash
# Use these safe practice platforms:
- TryHackMe (https://tryhackme.com)
- HackTheBox (https://hackthebox.com)
- PentesterLab (https://pentesterlab.com)
- DVWA (Damn Vulnerable Web App)
- WebGoat
```

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "SQLMap not found" | Install SQLMap: `git clone https://github.com/sqlmapproject/sqlmap.git` |
| "Permission denied" | Run: `chmod +x sqli_autopwn.py` |
| "Target unreachable" | Check network, URL format (include http://) |
| "No vulnerabilities found" | Target might be secure or use different parameters |
| "Scan is too slow" | Use `--aggressive` or reduce `--delay` |
| "Getting blocked" | Use `--stealth` and increase `--delay` |

### Verbose Mode
```bash
# See detailed progress
python3 sqli_autopwn.py http://target.com -v

# Check logs for errors
ls -la sqli_results_*/logs/
```
---

## 🔧 Advanced Configuration

### Customizing the Tool
```python
# Edit these variables in the script for customization:
USER_AGENTS = [...]  # Add your own user agents
TAMPERS = [...]      # Custom tamper scripts
DELAY = 0.5          # Default delay between requests
THREADS = 5          # Number of parallel threads
```

### Integration with Other Tools
```bash
# 1. Use with Nmap
nmap -sV target.com -oN nmap_scan.txt
python3 sqli_autopwn.py http://target.com

# 2. Use with Nikto
nikto -h target.com
python3 sqli_autopwn.py http://target.com/admin

# 3. Parse results with jq
cat results_*/reports/full_report.json | jq '.vulnerabilities[]'
```

---

## 📚 Learning Resources

### Learn SQL Injection
- [OWASP SQL Injection Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLMap Documentation](https://github.com/sqlmapproject/sqlmap/wiki)
- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection)

### Practice Safely
- [TryHackMe SQL Injection Rooms](https://tryhackme.com)
- [HackTheBox Web Challenges](https://hackthebox.com)
- [DVWA Installation Guide](http://www.dvwa.co.uk)

### Secure Your Applications
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Parameterized Query Examples](https://bobby-tables.com)

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement
- Add more evasion techniques
- Improve reporting formats
- Add API scanning capabilities
- Create Docker container
- Add GUI interface

---
## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2023 Muhammad Hozaifa Naeem**

## 📦 Dependencies

```
requests>=2.28.0
colorama>=0.4.6
beautifulsoup4>=4.11.0
```

Install with: `pip install -r requirements.txt`

---

## 🌟 Support

If you find this tool useful:
- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest features
- 🔄 Share with others

---

## 📄 Disclaimer

**This tool is for educational and authorized testing purposes only.** The developers are not responsible for misuse or damage caused by this tool. Always obtain proper authorization before testing any system you do not own.

---

## 🎓 Remember

> **"With great power comes great responsibility. Always use ethical hacking tools responsibly."**

---

**Made with ❤️ by Security Researchers**

**Last Updated:** January 2026
