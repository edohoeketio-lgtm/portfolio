import os
import sys
import re
from datetime import datetime
import markdown

def generate_article_html(title, body, date_str):
    """Converts the markdown body into the brutalist HTML article template."""
    
    # Process markdown tags
    html_content = markdown.markdown(body, extensions=['fenced_code', 'tables'])
    
    # We don't have a reliable single-sentence excerpt natively in standard Github issues 
    # unless we parse out the first paragraph, so let's try to extract the first text block.
    # Fallback to empty string if no standard paragraph is found.
    excerpt_match = re.search(r'<p>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
    excerpt = excerpt_match.group(1).strip() if excerpt_match else "A new article."
    # clean out any HTML from the excerpt
    excerpt = re.sub(r'<[^>]+>', '', excerpt)
    
    # Create the slug
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
    file_path = f"pages/articles/{slug}.html"
    
    # Format the date (March 17, 2026)
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = dt.strftime("%B %d, %Y")
    short_date = dt.strftime("%b %d, %Y")

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} - Maurice</title>
  <meta name="description" content="{excerpt}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&family=Space+Mono&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />
  <style>
    .article-container {{
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
      padding-top: 4rem;
      padding-bottom: 6rem;
      padding-left: clamp(2rem, 6vw, 4rem);
      padding-right: clamp(2rem, 6vw, 4rem);
      box-sizing: border-box;
    }}
    .article-header {{
      margin-bottom: 4rem;
    }}
    .article-date {{
      font-family: 'Space Mono', monospace;
      font-size: 0.9rem;
      color: #666;
      display: block;
      margin-bottom: 1rem;
    }}
    .article-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: calc(clamp(2rem, 4vw, 3rem) - 2px);
      font-weight: 700;
      letter-spacing: -0.03em;
      line-height: 1.1;
      margin-bottom: 1.5rem;
    }}
    .article-content {{
      font-family: 'Inter', sans-serif;
      font-size: 1.2rem;
      line-height: 1.8;
      color: #222;
      overflow-wrap: break-word;
      word-wrap: break-word;
      max-width: 100%;
    }}
    @media (max-width: 640px) {{
      .article-content {{
        font-size: calc(1.2rem - 2px);
      }}
      .article-container {{
        padding-top: 7rem;
      }}
    }}
    .article-content h2 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2rem;
      font-weight: 700;
      margin: 4rem 0 1.5rem;
      letter-spacing: -0.02em;
    }}
    .article-content p {{
      margin-bottom: 1.5rem;
    }}
    .article-content pre {{
      background: #111;
      color: #fff;
      padding: 1.5rem;
      border-radius: 8px;
      overflow-x: auto;
      max-width: 100%;
      width: 100%;
      font-family: 'Space Mono', monospace;
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 2rem 0;
      box-sizing: border-box;
      -webkit-overflow-scrolling: touch;
    }}
    .article-content code {{
      font-family: 'Space Mono', monospace;
      background: #e0e0e0;
      padding: 0.2rem 0.4rem;
      border-radius: 4px;
      font-size: 0.9em;
    }}
    .article-content pre code {{
      background: transparent;
      padding: 0;
      border-radius: 0;
    }}
    .article-content ul {{
      margin-bottom: 1.5rem;
      padding-left: 1.5rem;
    }}
    .article-content li {{
      margin-bottom: 0.5rem;
    }}
  </style>
</head>
<body class="theme-brutalist">
  <div class="brutalist-layout-container" style="padding: 0; max-width: 100%;">
    <a href="/pages/articles/index.html" id="home-btn" aria-label="Back to articles" style="display: flex; background: #000; color: #fff; border: none; font-size: 1.2rem;">←</a>

    <article class="article-container">
      <header class="article-header">
        <span class="article-date">{formatted_date}</span>
        <h1 class="article-title">{title}</h1>
      </header>

      <div class="article-content">
        {html_content}

        <div style="margin-top: 4rem; padding: clamp(1.5rem, 5vw, 2.5rem); background: #000; color: #fff; border: 3px solid #000; box-shadow: none; border-radius: 8px; box-sizing: border-box; width: 100%;">
          <h3 style="margin-top: 0; margin-bottom: 0.5rem; font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; text-transform: uppercase;">Get The Drop</h3>
          <p style="font-family: 'Space Mono', monospace; font-size: 0.95rem; margin-bottom: 2rem;">Drop your email to get early access to tools and engineering insights before anyone else.</p>
          <form id="subscribe-form" action="https://formspree.io/f/mzdjvoav" method="POST" style="display: flex; gap: 1rem; align-items: stretch; flex-wrap: wrap; width: 100%;">
            <input type="email" name="email" placeholder="CTO@acme.inc" required style="flex-grow: 1; flex-basis: 100%; min-width: 0; padding: 1.2rem; border: 3px solid #000; font-family: 'Space Mono', monospace; font-size: 1rem; border-radius: 4px; outline: none; box-sizing: border-box;" />
            <button type="submit" style="background: #fff; color: #000; border: 3px solid #fff; padding: 1rem 2.5rem; font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 700; cursor: pointer; text-transform: uppercase; border-radius: 4px; white-space: nowrap; flex-grow: 1; box-sizing: border-box;">Subscribe</button>
          </form>
          <div id="subscribe-success" style="display: none; padding: 1.2rem; border: 3px solid #000; font-family: 'Space Mono', monospace; font-size: 1rem; border-radius: 4px; background: #e0ff4f; color: #000; font-weight: 600;">
            Thanks for subscribing! Keep an eye on your inbox.
          </div>
          <script>
            {{
              const form = document.getElementById('subscribe-form');
              const successMessage = document.getElementById('subscribe-success');

              form.addEventListener('submit', async (e) => {{
                e.preventDefault();
                
                const data = new FormData(form);
                try {{
                  const response = await fetch(form.action, {{
                    method: form.method,
                    body: data,
                    headers: {{ 'Accept': 'application/json' }}
                  }});
                  
                  if (response.ok) {{
                    form.style.display = 'none';
                    successMessage.style.display = 'block';
                  }}
                }} catch (error) {{
                  console.error('Subscription failed', error);
                  alert('Oops! There was a problem submitting your email.');
                }}
              }});
            }}
          </script>
        </div>
      </div>
    </article>
  </div>
</body>
</html>"""

    # Write the new article
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)
    
    print(f"Created {file_path}")
    return slug, short_date, excerpt

def update_index_page(title, slug, short_date, excerpt):
    """Injects the new article card at the top of the article index."""
    index_path = "pages/articles/index.html"
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Index file not found or couldn't read it: {e}")
        return
        
    card_html = f"""
      <a href="/pages/articles/{slug}.html" class="article-card">
        <span class="article-date">{short_date}</span>
        <h2 class="article-headline">{title}</h2>
        <p class="article-excerpt">{excerpt}</p>
      </a>"""

    # Find the injection point right after the <main class="articles-list"> tag
    if '<main class="articles-list">' in content:
        content = content.replace('<main class="articles-list">', f'<main class="articles-list">\n{card_html}')
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated articles/index.html")
    else:
        print("Could not find the injection point in articles/index.html")

def main():
    title = os.environ.get("ISSUE_TITLE")
    body = os.environ.get("ISSUE_BODY", "")
    date_str = os.environ.get("ISSUE_DATE")

    if not title or not date_str:
        print("Error: Missing ISSUE_TITLE or ISSUE_DATE environment variables.")
        sys.exit(1)
        
    # Replace CRLF with LF just in case Markdown is picky
    body = body.replace('\\r\\n', '\\n')

    slug, short_date, excerpt = generate_article_html(title, body, date_str)
    update_index_page(title, slug, short_date, excerpt)

if __name__ == "__main__":
    main()
