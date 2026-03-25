# Guardian Clone Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Architect a completely headless, dynamic news platform (Web + iOS + Android) that leapfrogs The Guardian's legacy infrastructure, featuring dynamic category routing, automated content archiving, and instantaneous editorial publishing.

**Architecture:** 
1. **Headless CMS (Sanity.io):** Editors write content in a secure dashboard. Articles are saved as JSON with tags (`category: 'world'`, `publishedAt`). 
2. **Frontend Engine (Next.js):** Uses Incremental Static Regeneration (ISR). When an editor hits publish, Sanity fires a webhook to Vercel. Vercel rebuilds *only* that specific page in the background in milliseconds and pushes it to global Edge networks. 
3. **Mobile Engine (React Native/Expo):** Queries the exact same Sanity GraphQL API. 
4. **Dynamic Flow:** Old content is never manually deleted. The frontend queries `ORDER BY publishedAt DESC LIMIT 20`. New content automatically pushes old content into logical `/archive` routes.

**Tech Stack:** Next.js 14 (App Router), React Native (Expo), Sanity.io, Tailwind CSS, Vercel ISR, TypeScript.

---

### Task 1: Initialize Monorepo & Base Infrastructure

**Files:**
- Create: `package.json` (Monorepo Root)
- Create: `apps/web/package.json`
- Create: `apps/mobile/package.json`
- Create: `packages/cms/sanity.config.ts`

- [ ] **Step 1: Scaffold Turborepo**
Run `npx create-turbo@latest .` to set up the workspace for Web and Mobile to share UI components.

- [ ] **Step 2: Initialize Sanity Studio**
Run `npm create sanity@latest` inside `packages/cms`.

### Task 2: Define Content Schemas (The Database)

**Files:**
- Create: `packages/cms/schemas/article.ts`
- Create: `packages/cms/schemas/category.ts`

- [ ] **Step 1: Write the Article Schema**
```typescript
export default {
  name: 'article',
  type: 'document',
  title: 'News Article',
  fields: [
    { name: 'title', type: 'string', title: 'Headline' },
    { name: 'slug', type: 'slug', options: { source: 'title' } },
    { name: 'category', type: 'reference', to: [{ type: 'category' }] },
    { name: 'publishedAt', type: 'datetime', title: 'Publication Date' },
    { name: 'body', type: 'array', of: [{ type: 'block' }] }
  ]
}
```

- [ ] **Step 2: Test CMS Deployment**
Run `sanity deploy` to push the database schema live for editors.

### Task 3: Build Web Frontend & Dynamic Category Routing

**Files:**
- Create: `apps/web/app/page.tsx`
- Create: `apps/web/app/[category]/page.tsx`
- Create: `apps/web/app/[category]/[slug]/page.tsx`
- Create: `apps/web/lib/sanity.ts`

- [ ] **Step 1: Implement the Data Fetcher**
```typescript
// apps/web/lib/sanity.ts
export async function getLatestArticles(category?: string) {
  const filter = category ? `&& category->slug.current == $category` : '';
  return client.fetch(`*[_type == "article" ${filter}] | order(publishedAt desc)[0...20]`);
}
```

- [ ] **Step 2: Build the Dynamic Homepage**
```tsx
// apps/web/app/page.tsx
export const revalidate = 60; // ISR cache logic

export default async function Home() {
  const articles = await getLatestArticles();
  return <NewsFeed articles={articles} />
}
```

- [ ] **Step 3: Build the Category Router**
```tsx
// apps/web/app/[category]/page.tsx
export default async function CategoryPage({ params }) {
  const articles = await getLatestArticles(params.category);
  return <CategoryFeed title={params.category} articles={articles} />
}
```

### Task 4: Setup Webhook Invalidation (The Magic Update)

**Files:**
- Create: `apps/web/app/api/revalidate/route.ts`

- [ ] **Step 1: Build the On-Demand Invalidation Logic**
```typescript
import { revalidatePath } from 'next/cache';
export async function POST(req) {
  // When Sanity fires this hook, bust the cache immediately
  revalidatePath('/'); 
  return Response.json({ revalidated: true });
}
```

### Task 5: Mobile App Integration

**Files:**
- Create: `apps/mobile/app/(tabs)/index.tsx`
- Create: `apps/mobile/lib/sanity.ts`

- [ ] **Step 1: Build Mobile Feed**
```tsx
export default function MobileFeed() {
  // Fetch from the identical Sanity API
  const { data } = useSanityQuery(`*[_type == "article"] | order(publishedAt desc)[0...20]`);
  return <FlatList data={data} renderItem={ArticleCard} />
}
```
