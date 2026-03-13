export function initUI() {
    // ── View Toggle & CTA Initialization ──
    const homeBtn = document.getElementById('home-btn');
    if (homeBtn) {
        homeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Brutalist Mode: Anchored Preview ───────────
    const hoverPreview = document.getElementById('hover-preview');
    const brutalistItems = document.querySelectorAll('.brutalist-item');

    brutalistItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const previewImg = item.getAttribute('data-preview');
            if (previewImg && hoverPreview) {
                item.appendChild(hoverPreview);
                hoverPreview.innerHTML = `<img src="${previewImg}" alt="Preview">`;
                hoverPreview.style.left = '105%';
                hoverPreview.style.top = '-20px';
                hoverPreview.classList.add('active');
            }
        });

        item.addEventListener('mouseleave', () => {
            if (hoverPreview) hoverPreview.classList.remove('active');
        });
    });
}
