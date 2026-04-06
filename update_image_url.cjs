const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const articlesDir = path.join(rootDir, 'pages', 'articles');

const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => path.join(articlesDir, f));
files.push(path.join(rootDir, 'index.html'));

let changed = 0;
for (const filePath of files) {
    if (!fs.existsSync(filePath)) continue;
    let content = fs.readFileSync(filePath, 'utf8');
    
    if (content.includes('edohoeket.com/favicon.png')) {
        content = content.split('edohoeket.com/favicon.png').join('edohoeket.com/logo.png');
        fs.writeFileSync(filePath, content, 'utf8');
        changed++;
    }
}
console.log(`Updated ${changed} files.`);
