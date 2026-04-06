const fs = require('fs');
const path = require('path');

const articlesDir = path.join(__dirname, 'pages', 'articles');
const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html') && f !== 'sitting-in-a-quiet-room.html' && f !== 'index.html');

const shareCss = `
    .article-share {
      display: flex;
      gap: 1rem;
      margin: 3rem 0;
      flex-wrap: wrap;
    }
    .share-btn {
      background: transparent;
      color: #000;
      border: 2px solid #000;
      padding: 0.6rem 1.2rem;
      font-family: 'Space Mono', monospace;
      font-size: 0.9rem;
      cursor: pointer;
      border-radius: 4px;
      text-transform: uppercase;
      font-weight: 700;
      transition: all 0.2s ease;
    }
    .share-btn:hover {
      background: #000;
      color: #fff;
    }
`;

const shareHtml = `
        <div class="article-share">
          <button onclick="window.open(\`https://twitter.com/intent/tweet?text=\${encodeURIComponent(document.title)}&url=\${encodeURIComponent(window.location.href)}\`, '_blank')\" class="share-btn">Share on X</button>
          <button onclick="window.open(\`https://www.linkedin.com/sharing/share-offsite/?url=\${encodeURIComponent(window.location.href)}\`, '_blank')\" class="share-btn">Share on LinkedIn</button>
          <button onclick="navigator.clipboard.writeText(window.location.href).then(() => { const btn = event.target; const orig = btn.innerText; btn.innerText = 'Copied!'; setTimeout(() => btn.innerText = orig, 2000); })" class="share-btn">Copy Link</button>
        </div>
`;

for (const file of files) {
    let filePath = path.join(articlesDir, file);
    let content = fs.readFileSync(filePath, 'utf8');

    if (!content.includes('.article-share {')) {
        content = content.replace('</style>', shareCss + '\n  </style>');
    }

    if (!content.includes('<div class="article-share">')) {
        let match = content.indexOf('<div style="margin-top: 4rem;');
        if (match !== -1) {
            content = content.replace('<div style="margin-top: 4rem;', shareHtml + '\n        <div style="margin-top: 4rem;');
        }
    }
    
    // Update the form h3 label if needed
    content = content.replace(/Get The Drop/g, 'Quiet Room');

    fs.writeFileSync(filePath, content);
}
console.log("Updated 9 articles with share buttons and Quiet Room branding.");
