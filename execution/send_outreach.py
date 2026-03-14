import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import csv
import os
import time

env_dict = {}
try:
    with open('/home/sk/Downloads/Style DNA/.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env_dict[k] = v.strip('"\'')
except FileNotFoundError:
    pass

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", env_dict.get("EMAIL_ADDRESS"))
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", env_dict.get("EMAIL_APP_PASSWORD"))

def send_batch_emails(csv_file_path, resume_path=None, limit=150):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        print("❌ Error: EMAIL_ADDRESS and EMAIL_APP_PASSWORD environment variables must be set.")
        return

    print("🚀 Initializing SMTP connection to Gmail...")
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        print("✅ Successfully authenticated with Gmail.")
    except Exception as e:
        print(f"❌ Failed to authenticate: {e}")
        return

    success_count = 0
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if success_count >= limit:
                print(f"🛑 Reached safe batch limit of {limit} emails. Stopping to protect sender reputation.")
                break
                
            target_email = row.get("Email")
            subject = row.get("Subject")
            body = row.get("Body")
            
            if not target_email or not subject or not body:
                print(f"⚠️ Skipping invalid row: {row}")
                continue

            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = target_email
            msg['Subject'] = subject

            # Attach the tailored body
            msg.attach(MIMEText(body, 'html'))

            # Attach Resume if provided
            if resume_path and os.path.exists(resume_path):
                try:
                    with open(resume_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(resume_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(resume_path)}"'
                        msg.attach(part)
                except Exception as e:
                    print(f"⚠️ Could not attach resume for {target_email}: {e}")

            # Send Email
            try:
                print(f"📧 Sending to {target_email}...")
                server.send_message(msg)
                success_count += 1
                # Sleep to prevent Gmail rate-limiting (Gmail limits to ~100-150 rolling per day for personal, 500 for workspace, but burst sending can trigger spam filters)
                time.sleep(3) 
            except Exception as e:
                print(f"❌ Failed to send to {target_email}: {e}")

    server.quit()
    print(f"\n🎉 Batch complete. Successfully sent {success_count} emails.")

if __name__ == "__main__":
    import os
    
    # Absolute paths
    CSV_PATH = "/home/sk/Downloads/Style DNA/execution/sa_executive_leads_tailored.csv"
    PDF_PATH = "/home/sk/Downloads/Style DNA/Maurice_Edohoeket_Senior_Product_Engineer_CV.pdf"
    
    print(f"Loading SMTP-verified safe leads from: {CSV_PATH}")
    print(f"Attaching PDF: {PDF_PATH}")
    
    # We remove the hardcoded 5 limit to blast the whole verified list
    confirm = input("Are you absolutely sure you want to blast these SMTP-verified emails? (Type 'YES' to confirm): ")
    if confirm == "YES":
        send_batch_emails(CSV_PATH, resume_path=PDF_PATH, limit=150)
    else:
        print("Aborting.")
