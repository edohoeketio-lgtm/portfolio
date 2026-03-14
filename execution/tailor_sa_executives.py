import csv

executives = [
    {
        "Name": "Kiaan Pillay",
        "Email": "kiaan@stitch.money",
        "Domain": "stitch.money",
        "Subject": "Scaling API infrastructure and frictionless payments at Stitch",
        "Body": """Hi Kiaan,<br><br>

I'm a Senior Product Engineer with a specialized background in high-velocity Fintech and Web3 data pipelines. I know exactly how hard it is to abstract away fragmented banking infrastructure, and the API surface Stitch has built is incredible.<br><br>

I previously engineered frontend systems for Aave, taking incredibly dense transaction data and rendering it instantly for the end user. I just migrated my own architecture (<a href="https://folio-jet-mu.vercel.app/">folio-jet-mu.vercel.app</a>) to strict Playwright E2E testing to guarantee flawless delivery. I'd love to bring this level of scaling rigor to Stitch.<br><br>

Are you currently hiring any remote engineers in the WAT timezone?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Priyen Pillay",
        "Email": "priyen@stitch.money",
        "Domain": "stitch.money",
        "Subject": "Engineering frictionless checkout and scaling Stitch's API",
        "Body": """Hi Priyen,<br><br>

I'm a Senior Product Engineer obsessed with frontend architecture and deploy velocity in the FinTech space. Constructing a flawless, abstracted API layer for payments in Africa is a massive technical challenge, and what Stitch is building is best-in-class.<br><br>

I have deep experience translating complex transaction graphs into seamless UI. At Aave, I engineered the consumer-facing dashboards handling decentralized liquidity at scale. More recently, I integrated full E2E Playwright coverage directly into my personal React infrastructure to prevent deployment regressions.<br><br>

Do you have any remote engineering roles open in the WAT timezone? I've attached my resume.<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Junaid Dadan",
        "Email": "junaid@stitch.money",
        "Domain": "stitch.money",
        "Subject": "Scaling API infrastructure and frictionless payments at Stitch",
        "Body": """Hi Junaid,<br><br>

I'm a Senior Product Engineer with a specialized background in high-velocity Fintech and Web3 data pipelines. I know exactly how hard it is to abstract away fragmented banking infrastructure, and the API surface Stitch has built is incredible.<br><br>

I previously engineered frontend systems for Aave, taking incredibly dense transaction data and rendering it instantly for the end user. I just migrated my own architecture (<a href="https://folio-jet-mu.vercel.app/">folio-jet-mu.vercel.app</a>) to strict Playwright E2E testing to guarantee flawless delivery. I'd love to bring this level of scaling rigor to Stitch.<br><br>

Are you currently hiring any remote engineers in the WAT timezone?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Lungisa Matshoba",
        "Email": "lungisa@yoco.com",
        "Domain": "yoco.com",
        "Subject": "Bridging UX and complex payment telemetry at Yoco",
        "Body": """Hi Lungisa,<br><br>

I'm a Senior Product Engineer and UI Architect. Yoco is strictly the gold standard for empowering African merchants via frictionless hardware/software syncing. Building extremely fast, state-driven UIs for transaction processing is exactly what I hyper-focus on.<br><br>

I recently built a custom Web Audio engine and brutalist UI architecture from scratch (<a href="https://folio-jet-mu.vercel.app/">folio-jet-mu.vercel.app</a>), fully instrumented with PostHog analytics and Playwright E2E testing because I refuse to ship unmeasured code to production. I also bring deep DeFi experience from architecting frontend workflows at Aave.<br><br>

I'd love to bring my high-velocity engineering background to the Yoco team. Are you hiring remote engineers right now?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Bradley Wattrus",
        "Email": "bradley@yoco.com",
        "Domain": "yoco.com",
        "Subject": "Scaling Yoco's platform via telemetry and data-driven UX",
        "Body": """Hi Bradley,<br><br>

I'm a Senior Product Engineer with a specific focus on bringing data-driven velocity to deployment cycles. What Yoco has done for financial inclusion and merchant tooling in Africa is incredible. I know scaling that type of volume requires highly predictable infrastructure.<br><br>

I enforce strict PostHog telemetry and comprehensive Playwright testing within my own React architectures to close the feedback loop on every single feature. I also previously built secure, frictionless frontend flows for decentralized finance protocols at Aave.<br><br>

I'd love to apply this level of engineering rigor to Yoco's product suite. Do you have any remote slots open for a WAT-based engineer?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Carl Wazen",
        "Email": "carl@yoco.com",
        "Domain": "yoco.com",
        "Subject": "Accelerating Yoco's go-to-market with rapid feature shipping",
        "Body": """Hi Carl,<br><br>

I'm a Senior Product Engineer obsessed with shrinking the feedback loop between a product idea and a shipped feature. As Yoco scales its merchant offerings, accelerating feature delivery without breaking the transactional UI is critical.<br><br>

I recently rebuilt my own React architecture heavily instrumented by Playwright testing and PostHog analytics. I also bring deep DeFi scale experience from engineering frontend features at Aave. Finding the balance between "building fast" and "building safe" is exactly what I specialize in.<br><br>

Are you currently hiring any remote engineers to scale Yoco's go-to-market efforts? My CV is attached.<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Katlego Maphai",
        "Email": "katlego@yoco.com",
        "Domain": "yoco.com",
        "Subject": "Scaling Yoco's engineering speed and product strategy",
        "Body": """Hi Katlego,<br><br>

I'm a Senior Product Engineer who thrives on owning product architecture end-to-end. Scaling Yoco from an initial piece of POS hardware to a massive financial ecosystem requires an engineering culture that obsesses over user telemetry—which is precisely how I operate.<br><br>

I enforce strict PostHog telemetry and comprehensive E2E testing within my React architectures to prove every feature drives value. My previous fintech background includes engineering the frontend dashboards for Aave's decentralized liquidity protocol.<br><br>

I'd love to discuss how I can help bring that 0-to-1 build speed into Yoco's strategic initiatives. Let me know if you are open to a conversation.<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Steve Phillips",
        "Email": "steve.phillips@zappistore.com",
        "Domain": "zappi.io",
        "Subject": "Bringing PostHog telemetry and rapid iteration to Zappi",
        "Body": """Hi Steve,<br><br>

I'm a Senior Product Engineer and UI Architect. Taking dense analytical capabilities and translating them into frictionless, automated insights is incredibly difficult, which is why Zappi's market research tooling stands out to me.<br><br>

I don't just write code; I instrument every interaction using tools like PostHog telemetry to close the feedback loop, and I rely purely on E2E Playwright coverage to avoid regressions. I've scaled complex data-heavy React dashboards before during my time in the DeFi space.<br><br>

I'd love to help build and iterate on those internal analytics engines at Zappi. Are you hiring any remote engineers right now?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Aaron Kechley",
        "Email": "aaron.kechley@zappistore.com",
        "Domain": "zappi.io",
        "Subject": "Engineering speed and data-driven product telemetry at Zappi",
        "Body": """Hi Aaron,<br><br>

I'm a Senior Product Engineer obsessed with shrinking the time between asking a data question and shipping a feature answer. What Zappi does for fast, automated consumer insights perfectly aligns with how I build software: entirely telemetry and testing-driven.<br><br>

I recently built a custom modular architecture fully reinforced with E2E Playwright testing and PostHog funnels, because shipping unmeasured code is a liability. I also have deep experience rendering massive, dense datasets in real time from my work building DeFi dashboards at Aave.<br><br>

Are you currently hiring any remote engineers in the EMEA/WAT time zone? My CV is attached.<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Jonatan Allback",
        "Email": "jonatan@njiapay.com",
        "Domain": "njiapay.com",
        "Subject": "Architecting frictionless payment orchestration pipelines at NjiaPay",
        "Body": """Hi Jonatan,<br><br>

I'm a Senior Product Engineer who specializes in building fluid software over extremely complex transaction protocols. The way NjiaPay abstracts cross-border payments in Africa to make it feel like a seamless Web2 API checkout is highly impressive.<br><br>

I spent a year at Aave building precise UI wrappers around extremely volatile DeFi smart contracts, meaning my focus is making money movement feel utterly effortless for the consumer. I enforce my code quality with strict Playwright E2E testing to guarantee transactions never drop.<br><br>

I'd love to bring my transaction-graph and React expertise to NjiaPay. Are you hiring remote engineers right now?<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    },
    {
        "Name": "Roderick Simons",
        "Email": "roderick@njiapay.com",
        "Domain": "njiapay.com",
        "Subject": "Scaling payment infrastructure and UI speed at NjiaPay",
        "Body": """Hi Roderick,<br><br>

I'm a Senior Product Engineer obsessed with frontend architecture and deploy velocity. Solving cross-border payment routing in Africa demands incredibly resilient infrastructure, and what NjiaPay is building requires zero-error transaction UIs.<br><br>

I previously worked at Aave, handling dense Web3 liquidity graphs and rendering them into seamless consumer dashboards. To guarantee performance, I use strict Playwright E2E coverage and PostHog telemetry out of the box so that regressions simply do not happen on my watch.<br><br>

I'd love to bring my UX architecture and FinTech background to the NjiaPay engineering team. Let me know if you are hiring remote engineers in the WAT timezone!<br><br>

Best,<br>
Maurice Edohoeket<br>
<a href="https://github.com/edohoeketio-lgtm">GitHub</a> | <a href="https://folio-jet-mu.vercel.app/">Portfolio</a>"""
    }
]

def write_exec_csv():
    output_csv = "/home/sk/Downloads/Style DNA/execution/sa_executive_leads_tailored.csv"
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
            
    print(f"✅ Executed. Carefully tailored {len(executives)} surgical executive HTML emails mapped to their exact infrastructure.")
    print(f"Saved to: {output_csv}")

if __name__ == "__main__":
    write_exec_csv()
