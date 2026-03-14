import csv
import os
import time
import requests

# Load from .env securely
env_dict = {}
try:
    with open('/home/sk/Downloads/Style DNA/.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env_dict[k] = v.strip('"\'')
except FileNotFoundError:
    pass

APOLLO_API_KEY = os.environ.get("APOLLO_API_KEY", env_dict.get("APOLLO_API_KEY"))

CSV_PATH = "/home/sk/Downloads/Style DNA/execution/leads.csv"
ENRICHED_CSV_PATH = "/home/sk/Downloads/Style DNA/execution/leads_enriched.csv"

def enrich_leads():
    if not APOLLO_API_KEY:
        print("❌ Error: APOLLO_API_KEY environment variable is missing.")
        return

    print("🚀 Starting Apollo.io Lead Enrichment Process...")
    
    enriched_rows = []
    success_count = 0
    
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        total = len(reader)
        
        for idx, row in enumerate(reader):
            # The original setup placed the company name in the subject. We will parse it out, 
            # or just use the domain from the programmatic email.
            original_email = row.get("Email", "")
            if "@" not in original_email:
                enriched_rows.append(row)
                continue
                
            # Parse the actual startup name from the subject line we generated
            startup_name = row.get("Subject", "").split("Product Engineer for ")[-1].split(" (Remote")[0]
            
            print(f"[{idx+1}/{total}] Searching for engineering leader at {startup_name}...")
            
            url = "https://api.apollo.io/v1/contacts/search"
            
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "X-Api-Key": APOLLO_API_KEY
            }
            
            # We are looking for someone with a CTO, VP Engineering, or Founder title at this specific company
            data = {
                "q_organization_name": startup_name,
                "person_titles": ["CTO", "Chief Technology Officer", "VP Engineering", "Vice President of Engineering", "Head of Engineering", "Founder", "Co-Founder"],
                "page": 1,
                "per_page": 1 # Just get the top match
            }
            
            try:
                response = requests.post(url, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    contacts = result.get('contacts', [])
                    
                    if contacts and len(contacts) > 0:
                        contact = contacts[0]
                        verified_email = contact.get('email')
                        first_name = contact.get('first_name', 'there')
                        
                        if verified_email:
                            print(f"  ✅ Found: {first_name} <{verified_email}>")
                            
                            # Update the row with the verified data
                            # We will also update the body to use their actual first name
                            row["Email"] = verified_email
                            
                            # Replace the programmatic "Hi Alex," with the real name
                            old_greeting = row["Body"].split(',\\n\\n')[0]
                            row["Body"] = row["Body"].replace(old_greeting, f"Hi {first_name}")
                            
                            success_count += 1
                        else:
                            print(f"  ⚠️ Match found but email is hidden/premium.")
                    else:
                        print(f"  ❓ No exact engineering leader match found on free tier.")
                
                elif response.status_code == 429:
                    print("  🛑 Rate limited by Apollo! Waiting 60 seconds...")
                    time.sleep(60)
                    # We'll just append the original row for this one and continue
                else:
                    print(f"  ❌ API Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Request Failed: {e}")
                
            enriched_rows.append(row)
            
            # Apollo free tier strict rate limit (usually ~50-100 per minute)
            # We sleep for 1.5 seconds to be safe
            time.sleep(1.5)
            
    # Write the enriched data to a new file so we don't destroy the original
    with open(ENRICHED_CSV_PATH, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Email", "Subject", "Body"])
        writer.writeheader()
        for enriched_row in enriched_rows:
            writer.writerow(enriched_row)
            
    print(f"\\n🎉 Enrichment complete. Successfully found {success_count} verified emails.")
    print(f"Saved to: {ENRICHED_CSV_PATH}")

if __name__ == "__main__":
    enrich_leads()
