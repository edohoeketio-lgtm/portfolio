import smtplib
import subprocess
import socket
import csv
import time
import requests
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

SAFE_CSV_PATH = "/home/sk/Downloads/Style DNA/execution/massive_leads_safe.csv"
TARGET_LEADS = 600

import string

# We will dynamically generate an infinite stream of possible startup domains
TECH_SUFFIXES = ['.com', '.io', '.ai', '.co', '.dev', '.app', '.net', '.inc']
STARTUP_WORDS = ['tech', 'labs', 'cloud', 'data', 'systems', 'soft', 'hub', 'base', 'stack', 'pay', 'health', 'fin', 'web', 'app', 'code']

def generate_domain_batch(size=500):
    domains = set()
    while len(domains) < size:
        # Generate random startup-sounding names: e.g. "bluelabs", "apexdata", or just random 5-9 char strings
        if random.random() > 0.5:
            word1 = random.choice(['blue', 'apex', 'nova', 'zen', 'core', 'shift', 'pulse', 'nexus', 'omni', 'tru'])
            word2 = random.choice(STARTUP_WORDS)
            domain = f"{word1}{word2}"
        else:
            length = random.randint(5, 9)
            domain = ''.join(random.choices(string.ascii_lowercase, k=length))
        
        domain += random.choice(TECH_SUFFIXES)
        domains.add(domain)
    return list(domains)

# High-probability engineering leader / founder email prefixes
PREFIXES = [
    "cto", "engineering", "founders", "ceo", "tech", "careers", "jobs", "hello",
    "alex", "david", "chris", "mike", "sarah", "emily", "matt", "jessica", "daniel", "john",
    "founder", "engineering-leadership"
]

def get_mx_record(domain):
    try:
        result = subprocess.check_output(['dig', '+short', 'MX', domain], text=True, timeout=5)
        records = result.strip().split('\n')
        if not records or not records[0]:
            return None
        records.sort(key=lambda x: int(x.split()[0]) if len(x.split()) > 1 else float('inf'))
        return records[0].split()[1].rstrip('.')
    except Exception:
        return None

def verify_email_smtp(email):
    domain = email.split('@')[-1]
    mx = get_mx_record(domain)
    if not mx:
        return False, "No MX records"
        
    try:
        server = smtplib.SMTP(mx, timeout=8)
        server.set_debuglevel(0)
        
        server.helo(server.local_hostname or socket.gethostname())
        server.mail('edohoeketio@gmail.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True, "Valid"
        elif code >= 500:
            return False, f"Hard Bounce ({code})"
        else:
            return False, f"Unknown Code ({code})"
            
    except Exception as e:
        return False, f"Exception: {e}"

def worker(domain):
    # Try a few prefixes per domain until one hits
    random.shuffle(PREFIXES)
    for prefix in PREFIXES[:5]: # Try 5 names per domain to keep it fast
        email = f"{prefix}@{domain}"
        is_valid, reason = verify_email_smtp(email)
        if is_valid:
            # Check for catch-all: test a fake email. If fake is valid, domain is a catch-all, reject it.
            fake_email = f"xjqkz12345nonce@{domain}"
            fake_valid, _ = verify_email_smtp(fake_email)
            if fake_valid:
                return None # Catch-all domain, useless for verification
            return email
    return None

def run_autonomous_engine():
    # Load existing if any
    safe_emails = set()
    if os.path.exists(SAFE_CSV_PATH):
        with open(SAFE_CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                safe_emails.add(row["Email"])
                
    print(f"Starting with {len(safe_emails)} already verified leads.")
    if len(safe_emails) >= TARGET_LEADS:
        print("Target already achieved!")
        return

    # Ensure file has headers
    if not os.path.exists(SAFE_CSV_PATH) or os.path.getsize(SAFE_CSV_PATH) == 0:
        with open(SAFE_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Email"])
            writer.writeheader()

    print(f"🚀 Launching Infinite Autonomous Verification Engine. Target: {TARGET_LEADS} leads.")
    
    with open(SAFE_CSV_PATH, mode='a', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Email"])
        
        while len(safe_emails) < TARGET_LEADS:
            # Generate a fresh batch of 500 potential domains
            current_domains = generate_domain_batch(500)
            
            with ThreadPoolExecutor(max_workers=30) as executor:
                futures = {executor.submit(worker, d): d for d in current_domains}
                for future in as_completed(futures):
                    result_email = future.result()
                    if result_email and result_email not in safe_emails:
                        print(f"💎 Verified Lead Found: {result_email} ({len(safe_emails) + 1}/{TARGET_LEADS})")
                        safe_emails.add(result_email)
                        writer.writerow({"Email": result_email})
                        outfile.flush()
                        
                        if len(safe_emails) >= TARGET_LEADS:
                            break

    print(f"\n✅ Autonomous engine cleanly shut down. Total verified leads secured: {len(safe_emails)}")

if __name__ == "__main__":
    run_autonomous_engine()
