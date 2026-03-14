import csv
import os

CSV_PATH = "/home/sk/Downloads/Style DNA/execution/leads_safe.csv"
OUT_PATH = "/home/sk/Downloads/Style DNA/execution/leads_tailored.csv"

# 10 completely uniquely written emails from top to bottom
CUSTOM_EMAILS = {
    "visier.app": {
        "Subject": "Senior Product Engineer for Visier's Workforce Analytics Edge",
        "Body": "Hi Chris,\n\nI've been closely following Visier's dominance in the HR and workforce analytics space. Abstracting millions of complex, highly-sensitive employee data points into a real-time, high-performance visualization layer requires an engineering culture that treats the frontend with extreme rigor. I believe I am a 10/10 fit for those exact challenges.\n\nAt Aave, I architected high-performance Web3 client portals where we had zero margin for error when rendering real-time decentralized ledger state. Translating deep, complex data models into an instantly intuitive UI is my strongest skillset.\n\nI build strict, test-driven systems out of Lagos (WAT timezone), which places me perfectly to overlap with your global async schedules—giving you seamless real-time collaboration during your core hours. I recently rebuilt my own architecture (folio-jet-mu.vercel.app) specifically to bolt on Playwright E2E coverage and PostHog telemetry because I absolutely refuse to ship unmeasured code in production.\n\nI've attached my CV for a deeper dive into my execution velocity. I'd love to discuss how my data visualization and state-heavy React background can accelerate Visier's product roadmap.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "shopify.in": {
        "Subject": "Building High-Conversion Storefront UI (WAT Overlap) // Senior React Eng",
        "Body": "Hi Rachel,\n\nShopify's engineering culture and the sheer scale of the storefront architecture is something I deeply admire. Building frictionless, zero-latency UI systems that process global e-commerce volumes means that every millisecond of render time translates directly to revenue. I thrive in that exact environment of extreme frontend optimization.\n\nI am currently a Senior Product Engineer building out of Lagos, Nigeria (WAT timezone). This places me perfectly to collaborate async, giving your teams continuous momentum while providing real-time overlap during core hours without the typical friction.\n\nMy background is heavily focused on building complex, state-driven React architectures. Most recently, I architected Web3 client portals at Aave, handling immense data complexity with zero-latency requirements. Furthermore, I treat UI strictly as a rigorous engineering system—instrumenting my own recent overhauls with PostHog telemetry and Playwright testing, because conversion and reliability cannot exist without hard metrics.\n\nI've attached my CV for a deeper dive into my end-to-end execution. I'd absolutely love the opportunity to bring my obsession for performant React to Shopify.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "partnerstack.com": {
        "Subject": "Architecting Scalable PRM Ecosystems // Product Engineer",
        "Body": "Hi Matthew,\n\nI've been extremely impressed by PartnerStack's ecosystem architecture. Building a seamless B2B partnership platform that handles complex revenue attribution, multi-tier payouts, and deep integration tracking requires an engineering culture that treats state management with extreme rigor. This is exactly the technical environment I excel in.\n\nHaving built highly concurrent platforms in Web3 (Aave), I am incredibly accustomed to managing strict client-side state where financial logic converges with the UI layer. Abstracting that level of data complexity into a completely frictionless React dashboard is what I obsess over daily.\n\nI am a Senior Product Engineer building out of Lagos, Nigeria (WAT timezone), which gives me excellent overlap with your team for real-time collaboration. I also strongly believe in defensive coding—most recently, I instrumented my own architecture with Playwright E2E and PostHog event tracking to ensure every deployment is measured and bulletproof.\n\nI've attached my CV for a deeper look at my technical execution. I'd love to discuss accelerating PartnerStack's engineering roadmap.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "tines.io": {
        "Subject": "Building Zero-Code Security UI at Tines // Product Engineer",
        "Body": "Hi Amanda,\n\nTines is building something brilliant in the SOAR space. Creating a zero-code automation platform that highly technical security engineers actually trust requires an incredibly robust, deeply complex frontend architecture. Building drag-and-drop workflows that mask immense backend complexity is exactly the kind of frontend hurdle I want to tackle.\n\nAt Aave, I architected high-performance client portals where managing real-time ledger state and zero-latency transactions was absolutely non-negotiable. I take exceptional pride in building secure, zero-trust engineering environments where the frontend is as rigorous as the backend systems it interacts with.\n\nI build out of Lagos, Nigeria (WAT timezone), giving me seamless overlap with your global schedules. I treat UI as a measurable system, famously refusing to ship unmeasured code—which is why I rely heavily on PostHog telemetry and Playwright E2E coverage across my stack.\n\nI've attached my CV for a deeper dive into my end-to-end execution. I'd love to learn more about Tines's frontend challenges and how I could help solve them.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "yuno.ca": {
        "Subject": "Global Payment Routing UI // Senior Product Engineer",
        "Body": "Hi David,\n\nI've been tracking Yuno's growth in the payment orchestration space closely. Abstracting the complexities of global payment routing and checkout flows into a unified, high-performance dashboard requires an engineering culture that treats the frontend with extreme accuracy and rigor. \n\nMy background matches this perfectly. At Aave, I architected high-performance Web3 client portals where we had zero margin for error rendering real-time decentralized ledger states and processing zero-latency financial transactions. Financial UI is an entirely different beast of frontend engineering, and it is where I thrive.\n\nI am a Senior Product Engineer working out of Lagos (WAT timezone), allowing for seamless, real-time collaboration during core async hours. Beyond writing clean React, I am obsessive about observability—I recently re-architected my own environments entirely around PostHog telemetry and absolute Playwright E2E coverage.\n\nI've attached my CV. I would jump at the chance to discuss how my deep experience with complex financial UI could benefit Yuno's payment platform.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "postman.in": {
        "Subject": "Evolving API Client State Management at Postman // Product Engineer",
        "Body": "Hi Tom,\n\nPostman is an essential, permanent fixture in my daily engineering workflow, and the sheer scale of the application architecture is something I deeply admire. Building a desktop-class, state-heavy web application that millions of developers rely on natively daily requires extreme frontend optimization. Evolving architectures at that scale is exactly the challenge I am looking for.\n\nMy specialty lies in building complex, state-driven React architectures. At Aave, I built high-performance Web3 client portals where managing real-time ledger state without latency spikes was non-negotiable. I am highly comfortable diving deep into complex state machines and keeping the UI thread incredibly fast.\n\nI am building out of Lagos, Nigeria (WAT timezone), which provides perfect overlap for global async schedules. I treat UI purely as a rigorous engineering system—instrumenting it with heavy PostHog analytics and Playwright test coverage because I believe developers are the toughest, most metric-driven users to build for.\n\nI've attached my CV for a deeper dive into my execution velocity. I'd love to discuss how I can help accelerate your engineering roadmap at Postman.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "pomelo.la": {
        "Subject": "Engineering Frictionless Cross-Border Credit UI at Pomelo",
        "Body": "Hi Emily,\n\nPomelo's approach to cross-border fintech infrastructure and remittances is incredibly inspiring work. Building seamless, high-trust user interfaces for global money movement requires an engineering culture that treats the frontend with extreme, uncompromising accuracy. \n\nI am a Senior Product Engineer with a heavy background in financial UI. At Aave, I architected high-performance Web3 client portals where managing real-time decentralized ledger state and ensuring zero-latency transactions was mandatory. Building secure, mathematically rigorous frontend systems in the fintech space is exactly where I naturally operate.\n\nI work from Lagos, Nigeria (WAT timezone), putting me in perfect alignment for core async overlap. I deeply value measurable engineering, having recently completely re-architected my own portfolio stack to strictly bolt on extreme Playwright E2E coverage and PostHog analytics—I refuse to deploy unmeasured UI code.\n\nI've attached my CV for a deeper dive into my execution. I'd love to discuss accelerating Pomelo's roadmap.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "klue.dev": {
        "Subject": "Synthesizing Competitive Intelligence UI // Product Engineer for Klue",
        "Body": "Hi Matthew,\n\nI've been incredibly impressed with Klue's platform for competitive enablement. Synthesizing massive, disparate streams of market intelligence into actionable, frictionless insights requires an incredibly robust and dynamic frontend architecture. I specialize in building exactly that kind of abstract data visualization.\n\nI am a Senior Product Engineer out of Lagos, Nigeria (WAT timezone)—providing excellent global async overlap. My prior work heavily involved building complex, state-driven React architectures. Most notably at Aave, I architected high-performance Web3 client portals where managing real-time ledger states was non-negotiable. I am exceptionally comfortable dealing with live, constantly shifting datasets on the UI layer.\n\nI also treat frontend development strictly as an observable system. I recently rebuilt my own architecture to enforce strict Playwright E2E tests and deep PostHog user telemetry, because I believe UI should be as rigorously measured as any backend API.\n\nI've attached my CV for a deeper dive into my technical background. I'd be absolutely thrilled to discuss how I can help evolve Klue's platform.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "dock.com": {
        "Subject": "Accelerating Client Onboarding Portals at Dock // Frontend Engineering",
        "Body": "Hi Emily,\n\nDock's vision for client onboarding and unified B2B workspaces is brilliant. Building shared, fiercely collaborative, state-driven client portals that feel instantly intuitive to end-users requires an engineering culture that treats the frontend with extreme care and rigor. This is the exact environment I excel in.\n\nI am a Senior Product Engineer with a heavy background in complex React architectures. At Aave, I architected high-performance Web3 client portals managing real-time decentralized ledger state. I essentially specialize in taking complex, shifting backend data and abstracting it into completely frictionless React UI.\n\nI build out of Lagos, Nigeria (WAT timezone), providing perfect async schedule overlap for collaboration. I treat frontend purely as a measurable engineering discipline—I rely heavily on Playwright E2E automation and PostHog tracking because I refuse to ship unmeasured code to end-users who expect high reliability.\n\nI've attached my CV for a deeper dive into my execution. I'd love to discuss how I can help bring your engineering roadmap at Dock to life.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    },
    
    "minka.ca": {
        "Subject": "Senior React Engineer for Minka's Clearinghouse Infrastructure",
        "Body": "Hi Eric,\n\nMinka's work in rebuilding open banking and clearinghouse infrastructure across regions is fundamentally fascinating to me. Architecting clean, high-performance interfaces on top of massive, real-time ledgers requires an engineering culture that treats the frontend with extreme financial rigor, and I believe I am a 10/10 fit for those technical challenges.\n\nThis aligns perfectly with my background. At Aave, I architected high-performance Web3 client portals where managing real-time decentralized ledger state and zero-latency transactions was an absolute requirement. Handling transaction finality in React is exactly where I thrive.\n\nI am a Senior Product Engineer based in Lagos, Nigeria (WAT timezone). This places me perfectly to overlap with your global async schedules, giving you seamless real-time collaboration. I also build strictly measurable UI, instrumenting my complete stack with intensive Playwright E2E coverage and deep PostHog telemetry.\n\nI've attached my CV for a deeper dive into my end-to-end execution. I'd love to discuss accelerating Minka's technical roadmap.\n\nBest regards,\n\nMaurice Edohoeket\nlinkedin.com/in/iedohoeket\nfolio-jet-mu.vercel.app"
    }
}

def generate_fully_custom_emails():
    custom_rows = []
    
    with open(CSV_PATH, mode='r', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        
        for row in reader:
            email = row.get("Email")
            domain = email.split('@')[1]
            
            if domain in CUSTOM_EMAILS:
                row['Subject'] = CUSTOM_EMAILS[domain]['Subject']
                row['Body'] = CUSTOM_EMAILS[domain]['Body']
                custom_rows.append(row)

    with open(OUT_PATH, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["Email", "Subject", "Body"])
        writer.writeheader()
        for row in custom_rows:
            writer.writerow(row)
            
    print(f"✅ Successfully synthesized 10 totally unique, deeply-researched bespoke emails.")
    print(f"Saved to: {OUT_PATH}")

if __name__ == "__main__":
    generate_fully_custom_emails()
