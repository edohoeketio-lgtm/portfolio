import subprocess
import smtplib
import socket
import time
import re
import csv

TARGETS = [
    # (First, Last, Domain)
    ("Malte", "Ubl", "vercel.com"),
    ("Lindsey", "Simon", "vercel.com"),
    ("Ant", "Wilson", "supabase.com"),
    ("Paul", "Copplestone", "supabase.com"),
    ("Tuomas", "Artman", "linear.app"),
    ("Nan", "Yu", "linear.app"),
    ("Petr", "Nikolaev", "raycast.com"),
    ("Philip", "Beevers", "attio.com"),
    ("Alexander", "Christie", "attio.com"),
    ("Thomas", "Mary", "maze.co"),
    ("David", "Rodrigues", "argent.xyz")
]

def get_mx_record(domain):
    try:
        result = subprocess.run(
            ['dig', '+short', 'MX', domain],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            records = []
            for line in lines:
                parts = line.split()
                if len(parts) == 2:
                    records.append((int(parts[0]), parts[1].strip('.')))
            if records:
                records.sort(key=lambda x: x[0])
                return records[0][1]
    except Exception as e:
        print(f"Error getting MX for {domain}: {e}")
    return None

def verify_email(email, mx_record):
    domain = email.split('@')[1]
    try:
        server = smtplib.SMTP(timeout=5)
        server.set_debuglevel(0)
        
        server.connect(mx_record, 25)
        server.ehlo_or_helo_if_needed()
        
        # Use a realistic sender
        server.mail('hello@google.com')
        
        # Check recipient
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return True
        return False
        
    except (socket.timeout, smtplib.SMTPServerDisconnected, Exception):
        # Only return True on a strict 250 OK
        return False

def generate_permutations(first, last, domain):
    f = first.lower()
    l = last.lower()
    return [
        f"{f}@{domain}",             # malte@vercel.com
        f"{f}.{l}@{domain}",         # malte.ubl@vercel.com
        f"{f[0]}{l}@{domain}",       # mubl@vercel.com
        f"{f}{l[0]}@{domain}",       # malteu@vercel.com
        f"{f}{l}@{domain}",          # malteubl@vercel.com
        f"{f[0]}.{l}@{domain}",      # m.ubl@vercel.com
        f"{l}@{domain}"              # ubl@vercel.com
    ]

def is_catch_all(domain, mx_record):
    # Test a completely bogus email to see if the server just accepts everything
    bogus = f"bldkhf192jd81jdka2@{domain}"
    return verify_email(bogus, mx_record)

def find_executive_emails():
    print("🚀 Initiating rigorous Target-Lock SMTP Verification for specific executives...\n")
    
    found_leads = []
    
    for first, last, domain in TARGETS:
        print(f"🔍 Targeting: {first} {last} @ {domain}")
        mx = get_mx_record(domain)
        if not mx:
            print(f"  ❌ No MX record found for {domain}")
            continue
            
        print(f"  📡 MX Record Found: {mx}")
        
        # Check for catch-all (which makes SMTP verification impossible)
        if is_catch_all(domain, mx):
            print(f"  ⚠️ {domain} is a CATCH-ALL domain. Strict SMTP verification impossible. Defaulting to first.last and first.")
            # For catch-alls, we just add the most likely permutations and flag them
            found_leads.append((f"{first} {last}", f"{first.lower()}@{domain}", domain, "Unverified (Catch-All)"))
            found_leads.append((f"{first} {last}", f"{first.lower()}.{last.lower()}@{domain}", domain, "Unverified (Catch-All)"))
            continue
            
        # Try permutations
        perms = generate_permutations(first, last, domain)
        matched = False
        
        for email in perms:
            # print(f"    Ping: {email}...")
            if verify_email(email, mx):
                print(f"  ✅ BOOM! Verified Address Found: {email}")
                found_leads.append((f"{first} {last}", email, domain, "Verified"))
                matched = True
                break # Move to next target once found
                
        if not matched:
            print(f"  ❌ Exhausted standard permutations, mail server rejected all.")
            
        print("-" * 50)
        time.sleep(1) # Politeness delay
        
    print("\n📝 RESULTS:\n")
    with open('/home/sk/Downloads/Style DNA/execution/executive_targets.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Domain', 'Status'])
        for name, email, domain, status in found_leads:
            print(f"[{status}] {name} -> {email}")
            writer.writerow([name, email, domain, status])
    
    print("\nSaved to: execution/executive_targets.csv")

if __name__ == "__main__":
    find_executive_emails()
