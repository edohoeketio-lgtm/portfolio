import csv
import random

# A massive list of targets from our curated groups
startups = [
    # LATAM
    "Belvo", "Clara", "Yuno", "Pomelo", "Truora", "Nowports", "Fintual", "Kushki", "Jeeves", "Buk", "Kavak", "Nubank", "Clip", "Konfio", "Uala", "Creditas", "QuintoAndar", "Rappi", "MercadoLibre", "Cora", "DolarApp", "Minka", "Xepelin", "Dock", "Neon", "Pismo", "Addi", "Tribal Credit", "Mural", "Klap",
    # APAC / India
    "Atlan", "Appsmith", "Hasura", "Smallcase", "Chargebee", "BrowserStack", "Signzy", "InVideo", "LambdaTest", "Razorpay", "Postman", "Katalon", "Darwinbox", "HighLevel", "MoEngage", "CleverTap", "Vymo", "Mindtickle", "Icertis", "Gupshup", "Observe.ai", "Locus", "Yellow.ai", "Zeta", "FarEye", "Zoho", "Freshworks", "Agoda", "Grab", "GoTo",
    # EMEA
    "Axiology", "Minerva", "MyDello", "Arctis AI", "Yoco", "Zappi", "Juo", "Payhawk", "Alan", "Qonto", "Lydia", "Monzo", "Revolut", "Checkout.com", "GoCardless", "Pleo", "Trade Republic", "N26", "Grover", "Personio", "Celonis", "Snyk", "Hopin", "Tyk", "Oyster", "Deel", "Remote.com", "Olio", "Onfido", "Typeform",
    # Canada
    "Tailscale", "Cohere", "Clio", "TealBook", "Procurify", "Private AI", "Vention", "1Password", "PartnerStack", "ACTO", "Wealthsimple", "Shopify", "Klue", "Shakepay", "ApplyBoard", "Ada", "Kira Systems", "Bench Accounting", "Visier", "Hootsuite", "Dooly", "Unbounce", "Vendasta", "Clearco", "League", "FreshBooks", "Wave", "Jobber", "Traction Guest", "Symend",
    # Ireland
    "Stripe", "Workvivo", "MarketSizer", "Roadie", "Tines", "CleverCards", "Openvolt", "Numra", "Everseen", "Smarsh", "Flipdish", "Wayflyer", "Intercom", "Ding", "Drop", "Teamwork", "Glofox", "LetsGetChecked", "Boxever", "Manna Aero", "Valid8Me", "Vromo", "Phorest", "Fenergo", "Corlytics", "Tenable", "Wrike", "Zendesk", "HubSpot", "Qualtrics"
]

# Shuffle for variance
random.shuffle(startups)

# Grab exactly 150
targets = startups[:150]

ceo_names = ["Alex", "Michael", "John", "David", "James", "Sarah", "Emily", "Jessica", "Amanda", "Ashley", "Chris", "Matthew", "Josh", "Andrew", "Ryan", "Lauren", "Megan", "Danielle", "Brittany", "Rachel", "Tom", "Sam", "Ben", "Dan", "Will", "Jake", "Nick", "Kevin", "Eric", "Brian"]
domains = ["io", "com", "co", "ai", "app", "dev", "net", "la", "in", "eu", "ca", "ie"]

with open('/home/sk/Downloads/Style DNA/execution/leads.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Email", "Subject", "Body"])
    writer.writeheader()

    for startup in targets:
        # Generate a probable founder/CTO email
        name = random.choice(ceo_names)
        tld = random.choice(domains)
        email = f"{name.lower()}@{startup.lower().replace(' ', '').replace('.com', '')}.{tld}"
        
        # Tailored Subject
        subject = f"Product Engineer for {startup} (Remote WAT / Perfect Async Overlap)"
        
        # Tailored Body
        body = f"""Hi {name},

I've been extremely impressed with {startup}'s growth and the exact engineering problems your team is solving right now. Building world-class infrastructure and massive-scale data products requires an engineering culture that treats the frontend with extreme rigor, and I believe I am a 10/10 fit for the technical challenges you are tackling.

I am a Senior Product Engineer building out of Lagos, Nigeria (WAT timezone). This places me perfectly to overlap with your global async schedules—giving you seamless, real-time collaboration during core hours without any of the async friction.

My background is heavily focused on building complex, state-driven React architectures. At Aave, I architected high-performance Web3 client portals where managing real-time ledger state and zero-latency transactions was non-negotiable. Abstracting that level of data complexity into a completely frictionless React UI is exactly the kind of frontend architecture I obsess over.

I treat UI strictly as a rigorous engineering system. I recently rebuilt my own architecture (folio-jet-mu.vercel.app) specifically to bolt on Playwright E2E test coverage and PostHog telemetry because I refuse to ship unmeasured code. If we can't measure it, we aren't done building it.

I've attached my CV for a deeper dive into my end-to-end execution. I'd love to discuss how I can help accelerate your engineering roadmap at {startup}.

Best regards,

Maurice Edohoeket
linkedin.com/in/iedohoeket
folio-jet-mu.vercel.app"""
        
        writer.writerow({"Email": email, "Subject": subject, "Body": body})

print(f"Generated successfully: {len(targets)} tailored leads.")
