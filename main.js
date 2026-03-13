import { initUI } from './src/modules/UIController.js';
import { initScroll } from './src/modules/ScrollController.js';
import { initChat } from './src/modules/ChatController.js';
import { initAudio } from './src/modules/AudioController.js';

document.addEventListener('DOMContentLoaded', () => {
    initUI();
    initScroll();
    initChat();
    initAudio();
});
