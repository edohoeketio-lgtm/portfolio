import csv

def parse_name(email_prefix):
    roles = ['cto', 'engineering', 'founders', 'ceo', 'tech', 'careers', 'jobs', 'hello']
    if email_prefix.lower() in roles:
        return email_prefix.capitalize() + " (Department/Role)"
    return email_prefix.capitalize()

def analyze_leads():
    try:
        with open("/home/sk/Downloads/Style DNA/verified_52_leads.md", "r") as f:
            raw_lines = f.readlines()
    except FileNotFoundError:
        print("verified_52_leads.md not found.")
        return

    leads = [line.strip().replace("- ", "") for line in raw_lines if "@" in line]

    # Heuristics for bucketing
    # Big non-target domains (freemail, edu, megacorps, generic portals)
    dud_domains = {
        'qq.com', 'gmail.com', 'apple.com', 'tiktok.com', 'yandex.com', 'ebay.com', 
        'android.com', 'msn.com', 'jhu.edu', 'wikimedia.org', 'wikipedia.org', 
        'naver.com', 'kakao.com', 'timeweb.ru', 'time.com', 'huffingtonpost.com', 
        'economist.com'
    }

    # Established or huge tech, not strict "startup" but completely valid big logos
    silver_domains = {
        'medium.com', 'hubspot.com', 'trustpilot.com', 'tripadvisor.com', 'ovh.com', 
        'eventbrite.com', 'weebly.com', 'foursquare.com', 'udemy.com', 'soundcloud.com', 
        'vimeo.com', 'buzzfeed.com', 'imgur.com', 'deezer.com', 'domainmarket.com', 
        'namecheap.com', 'bluepay.com', 'apexsystems.com', 'apexsystems.net', 
        'mixcloud.com', 'pexels.com'
    }

    gold = []
    silver = []
    duds = []

    for email in leads:
        try:
            prefix, domain = email.split('@')
        except ValueError:
            continue
        
        name = parse_name(prefix)
        
        # Categorize
        if domain in dud_domains:
            duds.append((email, name, domain))
        elif domain in silver_domains:
            silver.append((email, name, domain))
        else:
            # Everything else is highly likely a dynamically generated small tech/startup
            # or a very specific B2B target domain from the dataset.
            gold.append((email, name, domain))

    output_path = "/home/sk/Downloads/Style DNA/Execution_52_Leads_Analysis.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Automated Email Lead Analysis (52 Verified Hits)\n\n")
        
        f.write("## 🥇 GOLD TIER (High-Value Startups & Tech Domains)\n")
        f.write("*These are likely the dynamically generated startup domains or strong hits that match our exact outreach profile. They are smaller, more likely to read cold outreach, and perfectly aligned for a Product Engineer.* \n\n")
        for email, name, domain in gold:
            f.write(f"- **{email}** | Target: `{name}` | Company: {domain.capitalize()}\n")
            
        f.write("\n## 🥈 SILVER TIER (Established / Big Tech & Media)\n")
        f.write("*These are established mid-to-large cap tech companies. Finding the decision maker via cold outreach to generic addresses might get lost, but they are fully valid targets.* \n\n")
        for email, name, domain in silver:
            f.write(f"- **{email}** | Target: `{name}` | Company: {domain.capitalize()}\n")

        f.write("\n## 🗑️ DUDS (Massive Corps, Freemail, Education, Publishers)\n")
        f.write("*These are mathematically verified to exist, but they are massive corporations (Apple), public free emails (Gmail), educational (JHU), or not relevant for startup-focused cold outreach.* \n\n")
        for email, name, domain in duds:
            f.write(f"- ~~{email}~~ | Target: `{name}` | Company: {domain.capitalize()}\n")
            
    print(f"✅ Categorized {len(gold)} Gold, {len(silver)} Silver, and {len(duds)} Duds into Execution_52_Leads_Analysis.md")

if __name__ == "__main__":
    analyze_leads()
