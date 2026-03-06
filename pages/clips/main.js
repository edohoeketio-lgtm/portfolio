/**
 * Lens Dashboard — Live Stat Animation + Video Control
 * Smoothly animates all stat values to simulate a real-time analytics feed.
 * Slows hero background video to 40% speed (60% slower).
 */

(function () {
    const stats = [
        { selector: 0, base: 1243, format: 'int' },
        { selector: 1, base: 38472, format: 'comma' },
        { selector: 2, base: 947, format: 'comma' },
        { selector: 3, base: 2841509, format: 'comma' },
        { selector: 4, base: 58700000, format: 'millions' },
        { selector: 5, base: 8.3, format: 'percent' },
    ];

    function formatValue(val, format) {
        switch (format) {
            case 'int':
                return Math.round(val).toLocaleString();
            case 'comma':
                return Math.round(val).toLocaleString();
            case 'millions':
                return (val / 1000000).toFixed(1) + 'M';
            case 'percent':
                return val.toFixed(1) + '%';
            default:
                return Math.round(val).toString();
        }
    }

    function randomDelta(base) {
        // Drift by ±0.5–2% of the base value
        const pct = (Math.random() * 1.5 + 0.5) / 100;
        return base * pct * (Math.random() > 0.5 ? 1 : -1);
    }

    let currentValues = stats.map(s => s.base);

    function tick() {
        const cards = document.querySelectorAll('.stat-value');
        if (!cards.length) return;

        stats.forEach((stat, i) => {
            const delta = randomDelta(stat.base);
            let next = currentValues[i] + delta;

            // Keep within ±8% of base so it never drifts too far
            const lo = stat.base * 0.92;
            const hi = stat.base * 1.08;
            if (next < lo) next = lo;
            if (next > hi) next = hi;

            currentValues[i] = next;

            if (cards[i]) {
                cards[i].textContent = formatValue(next, stat.format);
            }
        });

        // Also randomly nudge the trend percentages
        const trends = document.querySelectorAll('.stat-trend');
        trends.forEach(el => {
            const isPositive = el.classList.contains('positive');
            const base = parseFloat(el.textContent) || (isPositive ? 4 : -2);
            const nudge = (Math.random() - 0.5) * 0.4;
            let next = base + nudge;

            // Keep positive trends positive and negative trends negative
            if (isPositive && next < 0.1) next = 0.1;
            if (!isPositive && next > -0.1) next = -0.1;

            const sign = next >= 0 ? '+' : '';
            el.textContent = sign + next.toFixed(1) + '%';
        });
    }

    // Initial render
    tick();

    // Update every 2.5 seconds
    setInterval(tick, 2500);
})();
