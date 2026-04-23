# Sharpz Analytics — Landing Design

> Código del diseño de la landing actual (`sharpzanalytics.com`, hosted en Netlify).
> Es una SPA estática de 2 páginas: home + login de operador. Stack: HTML + CSS vanilla + Three.js para el hero 3D.
>
> **Design language:** dark mode, quiet authority, Space Grotesk + JetBrains Mono, tonos grises escalonados, acentos blanco-off (#e0e0e0), hero con visualización 3D de grafo rotativo.

---

## Archivo 1/2 · `index.html` (home)

Paleta de colores:
- Background: `#0a0a0a`
- Foreground: `#ffffff`
- Grays: `#1a1a1a` / `#2a2a2a` / `#3a3a3a` / `#666666` / `#999999`
- Accent: `#e0e0e0`

Fuentes:
- `Space Grotesk` (UI/display, weights 300-700)
- `JetBrains Mono` (tags, IDs, meta labels)

Secciones del layout:
1. **Hero** — título gradiente + Three.js 3D graph de fondo + 3 CTAs (Request a test / Explore / Operator login)
2. **01 / Services** — grid de 3 cards (Public Opinion / Market Reaction / Crisis Analysis)
3. **02 / How it works** — 4 steps numerados (Seed Document → Agent Generation → Simulation → Predictive Report) + row de 4 stats
4. **03 / Contact** — form + info sidebar con intake CTA
5. **Footer** — copyright

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sharpz Analytics — Predictive Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --bg: #0a0a0a;
  --fg: #ffffff;
  --gray-1: #1a1a1a;
  --gray-2: #2a2a2a;
  --gray-3: #3a3a3a;
  --gray-4: #666666;
  --gray-5: #999999;
  --accent: #e0e0e0;
}

html { scroll-behavior: smooth; }

body {
  font-family: 'Space Grotesk', sans-serif;
  background: var(--bg);
  color: var(--fg);
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

/* ═══ HERO ═══ */
#hero {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

#three-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  pointer-events: none;
}

.hero-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--gray-5);
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: clamp(2.5rem, 7vw, 5.5rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
  margin-bottom: 1.5rem;
  background: linear-gradient(180deg, #ffffff 0%, #888888 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: clamp(1rem, 2vw, 1.3rem);
  font-weight: 300;
  color: var(--gray-5);
  max-width: 600px;
  margin: 0 auto 2.5rem;
  line-height: 1.6;
}

.hero-cta {
  pointer-events: all;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.9rem 2rem;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  color: var(--fg);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  text-decoration: none;
  border-radius: 50px;
  transition: all 0.3s ease;
  cursor: pointer;
  backdrop-filter: blur(10px);
}

.hero-cta-primary {
  background: #ffffff;
  border-color: #ffffff;
  color: #0a0a0a;
  font-weight: 600;
}
.hero-cta-primary:hover {
  background: #e0e0e0;
  border-color: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.12);
}

.hero-cta-operator {
  opacity: 0.5;
  font-size: 13px;
  padding: 10px 20px;
  border-style: dashed;
}
.hero-cta-operator:hover {
  opacity: 1;
  border-style: solid;
}
.hero-cta-group {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-cta:hover {
  background: rgba(255,255,255,0.15);
  border-color: rgba(255,255,255,0.3);
  transform: translateY(-2px);
}

#hero::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 35%;
  background: linear-gradient(to bottom, transparent 0%, var(--bg) 100%);
  z-index: 1;
  pointer-events: none;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  animation: float 2s ease-in-out infinite;
}

.scroll-indicator span {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gray-4);
}

.scroll-indicator .arrow {
  width: 1px;
  height: 30px;
  background: linear-gradient(to bottom, var(--gray-4), transparent);
}

@keyframes float {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* ═══ SECTIONS ═══ */
section {
  padding: 8rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--gray-4);
  margin-bottom: 1rem;
}

.section-title {
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
  background: linear-gradient(180deg, #ffffff 0%, #aaaaaa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-desc {
  font-size: 1.1rem;
  color: var(--gray-5);
  max-width: 600px;
  line-height: 1.7;
  margin-bottom: 3rem;
}

/* ═══ SERVICES ═══ */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.service-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  opacity: 0;
  transition: opacity 0.4s;
}

.service-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.12);
  transform: translateY(-4px);
}

.service-card:hover::before { opacity: 1; }

.service-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.service-card h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.service-card p {
  font-size: 0.95rem;
  color: var(--gray-5);
  line-height: 1.6;
}

/* ═══ PROCESS ═══ */
#demo { border-top: 1px solid var(--gray-2); }

.process-steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-top: 1rem;
}

.step {
  text-align: center;
  padding: 2rem 1rem;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--gray-3);
  margin-bottom: 1rem;
}

.step-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.step-desc {
  font-size: 0.85rem;
  color: var(--gray-5);
  line-height: 1.5;
}

.step-connector {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gray-3);
  font-size: 1.5rem;
}

/* ═══ STATS ═══ */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  margin-top: 4rem;
  padding-top: 4rem;
  border-top: 1px solid var(--gray-2);
}

.stat { text-align: center; }

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(180deg, #ffffff 0%, #888888 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 0.8rem;
  color: var(--gray-5);
  margin-top: 0.3rem;
  letter-spacing: 0.05em;
}

/* ═══ CONTACT ═══ */
#contact { border-top: 1px solid var(--gray-2); }

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
}

.contact-form { display: flex; flex-direction: column; gap: 1rem; }

.contact-form input,
.contact-form textarea {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  padding: 1rem 1.2rem;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem;
  color: var(--fg);
  outline: none;
  transition: border-color 0.3s;
}

.contact-form input:focus,
.contact-form textarea:focus {
  border-color: rgba(255,255,255,0.25);
}

.contact-form textarea { min-height: 120px; resize: vertical; }

.contact-form input::placeholder,
.contact-form textarea::placeholder { color: var(--gray-4); }

.submit-btn {
  align-self: flex-start;
  padding: 0.9rem 2.5rem;
  background: var(--fg);
  color: var(--bg);
  border: none;
  border-radius: 50px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255,255,255,0.15);
}

.contact-info h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.contact-info p {
  color: var(--gray-5);
  line-height: 1.7;
  margin-bottom: 2rem;
}

.contact-links { display: flex; flex-direction: column; gap: 0.8rem; }

.contact-links a {
  color: var(--gray-5);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  transition: color 0.3s;
}

.contact-links a:hover { color: var(--fg); }

.contact-intake-cta {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--gray-2);
}
.contact-intake-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--gray-5);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  margin: 0 0 0.9rem 0 !important;
}
.contact-intake-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.85rem 1.6rem;
  background: var(--fg);
  color: var(--bg);
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.25s;
}
.contact-intake-btn:hover {
  background: var(--gray-5);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.08);
}

/* ═══ FOOTER ═══ */
footer {
  padding: 3rem 2rem;
  text-align: center;
  border-top: 1px solid var(--gray-2);
}

footer p {
  font-size: 0.8rem;
  color: var(--gray-4);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══ RESPONSIVE ═══ */
@media (max-width: 768px) {
  .process-steps { grid-template-columns: repeat(2, 1fr); }
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .contact-grid { grid-template-columns: 1fr; gap: 2rem; }
  .step-connector { display: none; }
  .hero-cta-group { flex-direction: column; align-items: center; }
}

@media (max-width: 480px) {
  .process-steps { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: 1fr; }
  section { padding: 4rem 1.5rem; }
}

/* ═══ ANIMATIONS ═══ */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
</head>
<body>

<!-- ═══ HERO ═══ -->
<div id="hero">
  <canvas id="three-canvas"></canvas>
  <div class="hero-content">
    <div class="hero-tag">Predictive Intelligence Platform</div>
    <h1 class="hero-title">SHARPZ<br>ANALYTICS</h1>
    <p class="hero-subtitle">We simulate scenarios with thousands of autonomous human-like agents to predict how society will react.</p>
    <div class="hero-cta-group">
      <a href="https://intake.sharpzanalytics.com/intake" class="hero-cta hero-cta-primary">Request a test &rarr;</a>
      <a href="#services" class="hero-cta">Explore &darr;</a>
      <a href="/login/" class="hero-cta hero-cta-operator" title="Operator / admin login">Operator login</a>
    </div>
  </div>
  <div class="scroll-indicator">
    <span>Scroll</span>
    <div class="arrow"></div>
  </div>
</div>

<!-- ═══ SERVICES ═══ -->
<section id="services">
  <div class="section-tag">01 / Services</div>
  <h2 class="section-title">Predictive intelligence<br>for real decisions</h2>
  <p class="section-desc">We use multi-agent simulation to anticipate what others only analyze after the fact.</p>

  <div class="services-grid">
    <div class="service-card fade-in">
      <div class="service-icon">&#9673;</div>
      <h3>Public Opinion Simulation</h3>
      <p>We generate thousands of autonomous agents with real personalities, alliances and motivations. We let them interact and observe which narratives emerge, which coalitions form, and how public sentiment evolves hour by hour.</p>
    </div>
    <div class="service-card fade-in">
      <div class="service-icon">&#9651;</div>
      <h3>Market Reaction Forecasting</h3>
      <p>Simulated agents representing investors, analysts and institutions react to policy changes, announcements and crises — revealing how markets and financial sentiment are likely to shift.</p>
    </div>
    <div class="service-card fade-in">
      <div class="service-icon">&#9888;</div>
      <h3>Crisis Analysis</h3>
      <p>We simulate crisis scenarios before they happen: scandals, regulatory changes, controversial announcements. We identify inflection points, key actors and windows of opportunity for strategic response.</p>
    </div>
  </div>
</section>

<!-- ═══ DEMO / PROCESS ═══ -->
<section id="demo">
  <div class="section-tag">02 / How it works</div>
  <h2 class="section-title">From a document<br>to a prediction</h2>
  <p class="section-desc">Four steps. One scenario. Thousands of simulated interactions. One actionable report.</p>

  <div class="process-steps">
    <div class="step fade-in">
      <div class="step-num">01</div>
      <div class="step-title">Seed Document</div>
      <div class="step-desc">You share the scenario: an announcement, a crisis, a public policy. We turn it into the simulation seed.</div>
    </div>
    <div class="step fade-in">
      <div class="step-num">02</div>
      <div class="step-title">Agent Generation</div>
      <div class="step-desc">We create dozens of autonomous agents with personalities, alliances and behaviors based on real-world actors.</div>
    </div>
    <div class="step fade-in">
      <div class="step-num">03</div>
      <div class="step-title">Simulation</div>
      <div class="step-desc">Agents interact on simulated social networks for hours or days. We observe what emerges without directing the outcome.</div>
    </div>
    <div class="step fade-in">
      <div class="step-num">04</div>
      <div class="step-title">Predictive Report</div>
      <div class="step-desc">We deliver a detailed analysis: dominant narratives, coalitions, inflection points and 30-day projections.</div>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat fade-in">
      <div class="stat-value">2000+</div>
      <div class="stat-label">Agents per simulation</div>
    </div>
    <div class="stat fade-in">
      <div class="stat-value">480h</div>
      <div class="stat-label">Real-time simulation</div>
    </div>
    <div class="stat fade-in">
      <div class="stat-value">400+</div>
      <div class="stat-label">Interactions per run</div>
    </div>
    <div class="stat fade-in">
      <div class="stat-value">+90d</div>
      <div class="stat-label">Scenario projection</div>
    </div>
  </div>
</section>

<!-- ═══ CONTACT ═══ -->
<section id="contact">
  <div class="section-tag">03 / Contact</div>
  <h2 class="section-title">Let's talk about<br>your scenario</h2>

  <div class="contact-grid">
    <form class="contact-form fade-in" onsubmit="event.preventDefault(); alert('Message sent. We will get back to you soon.');">
      <input type="text" placeholder="Name" required>
      <input type="email" placeholder="Email" required>
      <textarea placeholder="Tell us what scenario you want to simulate..."></textarea>
      <button type="submit" class="submit-btn">Send</button>
    </form>
    <div class="contact-info fade-in">
      <h3>Sharpz Analytics</h3>
      <p>Predictive intelligence platform powered by multi-agent simulation. Based in Buenos Aires, serving clients across Latin America.</p>
      <div class="contact-links">
        <a href="mailto:contacto@sharpzanalytics.com">contacto@sharpzanalytics.com</a>
        <a href="#">linkedin.com/company/sharpz-analytics</a>
        <a href="#">Buenos Aires, Argentina</a>
      </div>
      <div class="contact-intake-cta">
        <p class="contact-intake-label">Know what you want to test?</p>
        <a href="https://intake.sharpzanalytics.com/intake" class="contact-intake-btn">Start a structured intake &rarr;</a>
      </div>
    </div>
  </div>
</section>

<!-- ═══ FOOTER ═══ -->
<footer>
  <p>&copy; 2026 Sharpz Analytics. All rights reserved.</p>
</footer>
```

### Three.js hero background (visualización de grafo 3D rotativo)

El hero usa Three.js para renderizar un grafo 3D con ~600 nodes + edges curvos. Los nodes se distribuyen en clusters sobre una esfera (golden spiral) + clusters internos + nodos dispersos. Los edges se conectan entre nodes cercanos con curvas bezier cuadráticas (algunos se curvan hacia adentro de la esfera, otros hacia afuera, otros lateralmente). Hay partículas ambientes de fondo para profundidad.

El grafo rota lento en Y, con wobble subtil en X. Parallax con mouse. Los nodes son "hubs" (más grandes) o secundarios (chicos). Edges con opacity variable según si conectan hubs o nodes normales.

Script simplificado del setup + animación:

```javascript
const canvas = document.getElementById('three-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x0a0a0a, 1);
camera.position.z = 55;

// Build ~600 nodes distributed in clusters on a sphere (golden spiral distribution)
// + inner clusters + loose scatter nodes for roundness
// Hub nodes (first 2 per cluster) are bigger

// Custom ShaderMaterial for nodes: circular point sprite with glow,
// brightness proportional to size

// Curved edges between nearby nodes with THREE.QuadraticBezierCurve3
// 35% curve inward (through sphere), 25% curve outward, 40% lateral

// Animation: slow Y rotation (0.0012 rad/frame) + subtle X wobble
// Mouse parallax on camera (x: ±6, y: ±4)
// Ambient dust particles counter-rotating slowly
```

---

## Archivo 2/2 · `login/index.html` (operator login)

Diseño minimal — una card centered con API key input. Mismo dark theme pero más contenido, sin Three.js.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Operator login · Sharpz Analytics</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  background: #0a0a0a;
  color: #ffffff;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-card {
  max-width: 420px;
  width: 100%;
  padding: 48px 36px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  background: #111111;
}

.brand-mark {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.2em;
  color: #888;
  text-transform: uppercase;
  margin-bottom: 8px;
}

h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 14px;
  color: #888;
  margin-bottom: 32px;
  line-height: 1.6;
}

label {
  display: block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #888;
  margin-bottom: 8px;
}

input[type="password"], input[type="text"] {
  width: 100%;
  padding: 14px 16px;
  background: #0a0a0a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  color: #ffffff;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  margin-bottom: 20px;
}

input:focus {
  outline: none;
  border-color: #ffffff;
}

button {
  width: 100%;
  padding: 14px 20px;
  background: #ffffff;
  color: #0a0a0a;
  border: none;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 255, 255, 0.15);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-msg {
  margin-top: 16px;
  padding: 12px 14px;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: 6px;
  color: #ff8a80;
  font-size: 13px;
  display: none;
}

.error-msg.visible { display: block; }

.back-link {
  display: inline-block;
  margin-top: 24px;
  color: #888;
  font-size: 12px;
  text-decoration: none;
}

.back-link:hover { color: #fff; }

.footer-note {
  margin-top: 28px;
  font-size: 11px;
  color: #555;
  line-height: 1.6;
}
</style>
</head>
<body>

<div class="login-card">
  <div class="brand-mark">Sharpz Analytics</div>
  <h1>Operator access</h1>
  <p class="subtitle">
    Ingresá tu API key para acceder al dashboard de control. Si no tenés
    una, pedila al admin.
  </p>

  <form id="login-form">
    <label for="api-key">API Key</label>
    <input
      id="api-key"
      type="password"
      placeholder="sk_..."
      autocomplete="off"
      required
    />
    <button type="submit" id="login-btn">Login &rarr;</button>
    <div id="error-msg" class="error-msg"></div>
  </form>

  <a href="/" class="back-link">&larr; Back to landing</a>

  <p class="footer-note">
    Client access is separate — clients receive their deliverable URL
    directly via email.
  </p>
</div>
</body>
</html>
```

---

## Resumen del design language (para V2 replicate o rethink)

**Ethos:** dark, quiet, "predictive intelligence" — no saturado, sin colores vibrantes. Authority-feel tipo Bloomberg terminal pero más minimal.

**Tipografía:**
- `Space Grotesk` para UI, títulos (weights 300 para body, 600-700 para display)
- `JetBrains Mono` para tags, IDs, meta labels, section numbers

**Paleta:**
- `#0a0a0a` canvas base
- `#ffffff` primary text
- Grays escalonados 1a → 2a → 3a → 666 → 999
- `#e0e0e0` accent (off-white, no colores de marca)

**Signature patterns:**
- Section headers numerados "01 / Services", "02 / How it works"
- Gradient text en títulos grandes (white → gray)
- Thin 1px borders en `rgba(255,255,255,0.08-0.15)`
- Cards con fondo `rgba(255,255,255,0.03-0.05)` (casi invisible, solo borde sutil)
- CTAs principal: white solid + black text, rounded 50px
- Fade-in scroll animations con `cubic-bezier(0.16, 1, 0.3, 1)`

**3D hero:** graph rotativo con Three.js — signature visual del brand.

**Responsive:** grids colapsan a 2 cols a 768px, a 1 col a 480px. Hero CTAs stack en mobile.
