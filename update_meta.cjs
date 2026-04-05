const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const articlesDir = path.join(rootDir, 'pages', 'articles');

const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => path.join(articlesDir, f));
files.push(path.join(rootDir, 'index.html'));

for (const filePath of files) {
    if (!fs.existsSync(filePath)) continue;
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Add Favicon & Twitter/OG tags if not present
    if (!content.includes('favicon.png')) {
        let titleMatch = content.match(/<title>(.*?)<\/title>/);
        let descMatch = content.match(/<meta name="description" content="(.*?)"\s*\/>/);
        
        let title = titleMatch ? titleMatch[1] : "Maurice Eket";
        let desc = descMatch ? descMatch[1] : "";
        let newMeta = `
  <link rel="icon" type="image/png" href="/favicon.png" />
  <meta property="og:title" content="${title}" />
  <meta property="og:description" content="${desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:image" content="https://edohoeket.com/favicon.png" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:site" content="@skxngg" />
  <meta name="twitter:title" content="${title}" />
  <meta name="twitter:description" content="${desc}" />
  <meta name="twitter:image" content="https://edohoeket.com/favicon.png" />`;

        content = content.replace('</head>', newMeta + '\n</head>');
    }
    
    // Fix color in sitting-in-a-quiet-room
    if (filePath.includes('sitting-in-a-quiet-room')) {
        content = content.replace('color: #e0ff4f;', 'color: #fff;');
    }
    
    fs.writeFileSync(filePath, content);
}

console.log("Updated " + files.length + " files with favicon and OG tags.");
