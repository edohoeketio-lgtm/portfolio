const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const articlesDir = path.join(rootDir, 'pages', 'articles');

const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => path.join(articlesDir, f));

let changed = 0;
for (const filePath of files) {
    if (!fs.existsSync(filePath)) continue;
    let content = fs.readFileSync(filePath, 'utf8');
    
    if (content.includes('>Quiet Room</h3>')) {
        content = content.replace(/>Quiet Room<\/h3>/g, '>Margin Notes</h3>');
        fs.writeFileSync(filePath, content, 'utf8');
        changed++;
    }
}
console.log(`Updated newsletter NAME in UI across ${changed} files.`);
