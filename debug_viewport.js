const results = [];
const elements = document.querySelectorAll('*');
for (let el of elements) {
  const rect = el.getBoundingClientRect();
  if (rect.right > window.innerWidth || rect.width > window.innerWidth) {
    results.push({
      tag: el.tagName,
      class: el.className,
      id: el.id,
      width: rect.width,
      right: rect.right,
      windowWidth: window.innerWidth
    });
  }
}
document.body.innerHTML = `<textarea id="debug-output" style="width:100%;height:500px;">${JSON.stringify(results, null, 2)}</textarea>`;
