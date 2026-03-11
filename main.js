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
        if (previewImg) {
            item.appendChild(hoverPreview);
            hoverPreview.innerHTML = `<img src="${previewImg}" alt="Preview">`;
            hoverPreview.style.left = '105%';
            hoverPreview.style.top = '-20px';
            hoverPreview.classList.add('active');
        }
    });

    item.addEventListener('mouseleave', () => {
        hoverPreview.classList.remove('active');
    });
});

// ── Intersection Observer for Reveals ──────────
const revealElements = document.querySelectorAll('.reveal');
if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        revealObserver.observe(el);
    });
}

// ── Chat Contact Interface ────────────────────────
const chatModal = document.getElementById('chat-modal');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const chatClose = document.getElementById('chat-close');
const contactBtn = document.getElementById('brutalist-contact-btn');

if (chatModal) {
    const chatSteps = [
        { question: "hey! 👋 what's your name?", field: 'name', placeholder: 'Your name...' },
        { question: null, field: null },
        { question: "nice — what are you looking to build?", field: 'project_details', placeholder: 'A killer web app...' },
        { question: "last thing — drop your email so I can get back to you", field: 'email', placeholder: 'you@email.com' },
    ];

    let chatStep = 0;
    const chatData = {};

    function scrollChat() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addUserBubble(text) {
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble user';
        bubble.innerHTML = `${text}<span class="blue-checks">✓✓</span>`;
        chatMessages.appendChild(bubble);
        scrollChat();
        setTimeout(() => {
            const checks = bubble.querySelector('.blue-checks');
            if (checks) checks.classList.add('seen');
        }, 800);
    }

    function typeMessage(text) {
        return new Promise(resolve => {
            const bubble = document.createElement('div');
            bubble.className = 'chat-bubble maurice typing-cursor';
            bubble.textContent = '';
            chatMessages.appendChild(bubble);
            scrollChat();

            let i = 0;
            const speed = 30 + Math.random() * 20;
            const interval = setInterval(() => {
                bubble.textContent += text[i];
                i++;
                scrollChat();
                if (i >= text.length) {
                    clearInterval(interval);
                    bubble.classList.remove('typing-cursor');
                    resolve();
                }
            }, speed);
        });
    }

    function disableInput() {
        if (chatInput) chatInput.disabled = true;
        if (chatSend) chatSend.disabled = true;
    }

    function enableInput(placeholder) {
        if (chatInput) {
            chatInput.disabled = false;
            chatInput.placeholder = placeholder || 'Type here...';
            chatInput.value = '';
            chatInput.focus();
        }
        if (chatSend) chatSend.disabled = false;
    }

    async function startChat() {
        chatStep = 0;
        chatMessages.innerHTML = '';
        Object.keys(chatData).forEach(k => delete chatData[k]);
        disableInput();
        await typeMessage(chatSteps[0].question);
        enableInput(chatSteps[0].placeholder);
    }

    async function handleSend() {
        const value = chatInput.value.trim();
        if (!value) return;

        disableInput();
        addUserBubble(value);

        if (chatStep === 0) {
            chatData.name = value;
            chatSteps[1].question = `nice to meet you, ${value}! who are you with? (company or just yourself)`;
            chatSteps[1].field = 'company';
            chatStep = 1;
            await new Promise(r => setTimeout(r, 600));
            await typeMessage(chatSteps[1].question);
            enableInput('Company name...');
        } else if (chatStep === 1) {
            chatData.company = value;
            chatStep = 2;
            await new Promise(r => setTimeout(r, 600));
            await typeMessage(chatSteps[2].question);
            enableInput(chatSteps[2].placeholder);
        } else if (chatStep === 2) {
            chatData.project_details = value;
            chatStep = 3;
            await new Promise(r => setTimeout(r, 600));
            await typeMessage(chatSteps[3].question);
            enableInput(chatSteps[3].placeholder);
        } else if (chatStep === 3) {
            chatData.email = value;
            chatStep = 4;
            const formData = new FormData();
            formData.append('name', chatData.name);
            formData.append('company', chatData.company);
            formData.append('project_details', chatData.project_details);
            formData.append('email', chatData.email);
            fetch("https://formsubmit.co/ajax/edohoeketio@gmail.com", {
                method: "POST",
                body: formData,
                headers: { 'Accept': 'application/json' }
            }).catch(() => { });

            await new Promise(r => setTimeout(r, 800));
            await typeMessage("perfect — I've got everything I need 🤝");
            await new Promise(r => setTimeout(r, 400));
            await typeMessage("i'll get back to you within 24 hours. talk soon!");
            chatInput.placeholder = 'Sent ✓';
        }
    }

    if (contactBtn) contactBtn.addEventListener('click', () => { chatModal.classList.add('open'); startChat(); });
    if (chatClose) chatClose.addEventListener('click', () => { chatModal.classList.remove('open'); });
    if (chatModal) chatModal.addEventListener('click', (e) => { if (e.target === chatModal) chatModal.classList.remove('open'); });
    if (chatSend) chatSend.addEventListener('click', handleSend);
    if (chatInput) chatInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') handleSend(); });
}

// ── Music Pill Rotation ──
const songs = [
    { title: "Sing about me, im dying of thirst", artist: "Kendrick Lamar", art: "/kendrick.png" },
    { title: "Poor thang.", artist: "J. Cole", art: "/jcole.png" },
    { title: "lost souls", artist: "Baby Keem", art: "/babykeem.jpg" }
];

let currentSongIndex = 0;
const musicArt = document.getElementById('music-art');
const musicTitle = document.getElementById('music-title');
const musicArtist = document.getElementById('music-artist');
const musicPill = document.querySelector('.music-pill');

function rotateSong() {
    if (!musicPill || !musicArt || !musicTitle || !musicArtist) return;
    currentSongIndex = (currentSongIndex + 1) % songs.length;
    const song = songs[currentSongIndex];
    musicPill.style.opacity = '0';
    musicPill.style.transform = 'translateY(5px)';
    setTimeout(() => {
        musicArt.src = song.art;
        musicTitle.textContent = song.title;
        musicArtist.textContent = song.artist;
        musicPill.style.opacity = '1';
        musicPill.style.transform = 'translateY(0)';
    }, 400);
}

if (musicPill) setInterval(rotateSong, 45000);
