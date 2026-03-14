import csv
import smtplib
import subprocess
import socket
import time

CSV_PATH = "/home/sk/Downloads/Style DNA/execution/leads.csv"
SAFE_CSV_PATH = "/home/sk/Downloads/Style DNA/execution/leads_safe.csv"

def get_mx_record(domain):
    try:
        result = subprocess.check_output(['dig', '+short', 'MX', domain], text=True)
        records = result.strip().split('\n')
        if not records or not records[0]:
            return None
        records.sort(key=lambda x: int(x.split()[0]) if len(x.split()) > 1 else float('inf'))
        # Return the top priority MX server
        return records[0].split()[1].rstrip('.')
    except Exception:
        return None

def verify_email_smtp(email):
    domain = email.split('@')[-1]
    mx = get_mx_record(domain)
    if not mx:
        return False, "No MX records found"
        
    try:
        server = smtplib.SMTP(mx, timeout=8)
        server.set_debuglevel(0)
        
        server.helo(server.local_hostname or socket.gethostname())
        server.mail('edohoeketio@gmail.com')
        code, message = server.rcpt(email)
        server.quit()

        # 250 means OK (the server accepts it)
        if code == 250:
            return True, "Valid"
        # 550, 554, etc. means Hard Bounce or Relay Denied
        elif code >= 500:
            return False, f"Hard Bounce ({code})"
        else:
            return False, f"Unknown Code ({code})"
            
    except smtplib.SMTPServerDisconnected:
        return False, "SMTP Disconnected"
    except smtplib.SMTPConnectError:
        return False, "SMTP Connect Error"
    except socket.timeout:
        # Some aggressive corporate firewalls drop packets. We skip to be safe.
        return False, "Timeout"
    except Exception as e:
        return False, f"Exception: {e}"

def clean_leads_database():
    safe_rows = []
    total = 0
    bounced = 0
    
    print("🚀 Initiating rigorous Local SMTP Verification on all 150 leads...")
    
    # Read the original programmatic guesses
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        total = len(reader)
        
        for idx, row in enumerate(reader):
            email = row.get("Email")
            if not email or "@" not in email:
                continue
                
            print(f"[{idx+1}/{total}] Verifying {email}...")
            
            is_valid, reason = verify_email_smtp(email)
            
            if is_valid:
                print(f"  ✅ Acceptable: Mail server confirms route")
                safe_rows.append(row)
            else:
                print(f"  ❌ Rejected: {reason} (Protected sender score)")
                bounced += 1
            
            # Tiny sleep to avoid abusing public name servers
            time.sleep(0.5)

    with open(SAFE_CSV_PATH, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Email", "Subject", "Body"])
        writer.writeheader()
        for safe_row in safe_rows:
            writer.writerow(safe_row)
            
    print(f"\n🛡️ Verification Complete.")
    print(f"Total leads: {total}")
    print(f"Bounced/Rejected: {bounced}")
    print(f"Verified & Safe: {len(safe_rows)}")
    print(f"Saved highly protected list to: {SAFE_CSV_PATH}")

if __name__ == "__main__":
    clean_leads_database()
