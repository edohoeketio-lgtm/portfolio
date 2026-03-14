import subprocess
import smtplib
import socket
import time
import csv

TARGETS = [
    # Yoco
    ("Lungisa", "Matshoba", "yoco.com"),
    ("Bradley", "Wattrus", "yoco.com"),
    ("Carl", "Wazen", "yoco.com"),
    ("Katlego", "Maphai", "yoco.com"),
    
    # Stitch
    ("Kiaan", "Pillay", "stitch.money"),
    ("Priyen", "Pillay", "stitch.money"),
    ("Junaid", "Dadan", "stitch.money"),
    
    # Zappi
    ("Aaron", "Kechley", "zappi.io"),
    ("Steve", "Phillips", "zappi.io"),
    
    # NjiaPay
    ("Jonatan", "Allback", "njiapay.com"),
    ("Roderick", "Simons", "njiapay.com")
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
        pass
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
        return False

def generate_permutations(first, last, domain):
    f = first.lower()
    l = last.lower()
    return [
        f"{f}@{domain}",             # first@
        f"{f}.{l}@{domain}",         # first.last@
        f"{f[0]}{l}@{domain}",       # flast@
        f"{f}{l[0]}@{domain}",       # firstl@
        f"{f}{l}@{domain}",          # firstlast@
        f"{f[0]}.{l}@{domain}",      # f.last@
        f"{l}@{domain}"              # last@
    ]

def is_catch_all(domain, mx_record):
    bogus = f"bdf192jfhd8axjdka2@{domain}"
    return verify_email(bogus, mx_record)

def find_sa_emails():
    print("🚀 Initiating rigorous Target-Lock SMTP Verification for South African executives...\n")
    
    found_leads = []
    
    for first, last, domain in TARGETS:
        print(f"🔍 Targeting: {first} {last} @ {domain}")
        mx = get_mx_record(domain)
        if not mx:
            print(f"  ❌ No MX record found for {domain}")
            continue
            
        print(f"  📡 MX Record Found: {mx}")
        
        if is_catch_all(domain, mx):
            print(f"  ⚠️ {domain} is a CATCH-ALL domain. Strict SMTP verification impossible. Defaulting to first.last and first.")
            found_leads.append((f"{first} {last}", f"{first.lower()}@{domain}", domain, "Unverified (Catch-All)"))
            found_leads.append((f"{first} {last}", f"{first.lower()}.{last.lower()}@{domain}", domain, "Unverified (Catch-All)"))
            continue
            
        perms = generate_permutations(first, last, domain)
        matched = False
        
        for email in perms:
            if verify_email(email, mx):
                print(f"  ✅ BOOM! Verified Address Found: {email}")
                found_leads.append((f"{first} {last}", email, domain, "Verified"))
                matched = True
                break
                
        if not matched:
            print(f"  ❌ Exhausted standard permutations, mail server rejected all.")
            
        print("-" * 50)
        time.sleep(1) # Politeness delay
        
    print("\n📝 RESULTS:\n")
    output_file = '/home/sk/Downloads/Style DNA/execution/sa_executive_targets.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Email', 'Domain', 'Status'])
        for name, email, domain, status in found_leads:
            print(f"[{status}] {name} -> {email}")
            writer.writerow([name, email, domain, status])
    
    print(f"\nSaved to: {output_file}")

if __name__ == "__main__":
    find_sa_emails()
