import csv

executives = [
    {
        "Name": "Malte Ubl",
        "Email": "malte@vercel.com",
        "Domain": "vercel.com",
        "Subject": "Bringing 0-to-1 DX and Playwright rigor to Vercel",
        "Body": """Hi Malte,

I'm a Senior Product Engineer obsessed with frontend architecture and deploy velocity. I host my entire personal infrastructure on Vercel because of how absolutely frictionless you make the developer experience. 

I recently overhauled my React architecture (folio-jet-mu.vercel.app) specifically to integrate strict Playwright E2E testing and PostHog telemetry in order to guarantee its performance. I'd love to bring this level of UI/UX rigor and 0-to-1 build speed to your engineering team. 

Are you currently hiring any remote engineers in the EMEA (WAT) time zone? I've attached my resume.

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    },
    {
        "Name": "Lindsey Simon",
        "Email": "lindsey@vercel.com",
        "Domain": "vercel.com",
        "Subject": "Engineering UI speed and Playwright coverage at Vercel",
        "Body": """Hi Lindsey,

I'm a Senior Product Engineer obsessed with frontend architecture and deploy velocity. I host my entire personal infrastructure on Vercel because of how absolutely frictionless the developer experience is. 

I recently overhauled my React architecture (folio-jet-mu.vercel.app) specifically to integrate strict Playwright E2E testing and PostHog telemetry to guarantee its performance. I know VP Engineering roles demand predictable, test-driven scale, and I'd love to bring this level of UI/UX rigor and 0-to-1 build speed to the Vercel team. 

Are you currently hiring any remote engineers in the EMEA (WAT) time zone? My resume is attached.

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    },
    {
        "Name": "Tuomas Artman",
        "Email": "tuomas@linear.app",
        "Domain": "linear.app",
        "Subject": "Architecting frictionless, state-driven UI at Linear",
        "Body": """Hi Tuomas,

I'm a Senior Product Engineer and UI Architect. Linear is strictly the gold standard for what a web application should feel like, and building extremely fast, frictionless state-driven UIs is exactly what I hyper-focus on. 

I recently built a custom Web Audio engine and brutalist UI architecture from scratch (folio-jet-mu.vercel.app), complete with strict Playwright E2E testing and telemetry pipelines because I refuse to ship unmeasured code. 

I'd love to bring my UX architecture background to the core Linear team. Let me know if you are hiring remote engineers in the UK/EU/WAT time zone!

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    },
    {
        "Name": "Nan Yu",
        "Email": "nan@linear.app",
        "Domain": "linear.app",
        "Subject": "Scaling Linear's product velocity & UX architecture",
        "Body": """Hi Nan,

I'm a Senior Product Engineer and UI Architect. Linear is essentially the gold standard for what a web application should feel like, and building extremely fast, frictionless state-driven UIs is exactly what I do. 

I recently built a custom Web Audio engine and brutalist UI architecture from scratch (folio-jet-mu.vercel.app), complete with strict E2E testing and telemetry pipelines. Since you head up Product, I know predictable shipping velocity and rigorous UX testing are paramount to your roadmap. 

I'd love to bring my UX architecture background to the Linear team. Are you currently hiring remote engineers in the UK/EU/WAT time zone?

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    },
    {
        "Name": "Thomas Mary",
        "Email": "thomas@maze.co",
        "Domain": "maze.co",
        "Subject": "Bridging hard engineering and UX research at Maze",
        "Body": """Hi Thomas,

I'm a Senior Product Engineer who thrives perfectly at the intersection of UX research and hard engineering. As someone who builds strict React architectures, I love the exact problem Maze solves for continuous product discovery. 

I literally just implemented PostHog telemetry on my own architecture (folio-jet-mu.vercel.app) to track user session funnels because I refuse to ship without closing the feedback loop. I'd love to help build those tools internally at Maze. 

Are you hiring any remote EU/WAT engineers right now? My resume is attached for your review.

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    },
    {
        "Name": "David Rodrigues",
        "Email": "david@argent.xyz",
        "Domain": "argent.xyz",
        "Subject": "Architecting frictionless Web3/DeFi UI at Argent",
        "Body": """Hi David,

I'm a Senior Product Engineer with a highly specific background in Web3/DeFi UI architecture (having previously designed interfaces for Aave). I know exactly how hard it is to make wallet infrastructure and smart contract execution feel like a seamless Web2 consumer experience, which is why I love what Argent is doing. 

I recently rebuilt my own React architecture (folio-jet-mu.vercel.app) with full Playwright E2E testing to guarantee flawless delivery. I'd love to bring my DeFi UI background to your engineering team.

Do you have any remote EMEA/WAT slots open right now? My CV is attached.

Best,
Maurice Edohoeket
edohoeketio@gmail.com
https://folio-jet-mu.vercel.app/"""
    }
]

def write_exec_csv():
    output_csv = "/home/sk/Downloads/Style DNA/execution/executive_leads_tailored.csv"
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Email", "Name", "Company", "Subject", "Body"])
        writer.writeheader()
        
        for exec_target in executives:
            writer.writerow({
                "Email": exec_target["Email"],
                "Name": exec_target["Name"],
                "Company": exec_target["Domain"],
                "Subject": exec_target["Subject"],
                "Body": exec_target["Body"]
            })
            
    print(f"✅ Executed. Carefully tailored {len(executives)} surgical executive emails mapped to their exact infrastructure.")
    print(f"Saved to: {output_csv}")

if __name__ == "__main__":
    write_exec_csv()
