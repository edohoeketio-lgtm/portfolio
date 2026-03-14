import { defineConfig } from 'vite';
import { resolve } from 'path';
import { readdirSync, statSync } from 'fs';

// Helper to recursively find all HTML files
function getHtmlFiles(dir, fileList = []) {
  const files = readdirSync(dir);
  for (const file of files) {
    const filePath = resolve(dir, file);
    if (statSync(filePath).isDirectory()) {
      // Ignore build output, dependencies, and hidden folders
      if (file !== 'node_modules' && file !== 'dist' && !file.startsWith('.')) {
        getHtmlFiles(filePath, fileList);
      }
    } else if (filePath.endsWith('.html')) {
      fileList.push(filePath);
    }
  }
  return fileList;
}

const inputEntries = {};
// Dynamically generate the Rollup input map for every HTML page
getHtmlFiles(__dirname).forEach((file) => {
  const relativePath = file.replace(__dirname, '').replace(/^[/\\]/, '');
  const key = relativePath.replace(/\.html$/, '').replace(/[/\\]/g, '_');
  // Fallback 'main' key for the root index.html to match Vite conventions
  inputEntries[key === 'index' ? 'main' : key] = file;
});

export default defineConfig({
  server: {
    port: 3000,
    open: true,
  },
  build: {
    rollupOptions: {
      input: inputEntries
    }
  }
});
