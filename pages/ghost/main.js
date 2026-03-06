/**
 * Spectral Ghost — Interactive 3D Effect
 * Original code by Filip Zrnzevic, adapted for Vite/npm
 */

import * as THREE from 'three';
import { Pane } from 'tweakpane';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';

// Preloader management
class PreloaderManager {
  constructor() {
    this.preloader = document.getElementById("preloader");
    this.mainContent = document.getElementById("main-content");
    this.progressBar = document.querySelector(".progress-bar");
    this.loadingSteps = 0;
    this.totalSteps = 5;
    this.isComplete = false;
  }

  updateProgress(step) {
    this.loadingSteps = Math.min(step, this.totalSteps);
    const percentage = (this.loadingSteps / this.totalSteps) * 100;
    this.progressBar.style.width = `${percentage}%`;
  }

  complete(canvas) {
    if (this.isComplete) return;
    this.isComplete = true;
    this.updateProgress(this.totalSteps);

    setTimeout(() => {
      this.preloader.classList.add("fade-out");
      this.mainContent.classList.add("fade-in");
      canvas.classList.add("fade-in");

      setTimeout(() => {
        this.preloader.style.display = "none";
      }, 1000);
    }, 1500);
  }
}

const preloader = new PreloaderManager();

document.body.style.transform = "translateZ(0)";
document.body.style.backfaceVisibility = "hidden";
document.body.style.perspective = "1000px";

preloader.updateProgress(1);

// Scene
const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 20;

preloader.updateProgress(2);

// Renderer
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  powerPreference: "high-performance",
  alpha: true,
  premultipliedAlpha: false,
  stencil: false,
  depth: true,
  preserveDrawingBuffer: false
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.9;
renderer.setClearColor(0x000000, 0);
document.body.appendChild(renderer.domElement);

renderer.domElement.style.position = "absolute";
renderer.domElement.style.top = "0";
renderer.domElement.style.left = "0";
renderer.domElement.style.zIndex = "2";
renderer.domElement.style.pointerEvents = "auto";
renderer.domElement.style.background = "transparent";

// Post-processing
const originalBloomSettings = { strength: 0.3, radius: 1.25, threshold: 0.0 };

const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  originalBloomSettings.strength,
  originalBloomSettings.radius,
  originalBloomSettings.threshold
);
composer.addPass(bloomPass);

preloader.updateProgress(3);

// Analog Decay Shader
const analogDecayShader = {
  uniforms: {
    tDiffuse: { value: null },
    uTime: { value: 0.0 },
    uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
    uAnalogGrain: { value: 0.4 },
    uAnalogBleeding: { value: 1.0 },
    uAnalogVSync: { value: 1.0 },
    uAnalogScanlines: { value: 1.0 },
    uAnalogVignette: { value: 1.0 },
    uAnalogJitter: { value: 0.4 },
    uAnalogIntensity: { value: 0.6 },
    uLimboMode: { value: 0.0 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float uTime;
    uniform vec2 uResolution;
    uniform float uAnalogGrain;
    uniform float uAnalogBleeding;
    uniform float uAnalogVSync;
    uniform float uAnalogScanlines;
    uniform float uAnalogVignette;
    uniform float uAnalogJitter;
    uniform float uAnalogIntensity;
    uniform float uLimboMode;
    varying vec2 vUv;

    float random(vec2 st) {
      return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
    }

    float random(float x) {
      return fract(sin(x) * 43758.5453123);
    }

    float gaussian(float z, float u, float o) {
      return (1.0 / (o * sqrt(2.0 * 3.1415))) * exp(-(((z - u) * (z - u)) / (2.0 * (o * o))));
    }

    vec3 grain(vec2 uv, float time, float intensity) {
      float seed = dot(uv, vec2(12.9898, 78.233));
      float noise = fract(sin(seed) * 43758.5453 + time * 2.0);
      noise = gaussian(noise, 0.0, 0.5 * 0.5);
      return vec3(noise) * intensity;
    }

    void main() {
      vec2 uv = vUv;
      float time = uTime * 1.8;

      vec2 jitteredUV = uv;
      if (uAnalogJitter > 0.01) {
        float jitterAmount = (random(vec2(floor(time * 60.0))) - 0.5) * 0.003 * uAnalogJitter * uAnalogIntensity;
        jitteredUV.x += jitterAmount;
        jitteredUV.y += (random(vec2(floor(time * 30.0) + 1.0)) - 0.5) * 0.001 * uAnalogJitter * uAnalogIntensity;
      }

      if (uAnalogVSync > 0.01) {
        float vsyncRoll = sin(time * 2.0 + uv.y * 100.0) * 0.02 * uAnalogVSync * uAnalogIntensity;
        float vsyncChance = step(0.95, random(vec2(floor(time * 4.0))));
        jitteredUV.y += vsyncRoll * vsyncChance;
      }

      vec4 color = texture2D(tDiffuse, jitteredUV);

      if (uAnalogBleeding > 0.01) {
        float bleedAmount = 0.012 * uAnalogBleeding * uAnalogIntensity;
        float offsetPhase = time * 1.5 + uv.y * 20.0;
        vec2 redOffset = vec2(sin(offsetPhase) * bleedAmount, 0.0);
        vec2 blueOffset = vec2(-sin(offsetPhase * 1.1) * bleedAmount * 0.8, 0.0);
        float r = texture2D(tDiffuse, jitteredUV + redOffset).r;
        float g = texture2D(tDiffuse, jitteredUV).g;
        float b = texture2D(tDiffuse, jitteredUV + blueOffset).b;
        color = vec4(r, g, b, color.a);
      }

      if (uAnalogGrain > 0.01) {
        vec3 grainEffect = grain(uv, time, 0.075 * uAnalogGrain * uAnalogIntensity);
        grainEffect *= (1.0 - color.rgb);
        color.rgb += grainEffect;
      }

      if (uAnalogScanlines > 0.01) {
        float scanlineFreq = 600.0 + uAnalogScanlines * 400.0;
        float scanlinePattern = sin(uv.y * scanlineFreq) * 0.5 + 0.5;
        float scanlineIntensity = 0.1 * uAnalogScanlines * uAnalogIntensity;
        color.rgb *= (1.0 - scanlinePattern * scanlineIntensity);
        float horizontalLines = sin(uv.y * scanlineFreq * 0.1) * 0.02 * uAnalogScanlines * uAnalogIntensity;
        color.rgb *= (1.0 - horizontalLines);
      }

      if (uAnalogVignette > 0.01) {
        vec2 vignetteUV = (uv - 0.5) * 2.0;
        float vignette = 1.0 - dot(vignetteUV, vignetteUV) * 0.3 * uAnalogVignette * uAnalogIntensity;
        color.rgb *= vignette;
      }

      if (uLimboMode > 0.5) {
        float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
        color.rgb = vec3(gray);
      }

      gl_FragColor = color;
    }
  `
};

const analogDecayPass = new ShaderPass(analogDecayShader);
composer.addPass(analogDecayPass);

const outputPass = new OutputPass();
composer.addPass(outputPass);

// Parameters
const params = {
  bodyColor: 0x0f2027,
  glowColor: "orange",
  eyeGlowColor: "green",
  ghostOpacity: 0.88,
  ghostScale: 2.4,
  emissiveIntensity: 5.8,
  pulseSpeed: 1.6,
  pulseIntensity: 0.6,
  eyeGlowIntensity: 4.5,
  eyeGlowDecay: 0.95,
  eyeGlowResponse: 0.31,
  rimLightIntensity: 1.8,
  followSpeed: 0.075,
  wobbleAmount: 0.35,
  floatSpeed: 1.6,
  movementThreshold: 0.07,
  particleCount: 250,
  particleDecayRate: 0.005,
  particleColor: "orange",
  createParticlesOnlyWhenMoving: true,
  particleCreationRate: 5,
  revealRadius: 43,
  fadeStrength: 2.2,
  baseOpacity: 0.35,
  revealOpacity: 0.0,
  fireflyGlowIntensity: 2.6,
  fireflySpeed: 0.04,
  analogIntensity: 0.6,
  analogGrain: 0.4,
  analogBleeding: 1.0,
  analogVSync: 1.0,
  analogScanlines: 1.0,
  analogVignette: 1.0,
  analogJitter: 0.4,
  limboMode: false
};

const fluorescentColors = {
  cyan: 0x00ffff, lime: 0x00ff00, magenta: 0xff00ff, yellow: 0xffff00,
  orange: 0xff4500, pink: 0xff1493, purple: 0x9400d3, blue: 0x0080ff,
  green: 0x00ff80, red: 0xff0040, teal: 0x00ffaa, violet: 0x8a2be2
};

// Atmosphere
const atmosphereGeometry = new THREE.PlaneGeometry(300, 300);
const atmosphereMaterial = new THREE.ShaderMaterial({
  uniforms: {
    ghostPosition: { value: new THREE.Vector3(0, 0, 0) },
    revealRadius: { value: params.revealRadius },
    fadeStrength: { value: params.fadeStrength },
    baseOpacity: { value: params.baseOpacity },
    revealOpacity: { value: params.revealOpacity },
    time: { value: 0 }
  },
  vertexShader: `
    varying vec2 vUv;
    varying vec3 vWorldPosition;
    void main() {
      vUv = uv;
      vec4 worldPos = modelMatrix * vec4(position, 1.0);
      vWorldPosition = worldPos.xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 ghostPosition;
    uniform float revealRadius;
    uniform float fadeStrength;
    uniform float baseOpacity;
    uniform float revealOpacity;
    uniform float time;
    varying vec2 vUv;
    varying vec3 vWorldPosition;

    void main() {
      float dist = distance(vWorldPosition.xy, ghostPosition.xy);
      float dynamicRadius = revealRadius + sin(time * 2.0) * 5.0;
      float reveal = smoothstep(dynamicRadius * 0.2, dynamicRadius, dist);
      reveal = pow(reveal, fadeStrength);
      float opacity = mix(revealOpacity, baseOpacity, reveal);
      gl_FragColor = vec4(0.001, 0.001, 0.002, opacity);
    }
  `,
  transparent: true,
  depthWrite: false
});

const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
atmosphere.position.z = -50;
atmosphere.renderOrder = -100;
scene.add(atmosphere);

const ambientLight = new THREE.AmbientLight(0x0a0a2e, 0.08);
scene.add(ambientLight);

// Ghost
const ghostGroup = new THREE.Group();
scene.add(ghostGroup);

const ghostGeometry = new THREE.SphereGeometry(2, 40, 40);
const positionAttribute = ghostGeometry.getAttribute("position");
const positions = positionAttribute.array;
for (let i = 0; i < positions.length; i += 3) {
  if (positions[i + 1] < -0.2) {
    const x = positions[i];
    const z = positions[i + 2];
    const noise1 = Math.sin(x * 5) * 0.35;
    const noise2 = Math.cos(z * 4) * 0.25;
    const noise3 = Math.sin((x + z) * 3) * 0.15;
    positions[i + 1] = -2.0 + noise1 + noise2 + noise3;
  }
}
ghostGeometry.computeVertexNormals();

const ghostMaterial = new THREE.MeshStandardMaterial({
  color: params.bodyColor,
  transparent: true,
  opacity: params.ghostOpacity,
  emissive: fluorescentColors[params.glowColor],
  emissiveIntensity: params.emissiveIntensity,
  roughness: 0.02,
  metalness: 0.0,
  side: THREE.DoubleSide,
  alphaTest: 0.1
});

const ghostBody = new THREE.Mesh(ghostGeometry, ghostMaterial);
ghostGroup.add(ghostBody);

// Rim lights
const rimLight1 = new THREE.DirectionalLight(0x4a90e2, params.rimLightIntensity);
rimLight1.position.set(-8, 6, -4);
scene.add(rimLight1);

const rimLight2 = new THREE.DirectionalLight(0x50e3c2, params.rimLightIntensity * 0.7);
rimLight2.position.set(8, -4, -6);
scene.add(rimLight2);

preloader.updateProgress(4);

// Eyes
function createEyes() {
  const eyeGroup = new THREE.Group();
  ghostGroup.add(eyeGroup);

  const socketGeometry = new THREE.SphereGeometry(0.45, 16, 16);
  const socketMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });

  const leftSocket = new THREE.Mesh(socketGeometry, socketMaterial);
  leftSocket.position.set(-0.7, 0.6, 1.9);
  leftSocket.scale.set(1.1, 1.0, 0.6);
  eyeGroup.add(leftSocket);

  const rightSocket = new THREE.Mesh(socketGeometry, socketMaterial);
  rightSocket.position.set(0.7, 0.6, 1.9);
  rightSocket.scale.set(1.1, 1.0, 0.6);
  eyeGroup.add(rightSocket);

  const eyeGeometry = new THREE.SphereGeometry(0.3, 12, 12);

  const leftEyeMaterial = new THREE.MeshBasicMaterial({
    color: fluorescentColors[params.eyeGlowColor], transparent: true, opacity: 0
  });
  const leftEye = new THREE.Mesh(eyeGeometry, leftEyeMaterial);
  leftEye.position.set(-0.7, 0.6, 2.0);
  eyeGroup.add(leftEye);

  const rightEyeMaterial = new THREE.MeshBasicMaterial({
    color: fluorescentColors[params.eyeGlowColor], transparent: true, opacity: 0
  });
  const rightEye = new THREE.Mesh(eyeGeometry, rightEyeMaterial);
  rightEye.position.set(0.7, 0.6, 2.0);
  eyeGroup.add(rightEye);

  const outerGlowGeometry = new THREE.SphereGeometry(0.525, 12, 12);

  const leftOuterGlowMaterial = new THREE.MeshBasicMaterial({
    color: fluorescentColors[params.eyeGlowColor], transparent: true, opacity: 0, side: THREE.BackSide
  });
  const leftOuterGlow = new THREE.Mesh(outerGlowGeometry, leftOuterGlowMaterial);
  leftOuterGlow.position.set(-0.7, 0.6, 1.95);
  eyeGroup.add(leftOuterGlow);

  const rightOuterGlowMaterial = new THREE.MeshBasicMaterial({
    color: fluorescentColors[params.eyeGlowColor], transparent: true, opacity: 0, side: THREE.BackSide
  });
  const rightOuterGlow = new THREE.Mesh(outerGlowGeometry, rightOuterGlowMaterial);
  rightOuterGlow.position.set(0.7, 0.6, 1.95);
  eyeGroup.add(rightOuterGlow);

  return { leftEye, rightEye, leftEyeMaterial, rightEyeMaterial, leftOuterGlow, rightOuterGlow, leftOuterGlowMaterial, rightOuterGlowMaterial };
}

const eyes = createEyes();

// Fireflies
const fireflies = [];
const fireflyGroup = new THREE.Group();
scene.add(fireflyGroup);

function createFireflies() {
  for (let i = 0; i < 20; i++) {
    const fireflyGeometry = new THREE.SphereGeometry(0.02, 2, 2);
    const fireflyMaterial = new THREE.MeshBasicMaterial({ color: 0xffff44, transparent: true, opacity: 0.9 });
    const firefly = new THREE.Mesh(fireflyGeometry, fireflyMaterial);

    firefly.position.set((Math.random() - 0.5) * 40, (Math.random() - 0.5) * 30, (Math.random() - 0.5) * 20);

    const glowGeometry = new THREE.SphereGeometry(0.08, 8, 8);
    const glowMaterial = new THREE.MeshBasicMaterial({ color: 0xffff88, transparent: true, opacity: 0.4, side: THREE.BackSide });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    firefly.add(glow);

    const fireflyLight = new THREE.PointLight(0xffff44, 0.8, 3, 2);
    firefly.add(fireflyLight);

    firefly.userData = {
      velocity: new THREE.Vector3((Math.random() - 0.5) * params.fireflySpeed, (Math.random() - 0.5) * params.fireflySpeed, (Math.random() - 0.5) * params.fireflySpeed),
      basePosition: firefly.position.clone(),
      phase: Math.random() * Math.PI * 2,
      pulseSpeed: 2 + Math.random() * 3,
      glow, glowMaterial, fireflyMaterial, light: fireflyLight
    };

    fireflyGroup.add(firefly);
    fireflies.push(firefly);
  }
}
createFireflies();

// Particles
const particles = [];
const particleGroup = new THREE.Group();
scene.add(particleGroup);

const particlePool = [];
const particleGeometries = [
  new THREE.SphereGeometry(0.05, 6, 6),
  new THREE.TetrahedronGeometry(0.04, 0),
  new THREE.OctahedronGeometry(0.045, 0)
];

const particleBaseMaterial = new THREE.MeshBasicMaterial({
  color: fluorescentColors[params.particleColor], transparent: true, opacity: 0, alphaTest: 0.1
});

function initParticlePool(count) {
  for (let i = 0; i < count; i++) {
    const geomIndex = Math.floor(Math.random() * particleGeometries.length);
    const material = particleBaseMaterial.clone();
    const particle = new THREE.Mesh(particleGeometries[geomIndex], material);
    particle.visible = false;
    particleGroup.add(particle);
    particlePool.push(particle);
  }
}
initParticlePool(100);

function createParticle() {
  let particle;
  if (particlePool.length > 0) {
    particle = particlePool.pop();
    particle.visible = true;
  } else if (particles.length < params.particleCount) {
    const geomIndex = Math.floor(Math.random() * particleGeometries.length);
    const material = particleBaseMaterial.clone();
    particle = new THREE.Mesh(particleGeometries[geomIndex], material);
    particleGroup.add(particle);
  } else {
    return null;
  }

  const particleColor = new THREE.Color(fluorescentColors[params.particleColor]);
  particleColor.offsetHSL(Math.random() * 0.1 - 0.05, 0, 0);
  particle.material.color = particleColor;

  particle.position.copy(ghostGroup.position);
  particle.position.z -= 0.8 + Math.random() * 0.6;
  particle.position.x += (Math.random() - 0.5) * 3.5;
  particle.position.y += (Math.random() - 0.5) * 3.5 - 0.8;

  const s = 0.6 + Math.random() * 0.7;
  particle.scale.set(s, s, s);
  particle.rotation.set(Math.random() * Math.PI * 2, Math.random() * Math.PI * 2, Math.random() * Math.PI * 2);

  particle.userData.life = 1.0;
  particle.userData.decay = Math.random() * 0.003 + params.particleDecayRate;
  particle.userData.rotationSpeed = { x: (Math.random() - 0.5) * 0.015, y: (Math.random() - 0.5) * 0.015, z: (Math.random() - 0.5) * 0.015 };
  particle.userData.velocity = { x: (Math.random() - 0.5) * 0.012, y: (Math.random() - 0.5) * 0.012 - 0.002, z: (Math.random() - 0.5) * 0.012 - 0.006 };
  particle.material.opacity = Math.random() * 0.9;
  particles.push(particle);
  return particle;
}

// ═══════════════════════════════════════════
// ANIMUS HUD — Custom Wrapper + Tweakpane
// ═══════════════════════════════════════════

const hudContainer = document.createElement('div');
hudContainer.id = 'animus-hud';
hudContainer.innerHTML = `
  <div class="hud-scan-line"></div>
  <div class="hud-corner hud-tl"></div>
  <div class="hud-corner hud-tr"></div>
  <div class="hud-corner hud-bl"></div>
  <div class="hud-corner hud-br"></div>
  <div class="hud-header" id="hud-toggle">
    <div class="hud-header-left">
      <div class="hud-status-dot"></div>
      <span class="hud-label">ANIMUS</span>
      <span class="hud-version">2.1</span>
    </div>
    <div class="hud-header-right">
      <span class="hud-sync">SYNC</span>
      <span class="hud-sync-pct">100%</span>
      <span class="hud-chevron">▾</span>
    </div>
  </div>
  <div class="hud-body">
    <div class="hud-subheader">
      <span class="hud-creed">NOTHING IS TRUE — EVERYTHING IS PERMITTED</span>
    </div>
    <div class="hud-dna-strip">
      <svg viewBox="0 0 200 8" preserveAspectRatio="none">
        <path d="M0,4 Q10,0 20,4 Q30,8 40,4 Q50,0 60,4 Q70,8 80,4 Q90,0 100,4 Q110,8 120,4 Q130,0 140,4 Q150,8 160,4 Q170,0 180,4 Q190,8 200,4" 
              fill="none" stroke="rgba(196,164,105,0.3)" stroke-width="1"/>
        <path d="M0,4 Q10,8 20,4 Q30,0 40,4 Q50,8 60,4 Q70,0 80,4 Q90,8 100,4 Q110,0 120,4 Q130,8 140,4 Q150,0 160,4 Q170,8 180,4 Q190,0 200,4" 
              fill="none" stroke="rgba(196,164,105,0.15)" stroke-width="1"/>
      </svg>
    </div>
    <div id="pane-mount"></div>
    <div class="hud-footer">
      <span class="hud-footer-left">MEM.SEQ ◆ ACTIVE</span>
      <span class="hud-footer-right">▸ DESMOND.2026</span>
    </div>
  </div>
`;
document.body.appendChild(hudContainer);

// Collapse/expand toggle — starts collapsed
hudContainer.classList.add('collapsed');
const hudToggle = document.getElementById('hud-toggle');
const hudChevron = hudContainer.querySelector('.hud-chevron');
hudToggle.addEventListener('click', () => {
  hudContainer.classList.toggle('collapsed');
  hudChevron.textContent = hudContainer.classList.contains('collapsed') ? '▸' : '▾';
});

// Mount Tweakpane inside HUD
const pane = new Pane({ title: "", expanded: true, container: document.getElementById('pane-mount') });
pane.element.classList.add('ac-pane');

const colorOptions = { Cyan: "cyan", Lime: "lime", Magenta: "magenta", Yellow: "yellow", Orange: "orange", Pink: "pink", Purple: "purple", Blue: "blue", Green: "green", Red: "red", Teal: "teal", Violet: "violet" };

// Folders with AC-style names
const glowFolder = pane.addFolder({ title: "◈ OPTICS", expanded: false });
glowFolder.addBinding(params, "glowColor", { label: "Spectrum", options: colorOptions }).on("change", (ev) => { ghostMaterial.emissive.set(fluorescentColors[ev.value]); });
glowFolder.addBinding(params, "emissiveIntensity", { label: "Luminance", min: 1, max: 10, step: 0.1 }).on("change", (ev) => { ghostMaterial.emissiveIntensity = ev.value; });

const eyeFolder = pane.addFolder({ title: "◈ IRIS PROTOCOL", expanded: false });
eyeFolder.addBinding(params, "eyeGlowColor", { label: "Iris Color", options: colorOptions }).on("change", (ev) => {
  const c = fluorescentColors[ev.value]; eyes.leftEyeMaterial.color.set(c); eyes.rightEyeMaterial.color.set(c); eyes.leftOuterGlowMaterial.color.set(c); eyes.rightOuterGlowMaterial.color.set(c);
});
eyeFolder.addBinding(params, "eyeGlowDecay", { label: "Decay", min: 0.9, max: 0.99, step: 0.01 });
eyeFolder.addBinding(params, "eyeGlowResponse", { label: "Response", min: 0.05, max: 0.5, step: 0.01 });
eyeFolder.addBinding(params, "movementThreshold", { label: "Threshold", min: 0.01, max: 0.1, step: 0.01 });

const revealFolder = pane.addFolder({ title: "◈ FIELD DEPTH", expanded: false });
revealFolder.addBinding(params, "revealRadius", { label: "Radius", min: 5, max: 100, step: 2 }).on("change", (ev) => { atmosphereMaterial.uniforms.revealRadius.value = ev.value; });
revealFolder.addBinding(params, "fadeStrength", { label: "Fade", min: 0.1, max: 3, step: 0.1 }).on("change", (ev) => { atmosphereMaterial.uniforms.fadeStrength.value = ev.value; });
revealFolder.addBinding(params, "baseOpacity", { label: "Darkness", min: 0, max: 1, step: 0.05 }).on("change", (ev) => { atmosphereMaterial.uniforms.baseOpacity.value = ev.value; });
revealFolder.addBinding(params, "revealOpacity", { label: "Exposure", min: 0, max: 0.5, step: 0.01 }).on("change", (ev) => { atmosphereMaterial.uniforms.revealOpacity.value = ev.value; });

const firefliesFolder = pane.addFolder({ title: "◈ LUMINARIES", expanded: false });
firefliesFolder.addBinding(params, "fireflyGlowIntensity", { label: "Intensity", min: 0, max: 5, step: 0.1 }).on("change", (ev) => {
  fireflies.forEach((f) => { f.userData.glowMaterial.opacity = ev.value * 0.4; f.userData.fireflyMaterial.opacity = ev.value * 0.9; f.userData.light.intensity = ev.value * 0.8; });
});
firefliesFolder.addBinding(params, "fireflySpeed", { label: "Drift", min: 0.005, max: 0.1, step: 0.005 });

const analogFolder = pane.addFolder({ title: "◈ SIGNAL DECAY", expanded: false });
analogFolder.addBinding(params, "limboMode", { label: "Limbo" }).on("change", (ev) => { analogDecayPass.uniforms.uLimboMode.value = ev.value ? 1.0 : 0.0; });
analogFolder.addBinding(params, "analogIntensity", { label: "Intensity", min: 0, max: 2, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogIntensity.value = ev.value; });
analogFolder.addBinding(params, "analogGrain", { label: "Grain", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogGrain.value = ev.value; });
analogFolder.addBinding(params, "analogBleeding", { label: "Bleed", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogBleeding.value = ev.value; });
analogFolder.addBinding(params, "analogVSync", { label: "V-Sync", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogVSync.value = ev.value; });
analogFolder.addBinding(params, "analogScanlines", { label: "Scanlines", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogScanlines.value = ev.value; });
analogFolder.addBinding(params, "analogVignette", { label: "Vignette", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogVignette.value = ev.value; });
analogFolder.addBinding(params, "analogJitter", { label: "Jitter", min: 0, max: 3, step: 0.1 }).on("change", (ev) => { analogDecayPass.uniforms.uAnalogJitter.value = ev.value; });

const behaviorFolder = pane.addFolder({ title: "◈ LOCOMOTION", expanded: false });
behaviorFolder.addBinding(params, "followSpeed", { label: "Tracking", min: 0.01, max: 0.2, step: 0.005 });
behaviorFolder.addBinding(params, "wobbleAmount", { label: "Wobble", min: 0, max: 1, step: 0.05 });

const particlesFolder = pane.addFolder({ title: "◈ PARTICLE FIELD", expanded: false });
particlesFolder.addBinding(params, "particleColor", { label: "Hue", options: colorOptions }).on("change", (ev) => { particleBaseMaterial.color.set(fluorescentColors[ev.value]); });
particlesFolder.addBinding(params, "createParticlesOnlyWhenMoving", { label: "Motion Only" });
particlesFolder.addBinding(params, "particleCount", { label: "Density", min: 50, max: 400, step: 10 });

// Resize
let resizeTimeout;
window.addEventListener("resize", () => {
  if (resizeTimeout) clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    bloomPass.setSize(window.innerWidth, window.innerHeight);
    analogDecayPass.uniforms.uResolution.value.set(window.innerWidth, window.innerHeight);
  }, 250);
});

// Mouse
const mouse = new THREE.Vector2();
const prevMouse = new THREE.Vector2();
const mouseSpeed = new THREE.Vector2();
let lastMouseUpdate = 0;
let isMouseMoving = false;
let mouseMovementTimer = null;

window.addEventListener("mousemove", (e) => {
  const now = performance.now();
  if (now - lastMouseUpdate > 16) {
    prevMouse.x = mouse.x; prevMouse.y = mouse.y;
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    mouseSpeed.x = mouse.x - prevMouse.x;
    mouseSpeed.y = mouse.y - prevMouse.y;
    isMouseMoving = true;
    if (mouseMovementTimer) clearTimeout(mouseMovementTimer);
    mouseMovementTimer = setTimeout(() => { isMouseMoving = false; }, 80);
    lastMouseUpdate = now;
  }
});

// Animation
let lastParticleTime = 0;
let time = 0;
let currentMovement = 0;
let lastFrameTime = 0;
let isInitialized = false;
let frameCount = 0;

function forceInitialRender() {
  for (let i = 0; i < 3; i++) composer.render();
  for (let i = 0; i < 10; i++) createParticle();
  composer.render();
  isInitialized = true;
  preloader.complete(renderer.domElement);
}

preloader.updateProgress(5);
setTimeout(forceInitialRender, 100);

function animate(timestamp) {
  requestAnimationFrame(animate);
  if (!isInitialized) return;

  const deltaTime = timestamp - lastFrameTime;
  lastFrameTime = timestamp;
  if (deltaTime > 100) return;

  const timeIncrement = (deltaTime / 16.67) * 0.01;
  time += timeIncrement;
  frameCount++;

  atmosphereMaterial.uniforms.time.value = time;
  analogDecayPass.uniforms.uTime.value = time;
  analogDecayPass.uniforms.uLimboMode.value = params.limboMode ? 1.0 : 0.0;

  // Ghost movement
  const targetX = mouse.x * 11;
  const targetY = mouse.y * 7;
  const prevGhostPosition = ghostGroup.position.clone();

  ghostGroup.position.x += (targetX - ghostGroup.position.x) * params.followSpeed;
  ghostGroup.position.y += (targetY - ghostGroup.position.y) * params.followSpeed;

  atmosphereMaterial.uniforms.ghostPosition.value.copy(ghostGroup.position);

  const movementAmount = prevGhostPosition.distanceTo(ghostGroup.position);
  currentMovement = currentMovement * params.eyeGlowDecay + movementAmount * (1 - params.eyeGlowDecay);

  // Float
  ghostGroup.position.y += Math.sin(time * params.floatSpeed * 1.5) * 0.03 + Math.cos(time * params.floatSpeed * 0.7) * 0.018 + Math.sin(time * params.floatSpeed * 2.3) * 0.008;

  // Pulse
  const pulse1 = Math.sin(time * params.pulseSpeed) * params.pulseIntensity;
  const breathe = Math.sin(time * 0.6) * 0.12;
  ghostMaterial.emissiveIntensity = params.emissiveIntensity + pulse1 + breathe;

  // Fireflies
  fireflies.forEach((firefly) => {
    const ud = firefly.userData;
    const pulse = Math.sin(time + ud.phase * ud.pulseSpeed) * 0.4 + 0.6;
    ud.glowMaterial.opacity = params.fireflyGlowIntensity * 0.4 * pulse;
    ud.fireflyMaterial.opacity = params.fireflyGlowIntensity * 0.9 * pulse;
    ud.light.intensity = params.fireflyGlowIntensity * 0.8 * pulse;
    ud.velocity.x += (Math.random() - 0.5) * 0.001;
    ud.velocity.y += (Math.random() - 0.5) * 0.001;
    ud.velocity.z += (Math.random() - 0.5) * 0.001;
    ud.velocity.clampLength(0, params.fireflySpeed);
    firefly.position.add(ud.velocity);
    if (Math.abs(firefly.position.x) > 30) ud.velocity.x *= -0.5;
    if (Math.abs(firefly.position.y) > 20) ud.velocity.y *= -0.5;
    if (Math.abs(firefly.position.z) > 15) ud.velocity.z *= -0.5;
  });

  // Body animations
  const mouseDir = new THREE.Vector2(targetX - ghostGroup.position.x, targetY - ghostGroup.position.y).normalize();
  const tiltS = 0.1 * params.wobbleAmount;
  const tiltD = 0.95;
  ghostBody.rotation.z = ghostBody.rotation.z * tiltD + -mouseDir.x * tiltS * (1 - tiltD);
  ghostBody.rotation.x = ghostBody.rotation.x * tiltD + mouseDir.y * tiltS * (1 - tiltD);
  ghostBody.rotation.y = Math.sin(time * 1.4) * 0.05 * params.wobbleAmount;

  const scaleVar = 1 + Math.sin(time * 2.1) * 0.025 * params.wobbleAmount + pulse1 * 0.015;
  const scaleBreath = 1 + Math.sin(time * 0.8) * 0.012;
  const fs = scaleVar * scaleBreath;
  ghostBody.scale.set(fs, fs, fs);

  // Eye glow
  const normalizedMouseSpeed = Math.sqrt(mouseSpeed.x * mouseSpeed.x + mouseSpeed.y * mouseSpeed.y) * 8;
  const isMoving = currentMovement > params.movementThreshold;
  const targetGlow = isMoving ? 1.0 : 0.0;
  const glowChangeSpeed = isMoving ? params.eyeGlowResponse * 2 : params.eyeGlowResponse;
  const newOpacity = eyes.leftEyeMaterial.opacity + (targetGlow - eyes.leftEyeMaterial.opacity) * glowChangeSpeed;
  eyes.leftEyeMaterial.opacity = newOpacity;
  eyes.rightEyeMaterial.opacity = newOpacity;
  eyes.leftOuterGlowMaterial.opacity = newOpacity * 0.3;
  eyes.rightOuterGlowMaterial.opacity = newOpacity * 0.3;

  // Particles
  const shouldCreateParticles = params.createParticlesOnlyWhenMoving
    ? currentMovement > 0.005 && isMouseMoving
    : currentMovement > 0.005;

  if (shouldCreateParticles && timestamp - lastParticleTime > 100) {
    const speedRate = Math.floor(normalizedMouseSpeed * 3);
    const particleRate = Math.min(params.particleCreationRate, Math.max(1, speedRate));
    for (let i = 0; i < particleRate; i++) createParticle();
    lastParticleTime = timestamp;
  }

  const particlesToUpdate = Math.min(particles.length, 60);
  for (let i = 0; i < particlesToUpdate; i++) {
    const index = (frameCount + i) % particles.length;
    if (index < particles.length) {
      const p = particles[index];
      p.userData.life -= p.userData.decay;
      p.material.opacity = p.userData.life * 0.85;
      if (p.userData.velocity) {
        p.position.x += p.userData.velocity.x;
        p.position.y += p.userData.velocity.y;
        p.position.z += p.userData.velocity.z;
        p.position.x += Math.cos(time * 1.8 + p.position.y) * 0.0008;
      }
      if (p.userData.rotationSpeed) {
        p.rotation.x += p.userData.rotationSpeed.x;
        p.rotation.y += p.userData.rotationSpeed.y;
        p.rotation.z += p.userData.rotationSpeed.z;
      }
      if (p.userData.life <= 0) {
        p.visible = false;
        p.material.opacity = 0;
        particlePool.push(p);
        particles.splice(index, 1);
        i--;
      }
    }
  }

  composer.render();
}

// Init
const fakeEvent = new MouseEvent("mousemove", { clientX: window.innerWidth / 2, clientY: window.innerHeight / 2 });
window.dispatchEvent(fakeEvent);

animate(0);

// ═══════════════════════════════════════════
// Rotating Hero Text — every 30 seconds
// ═══════════════════════════════════════════
const heroQuotes = [
  { lines: ["Wolves Don't Kneel", "Crows Don't Mourn", "Kings Don't Last"], sub: "Whispers through memory" },
  { lines: ["Fire Made Flesh", "Crown of Ashes", "The Long Night"], sub: "Echoes of the fallen" },
  { lines: ["Steel and Stone", "Bone and Blood", "Ash and Echo"], sub: "Remnants of the realm" },
  { lines: ["All Men Die", "Few Men Live", "None Forget"], sub: "The old gods remember" },
  { lines: ["Vows Break", "Houses Burn", "Night Takes All"], sub: "Winter came for everyone" },
  { lines: ["Throne of Bones", "Oath of Flame", "Night Without End"], sub: "A song of ice and fire" },
];

let currentQuoteIndex = 0;
const quoteEl = document.querySelector('.quote');
const authorEl = document.querySelector('.author');

function rotateQuote() {
  currentQuoteIndex = (currentQuoteIndex + 1) % heroQuotes.length;
  const next = heroQuotes[currentQuoteIndex];

  // Fade out
  quoteEl.style.transition = 'opacity 0.8s ease';
  authorEl.style.transition = 'opacity 0.8s ease';
  quoteEl.style.opacity = '0';
  authorEl.style.opacity = '0';

  setTimeout(() => {
    quoteEl.innerHTML = next.lines.join('<br />');
    authorEl.textContent = next.sub;
    quoteEl.style.opacity = '1';
    authorEl.style.opacity = '0.7';
  }, 800);
}

setInterval(rotateQuote, 30000);
