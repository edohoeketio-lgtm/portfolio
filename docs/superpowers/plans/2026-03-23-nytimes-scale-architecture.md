# Enterprise News Platform Architecture (NYTimes Scale)

## 1. The UX & Dynamic Flow Mechanics (The "How It Works")
Unlike smaller blogs, enterprise platforms like The New York Times do not rely on editors "dragging and dropping" articles onto a homepage. With thousands of articles published daily, manual curation at scale is impossible. 

Instead, it relies on **Algorithmically Driven Content Modules**.

**How Headlines Change Automatically:**
1. **The Metadata Tagging System:** When an editor writes an article in Sanity.io, they don't pick where it goes on the homepage. They assign it metadata:
   - `Priority`: [Breaking, Hero, Standard, Briefing]
   - `Category`: [World, Business, Technology]
   - `Shelf Life`: [3 hours (Live), 24 hours (Standard), Evergreen]
2. **The Frontend Aggregator:** The Next.js website homepage is composed of blank "Zones" (e.g., The Lead Story Zone, The Top 3 Zone, The Opinion Zone).
3. **The Data Pipeline:** Every 60 seconds (or immediately via Webhook on breaking news), the Website Engine asks the CMS: *"Give me the 1 most recent article tagged 'Hero'."* It asks again: *"Give me the 5 most recent articles tagged 'Technology' that aren't the Hero."*
4. **The Slide-Down Effect:** Because the frontend is querying purely by *Time* and *Priority*, when a new Hero article is published, the previous Hero article instantly gets bumped down to a "Standard" slot, and the oldest Standard article falls off the homepage into the `/archive` or category pages. 

This creates a breathing, living homepage that updates autonomously 24/7.

## 2. Infrastructure Scale (Beating The Guardian)

To handle millions of concurrent users reading unique headlines, the system must be entirely decoupled.

```text
[Sanity CMS] -> [Redis Edge Cache] -> [Next.js Global Edge Network] -> [Users]
```

- **The Database Shield:** If 5 million people visit the site because of breaking news, 0 of them hit your database. 100% of them hit the Global Edge Network (Vercel/Cloudflare).
- **Stale-While-Revalidate (SWR):** When a headline changes, the Edge Network serves the *old* headline for 200 milliseconds to the first user while it fetches the *new* headline in the background. The next user gets the new headline. This guarantees the site literally never slows down, even during content updates.

## 3. The Cross-Platform Strategy
The absolute key to rivaling NYTimes without a 500-person engineering team is **"Write Once, Publish Everywhere."**

- Because the articles are pure JSON data (not HTML), the Next.js Web App and the React Native Mobile App (iOS/Android) pull from the *exact same API endpoint*.
- If an editor corrects a typo in a headline, it fixes instantly on the Web Homepage, the Mobile App Feed, and Apple News syndication simultaneously.

---

### Implementation Phases

**PHASE 1: The Headless Core & Schema**
- Define the Sanity Schema (`Article`, `Author`, `Category`, `Tag`).
- Implement the "Priority" and "Layout" metadata fields for algorithmic homepage placement.
- Build the Webhook pipeline that triggers cache invalidation on publish.

**PHASE 2: The Next.js Frontend Framework**
- Build the Component Library (HeroCards, StandardCards, OpinionCards).
- Implement the server-side queries that populate the dynamic "Zones".
- Configure Incremental Static Regeneration (ISR) and Edge Caching.

**PHASE 3: Cross-Platform Extension**
- Build the Expo (React Native) application.
- Consume the exact same Sanity backend.
- Implement native push notifications linked to the CMS publish event.
