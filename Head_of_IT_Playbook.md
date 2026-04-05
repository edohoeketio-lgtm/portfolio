# The Guardian NG - Head of IT 30-Day Transition Playbook

## Executive Summary
This document serves as the tactical, operational, and leadership playbook for transitioning into the Head of IT role at The Guardian NG. Moving from a modern engineering background into a massive legacy WordPress environment requires a swift injection of strict access control, modern CI/CD deployment pipelines, and decisive leadership.

---

## PART 1: The First Week Strategy (Setting the Tone)

Your first week isn't about rewriting code—it’s about asserting control, mapping the battlefield, and proving stability.

### 1. Audit Everything. Change Nothing.
Spend your first 3 days creating an Architecture Map. Find out where DNS points, where the databases live, and what cron jobs are running. You are the meticulous engineer who demands blueprints before touching load-bearing walls.

### 2. Secure the Fortress
Export a list of all users with Administrator/Editor permissions. Ruthlessly cull formers employees. Mandate Two-Factor Authentication (2FA) for all remaining Admins immediately. 

### 3. The "Bus Factor" Assessment
Schedule 1-on-1s with whoever currently handles engineering. Figure out what undocumented knowledge is isolated in their heads. Build institutional resilience.

### 4. Verify the "Oh Sh*t" Button
Never trust automatic backups. Pull a full database and file backup to a local environment. Attempt to boot it up manually to prove you can restore the site in a crisis.

### 5. The Financial & Billing Audit 
Map out every SaaS tool, hosting bill, and plugin subscription. Ensure all billing is tied to a corporate card and a corporate group email (`it@guardian.ng`), not a personal employee email. 

### 6. Protect the Revenue (SEO & Ads)
Audit the SEO plugins (Yoast/RankMath). Strip "Admin" access from the Editorial team so they cannot accidentally break global traffic redirects. 

### 7. Dictate the New Standard: "The CLI Rule"
End the era of "cowboy coding." Moving forward, infrastructure is treated as code. No UI plugin installs on production. No editing PHP files in the browser. 

---

## PART 2: The Execution Guide (Technical Scripts & Commands)

### The Pre-Boarding "Keys to the Kingdom" Email
Send this to Operations/HR three days before you start:
> **Subject:** IT Onboarding: Infrastructure Access Checklist
> 
> Hi Team, 
> To ensure I can manage the infrastructure effectively on Day 1, please ensure I am provisioned with "Owner" or "Super Admin" level access to the following systems prior to my start:
> 
> 1. Server/Hosting Provider (AWS/WP Engine) + SSH keys
> 2. Primary DNS Registrar (GoDaddy/Namecheap)
> 3. Cloudflare / WAF Account
> 4. GitHub/Gitlab Repositories
> 5. A dedicated Administrator account on the live WordPress site
>
> Please securely transmit these credentials. Best, [Your Name]

### Emergency "Fire Drill" Commands (WP-CLI)
Do not use the WordPress GUI to fix emergencies. SSH into the server and run these commands:
*   **Database Backup:** `wp db export backup-date.sql`
*   **Mass Flush Cache (Under Traffic Surges):** `wp cache flush`
*   **Revert a Broken Plugin:** `wp plugin update [plugin-name] --version=[previous-version]`
*   **Demote a Rogue Admin:** `wp user set-role [username] subscriber`

### The "Cowboy Coding" Killswitch
Immediately inject this into `wp-config.php` to prevent developers from editing code in the browser:
```php
define( 'DISALLOW_FILE_EDIT', true );
```

---

## PART 3: The Deployment Pipeline Architecture

You streamline deployments not by reading every line of code, but by building a robust system that stops errors at the gate.

### 1. The Vault (GitHub) & Taking the Keys
You physically remove direct FTP/Server access from junior developers. All website code is moved to a highly secure repository (GitHub).

### 2. The Bouncer (Branch Protection)
Developers must submit a "Pull Request" on GitHub. We set a "Branch Protection Rule" forcing all code to stop at the gate. The code cannot merge into the live site until a designated Senior Developer reviews it and clicks "Approve." (You delegate the code reading; you do not do it yourself).

### 3. Visual Testing (The Staging Server)
Before approval, the code automatically builds a secret identical copy of the website (e.g., `staging.guardian.ng`). You and the QoS team can open the browser, click the buttons, and verify it looks good visually without reading a single line of PHP.

### 4. The Robot Delivery (Automated Deploy)
Once human-approved, GitHub Actions automatically executes the deployment. Because this automated robot is the *only* entity that has the live server password, developers are physically forced to follow your review process.

---

## PART 4: Team Leadership & Communication

### The "CLI Rule" Speech to the Engineering Team
Deliver this speech in your first engineering meeting:

"Team, thank you. I know what it takes to keep a publication of this size running every day. But my job as Head of IT is to protect this platform—and more importantly, to protect *you*. 

Right now, if breaking news hits, the standard practice is often to log into the dashboard and type raw PHP right in the browser. We operate at too large a scale for that anymore. That cowboy coding leaves you one typo away from taking down the entire homepage, costing the company revenue and putting the blame entirely on your shoulders.

**Starting next week, that stops.** 

I am disabling live file editing from within the WordPress dashboard. Here is our new baseline, which I call the **CLI Rule**:
1. No direct edits on production. Period. 
2. Local First: All code changes are developed on your local machine.
3. Version Control: You commit to our Git repository.
4. Staging Deployments: Code is pushed to staging, human-reviewed, and deployed by our automated robot.

I know this is a shift, and I am not expecting you to transition overnight alone. I will be personally working with each of you to set up your local environments and architect these pipelines. My goal is to give you peace of mind. When you push, you should know with 100% certainty that it won't crash the site. We treat infrastructure as code now. Let's get to work."
