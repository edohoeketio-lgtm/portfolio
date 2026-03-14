import smtplib
import subprocess
import time
import socket

def get_mx_record(domain):
    try:
        # Using dig to bypass the need for external dns packages
        result = subprocess.check_output(['dig', '+short', 'MX', domain], text=True)
        records = result.strip().split('\n')
        if not records or not records[0]:
            return None
        # Example output line: "10 mail.example.com."
        # Take the top priority record
        records.sort(key=lambda x: int(x.split()[0]) if x else float('inf'))
        mx = records[0].split()[1]
        return mx.rstrip('.')
    except Exception as e:
        print(f"Failed to get MX for {domain}: {e}")
        return None

def verify_email_smtp(email):
    domain = email.split('@')[1]
    mx = get_mx_record(domain)
    if not mx:
        return False, "No MX"
        
    try:
        # Establish connection
        server = smtplib.SMTP(mx, timeout=5)
        server.set_debuglevel(0)
        
        # SMTP Conversation
        server.helo(server.local_hostname or socket.gethostname())
        server.mail('edohoeketio@gmail.com')
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return True, "Valid"
        elif code == 550:
            return False, "Hard Bounce"
        else:
            return False, f"Unknown ({code})"
            
    except smtplib.SMTPServerDisconnected:
        return False, "Disconnected"
    except smtplib.SMTPConnectError:
        return False, "Connection Error"
    except socket.timeout:
        return False, "Timeout"
    except Exception as e:
        return False, f"Exception: {e}"

print("Testing known bad email:")
print(verify_email_smtp("danielle@juo.la"))

print("\nTesting probable catch-all:")
print(verify_email_smtp("alex@stripe.com"))
