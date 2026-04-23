# Sharpz · Deliverable al cliente · Diseño

Este documento cubre el **deliverable final** que recibe el cliente cuando termina un test: el paquete HTML (+ PDF) que concentra todo el valor del producto. Solo diseño — tokens, layout, componentes, templates, flujo de navegación. No tiene prescripciones técnicas de backend (cómo se genera, cómo se firma la URL, cómo se cachea, etc.): eso es decisión del equipo que implemente V2.

> **Pareja con los otros dos documentos:**
> - `sharpz_landing_design.md` — marketing público (dark, motion, Three.js).
> - `sharpz_intake_design.md` — consola operativa interna (dark, denso, formulario guiado).
> - `sharpz_deliverable_design.md` (este) — **el producto entregado al cliente** (light, serif, lento, autoritativo).

---

## 1. Qué es el deliverable

Cuando un test termina, Sharpz publica un **paquete multi-página** en una URL firmada (único link por deliverable). El cliente abre el link y encuentra una micrositio interno, con sidebar de navegación y 6–8 páginas de lectura larga. Cada página responde a una pregunta distinta del comprador:

| Sección | Pregunta del cliente | Obligatoria |
|---|---|---|
| **Executive Report** | "¿Cuál variante ganó y por qué?" | sí |
| **Audience** | "¿Contra quién testearon? ¿Era representativo?" | sí |
| **Variant A / B / C …** | "Mostrame cómo reaccionó cada variante en detalle." | sí (una por variante) |
| **Interviews** (Apéndice B) | "¿Qué dijeron los buyers clave sobre cada opción?" | sí |
| **Forecast** (opcional) | "¿Esto cuánto me vende?" (solo si el test_type lo amerita) | no |
| **Metrics** (Apéndice A) | "Dame la data cruda para auditar." | no (tiers altos) |
| **Methodology** (Apéndice D) | "¿Esto es serio? ¿Cómo lo hicieron?" | sí |
| **Download PDF** | "Lo llevo al board impreso." | sí |

Además, se entrega un **one-pager** (400–600 palabras) en la primera carga, visible sin scroll para el CEO que tiene 30 segundos.

La URL firmada está parametrizada por `deliverable_id` — típicamente: `https://app.sharpz.io/d/<deliverable_id>?token=<jwt>`. El cliente la abre sin login (el token es el login).

---

## 2. Design language — "quiet authority"

Inspiración declarada: **Financial Times × McKinsey Insights × Stratechery**. Tres principios que ordenan todas las decisiones:

1. **Reading-first.** El deliverable no es un dashboard. Es un *reporte para leer*. Serif en el body, ancho de lectura clásico (720px), line-height generoso (1.75). Nada de tarjetas de KPI gigantes ni numeritos en bold con gradient. Si hay un gráfico, es porque aporta — no porque hay que llenar espacio.
2. **Quiet authority.** Sin emojis, sin glass morphism, sin motion gratuito, sin colores saturados. Un único acento cálido (terracota) para el hilo de marca y los blockquotes; un único acento frío (azul profundo) para los links. Todo lo demás es paleta neutra tipo papel.
3. **Source integrity visible.** El cliente tiene que sentir que puede auditar. Quote integrity, confidence score, methodology explícita, raw JSON en `<details>`. La honestidad es parte del diseño: la seriedad se transmite mostrando los *límites*, no tapándolos.

**Contraste explícito con landing/intake:**

|  | Landing / Intake | Deliverable |
|---|---|---|
| Tema | oscuro (#0a0a0a) | claro (#FAF9F6 canvas, #FFFFFF paper) |
| Fuente de lectura | sans (Space Grotesk / Inter) | **serif (Source Serif 4)** |
| Densidad | alta, operativa | baja, lenta, respiratoria |
| Motion | sí (Three.js en landing) | prácticamente ninguno |
| Tono | operador / marketing | papel de banco de inversión |
| Breakpoint | responsive agresivo | optimizado para desktop + PDF |

---

## 3. Design tokens — `sharpz.css` (`:root` block)

```css
:root {
  /* -------- Colors -------- */
  --ink:             #0A0E27;   /* title/body color */
  --ink-soft:        #1F2441;   /* body prose */
  --canvas:          #FAF9F6;   /* page bg — warm paper, not pure white */
  --paper:           #FFFFFF;   /* sidebar / card bg */

  --accent-warm:     #B85C38;   /* terracotta — brand tag, blockquote rule */
  --accent-warm-soft:#E8CFC4;
  --accent-cool:     #1E40AF;   /* deep blue — links */
  --accent-cool-hover:#1E3A8A;

  --gray-100:        #F4F2ED;   /* callout bg */
  --gray-200:        #E5E1D8;   /* borders, rules */
  --gray-400:        #A8A29A;   /* nav labels */
  --gray-500:        #6B7280;   /* secondary text */
  --gray-700:        #374151;   /* strong secondary, table strong */

  /* -------- Typography --------
     Inter           — UI sans (sidebar, nav, tables)
     Source Serif 4  — body serif (article reading surface; Charter substitute)
     JetBrains Mono  — code / IDs
  */
  --font-ui:    "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-serif: "Source Serif 4", "Charter", "Iowan Old Style",
                "Palatino Linotype", "Hoefler Text", Georgia, serif;
  --font-mono:  "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;

  /* -------- Layout -------- */
  --sidebar-width:   280px;
  --reading-width:   720px;
  --content-padding: 48px;
}
```

**Por qué esos valores:**
- `#FAF9F6` canvas en lugar de blanco puro → simula papel, reduce fatiga visual en lecturas largas.
- `#B85C38` terracota como acento único → destaca blockquotes y brand tag sin gritar. Es el color emocional del deliverable.
- `#1E40AF` como link → lo suficientemente saturado para ser obvio, lo suficientemente serio para no parecer marketing.
- `720px` reading width → clásico de libros y reportes largos (60–80 char por línea).
- `280px` sidebar → cabe el nombre del cliente, metadata, nav completa y footer sin cortar.

---

## 4. Layout macro

```
┌────────────────────────────────────────────────────────────────┐
│  Sidebar fixed 280px               │   Main (fluid)            │
│  ──────────────────────────────    │   margin-left: 280px      │
│  [client logo opc.]                │   padding: 64px 48px 96px │
│  SHARPZ ANALYTICS (brand tag)      │   ┌──────────────────┐    │
│  Arcos Dorados (h1 big)            │   │ content max-w:   │    │
│                                    │   │ 720px            │    │
│  Test ID: test_a00e02…             │   │ centered         │    │
│  Tipo: pricing_test                │   │                  │    │
│  Generado: 21 Abr 2026             │   │ <cover>          │    │
│  Inversión: $23.40 USD             │   │ <article>        │    │
│                                    │   │ <callout>        │    │
│  ── CONTENIDO ──                   │   │ <blockquote>     │    │
│  › Executive Report        [ PDF ] │   │ ...              │    │
│    Audience                        │   │                  │    │
│    $9.900 ARS                      │   └──────────────────┘    │
│    $19.900 ARS                     │                           │
│    $29.900 ARS                     │                           │
│    Apéndice B · Entrevistas        │                           │
│    Apéndice D · Metodología        │                           │
│                                    │                           │
│  Confidencial · solo destinatario. │                           │
│  Sharpz Analytics — 21 Abr 2026    │                           │
└────────────────────────────────────────────────────────────────┘
```

- Sidebar es `position: fixed` y scrollea independiente si overflow.
- Main tiene `margin-left: 280px` (= sidebar width), content centrado a 720px.
- En móvil (<900px): sidebar colapsa a bloque estático arriba, main ocupa 100%.
- En print: sidebar desaparece, main ocupa toda la página, font-size baja a 11pt.

---

## 5. Templates Jinja2 — código completo

### 5.1 `base.html` — layout maestro

Todos los templates de deliverable extienden de éste. Es el que define el shell (sidebar + main), cabeza HTML, fuentes, e inyecta el branding del cliente por CSS variables.

```html
<!DOCTYPE html>
<html lang="{{ language|default('es') }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>{{ page_title|default(test.title) }} · Sharpz</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!--
    Inter         — UI sans (headers, sidebar, nav)
    Source Serif 4 — body serif (article/reading surface; substitute for Charter)
    JetBrains Mono — code/IDs
  -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="{{ static_url('sharpz.css') }}">

  {% if branding and branding.primary_color %}
  <style>
    :root {
      --sharpz-client-primary: {{ branding.primary_color }};
    }
    .sharpz-brand-tag             { color: var(--sharpz-client-primary); }
    .sharpz-nav-item a.active     { border-left-color: var(--sharpz-client-primary); }
    .sharpz-chip--winner          { background: var(--sharpz-client-primary); color: #fff; }
    a                             { color: var(--sharpz-client-primary); }
  </style>
  {% endif %}

  {% block head_extra %}{% endblock %}
</head>
<body class="sharpz-viewer">
  <div class="sharpz-layout">

    <aside class="sharpz-sidebar">
      {% if branding and branding.logo_url %}
      <img src="{{ branding.logo_url }}"
           alt="{{ deliverable.client_display_name or test.title }}"
           class="sharpz-client-logo">
      {% endif %}

      <span class="sharpz-brand-tag">Sharpz Analytics</span>
      <h1>{{ deliverable.client_display_name or test.title }}</h1>

      <div class="sharpz-meta">
        <strong>Test ID</strong>
        <code>{{ test.test_id }}</code>

        <strong>Tipo de test</strong>
        {{ test.test_type_display_name }}

        <strong>Generado</strong>
        {{ generated_at_display }}

        {% if test.total_cost_usd %}
        <strong>Inversión en compute</strong>
        ${{ "%.2f"|format(test.total_cost_usd) }} USD
        {% endif %}
      </div>

      <ul class="sharpz-nav">
        <li class="sharpz-nav-label">Contenido</li>
        {% for item in sidebar_items %}
        <li class="sharpz-nav-item">
          <a href="{{ item.url }}" {% if item.slug == current_slug %}class="active"{% endif %}>
            <span class="sharpz-nav-icon">{{ item.icon }}</span>
            {{ item.title }}
          </a>
          {% if item.pdf_url %}
          <a href="{{ item.pdf_url }}" class="sharpz-pdf-btn" download>↓ PDF</a>
          {% endif %}
        </li>
        {% endfor %}
      </ul>

      <div class="sharpz-sidebar-footer">
        Confidencial · solo para el destinatario.<br>
        Sharpz Analytics — {{ generated_at_display }}
      </div>
    </aside>

    <main class="sharpz-main">
      <div class="sharpz-content">
        {% block content %}{% endblock %}
      </div>
    </main>
  </div>
</body>
</html>
```

**Inyección de branding por cliente** — el backend puede pasar `branding.primary_color` (hex) y `branding.logo_url` en el contexto; el template los inyecta via CSS custom properties. Permite deliverables de Arcos Dorados con amarillo McDonald's, Boca con azul y oro, etc., sin cambiar el CSS base.

### 5.2 `executive.html` — reporte ejecutivo (landing page)

La página que el cliente ve *primero* cuando abre el link. Arranca con una **cover page** (título, subtítulo, metadata grid), ofrece download del PDF arriba-derecha, y muestra una **metodología-disclosure de 30 segundos** antes del artículo — para que el lector entienda qué tipo de afirmaciones va a leer antes de entrar en ellas. Al final, un **veredicto callout** con confidence score y quote-integrity summary.

```html
{% extends "base.html" %}

{% block content %}
<section class="sharpz-cover">
  <span class="sharpz-cover-brand">
    Reporte Ejecutivo · {{ test.test_type_display_name }}
  </span>
  <h1>{{ test.title }}</h1>
  {% if test.objective %}
  <p class="sharpz-subtitle">{{ test.objective }}</p>
  {% endif %}
  <div class="sharpz-cover-meta">
    {% if deliverable.client_display_name %}
    <div><strong>Cliente</strong><span>{{ deliverable.client_display_name }}</span></div>
    {% endif %}
    <div><strong>Tipo de test</strong><span>{{ test.test_type_display_name }}</span></div>
    <div><strong>Variantes comparadas</strong><span>{{ variants|length }}</span></div>
    <div><strong>Audiencia sintética</strong><span>{{ num_agents }} agentes</span></div>
    <div><strong>Test ID</strong><span>{{ test.test_id }}</span></div>
    <div><strong>Generado</strong><span>{{ generated_at_display }}</span></div>
  </div>
</section>

<!-- PDF download CTA. WeasyPrint-ed server-side on first request, cached after.
     Rendered prominently because CMOs frequently share printed copies with
     their board and prefer a single file over navigating HTML. -->
<div class="sharpz-pdf-download" style="display:flex;justify-content:flex-end;margin:8px 0 16px;">
  <a href="download/full.pdf" download class="sharpz-btn" style="
       display:inline-flex;align-items:center;gap:8px;
       padding:10px 20px;background:var(--accent-warm,#c48a3e);
       color:white;text-decoration:none;border-radius:6px;
       font-weight:600;font-size:14px;">
    ⇣ Descargar deliverable completo (PDF)
  </a>
</div>

<!-- Methodology disclosure: el 30-sec read que frame everything.
     Recordamos al lector que esto es reacción sintética, no research estadístico.
     Mantiene honestidad. -->
<aside class="sharpz-methodology-disclosure" style="
  margin:40px 0 32px;padding:20px 24px;background:#f9f7f2;
  border-left:3px solid var(--accent-warm,#c48a3e);border-radius:6px;
  font-size:13px;line-height:1.6;color:var(--gray-700,#444);">
  <div style="font-size:11px;text-transform:uppercase;letter-spacing:0.1em;
              color:var(--gray-500,#888);margin-bottom:8px;font-weight:600;">
    Cómo leer este reporte · 30 segundos
  </div>
  <p style="margin:0 0 8px;">
    <strong>Este es un test de reacción sintética, no research estadístico.</strong>
    {{ num_agents }} agentes generados por IA — calibrados por archetype —
    consumieron cada variante en paralelo y reaccionaron de forma autónoma.
    Las cifras, patrones y voces capturadas son <strong>señales relativas
    entre variantes</strong>, no predicciones absolutas del mercado real.
  </p>
  <p style="margin:0 0 8px;">
    El valor del reporte está en <strong>detectar qué variante funciona
    mejor bajo las mismas condiciones</strong> y en <strong>iluminar tensiones
    estratégicas antes del spend real</strong> — no en reemplazar paneles
    cuantitativos o ventas piloto.
  </p>
  <p style="margin:0;">
    Encontrarás tres tipos de afirmación diferenciados: <strong>Observación</strong>
    (lo que pasó en la sim), <strong>Inferencia</strong> (razonamiento del
    analista, marcado explícitamente), <strong>Recomendación</strong>
    (acción ancla en observación + inferencia). Metodología completa en Apéndice D.
  </p>
</aside>

<article class="sharpz-article">
  {{ report_html|safe }}
</article>

{% if winner_variant %}
<div class="sharpz-callout" style="margin-top:64px;">
  <div class="sharpz-callout-title">Veredicto · variante recomendada</div>
  <strong>{{ winner_variant.name }}</strong><br>
  <span style="color:var(--gray-500);font-size:13px;">
    variant_id: <code>{{ winner_variant.variant_id }}</code>
  </span>

  {% if test.winner_confidence %}
  <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(0,0,0,0.08);">
    <span style="font-size:12px;text-transform:uppercase;letter-spacing:0.08em;
                 color:var(--gray-500);">
      Confianza del veredicto
    </span>
    <div style="display:flex;align-items:center;gap:12px;margin-top:6px;">
      <strong style="font-size:24px;">{{ "%.0f"|format(test.winner_confidence) }}/100</strong>
      <span class="sharpz-chip">{{ test.winner_confidence_label or '—' }}</span>
    </div>
    {% if test.winner_confidence_reasoning %}
    <p style="font-size:12px;color:var(--gray-500);margin:8px 0 0 0;line-height:1.5;">
      {{ test.winner_confidence_reasoning }}
    </p>
    {% endif %}
  </div>
  {% endif %}

  {% if quote_integrity and quote_integrity.total %}
  <div style="margin-top:16px;padding-top:16px;border-top:1px solid rgba(0,0,0,0.08);">
    <span style="font-size:12px;text-transform:uppercase;letter-spacing:0.08em;
                 color:var(--gray-500);">
      Integridad de quotes
    </span>
    <div style="display:flex;align-items:center;gap:12px;margin-top:6px;">
      <strong style="font-size:18px;">
        {{ quote_integrity.verbatim + quote_integrity.close_match }}/{{ quote_integrity.total }}
      </strong>
      <span class="sharpz-chip">{{ quote_integrity.verified_pct }}% verificadas</span>
    </div>
    <p style="font-size:12px;color:var(--gray-500);margin:8px 0 0 0;line-height:1.5;">
      Quotes verbatim: {{ quote_integrity.verbatim }} ·
      Paráfrasis cercanas (rapidfuzz): {{ quote_integrity.close_match }} ·
      Match semántico (embeddings): {{ quote_integrity.semantic_match or 0 }} ·
      Sin match: {{ quote_integrity.unverified }}.
      Auditable en meta.json del reporte.
    </p>
  </div>
  {% endif %}
</div>
{% endif %}
{% endblock %}
```

### 5.3 `variant.html` — una variante, en detalle

Una página por cada variante del test. Arranca con el nombre, el objetivo contextual, y los *key facts* (precio, specs, fecha, lo que aplique al test_type). Luego un **SVG chart inline** con posts-por-hora durante la simulación (sin JS, printa en PDF). Después la narrativa de 24h, y finalmente los posts iniciales como blockquotes.

```html
{% extends "base.html" %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">
      Variante {{ variant.position|default(variant.name) }}
    </span>
  </div>

  <h1>{{ variant.name }}</h1>

  {% if variant.objective_context %}
  <p style="font-size:20px;color:var(--gray-700);font-style:italic;margin-bottom:48px;">
    {{ variant.objective_context }}
  </p>
  {% endif %}

  {% if variant.key_facts %}
  <div class="sharpz-callout" style="margin-bottom:48px;">
    <div class="sharpz-callout-title">Hechos clave de esta variante</div>
    <ul style="margin:8px 0 0;padding-left:20px;">
      {% for k, v in variant.key_facts.items() %}
      <li><strong>{{ k|replace('_', ' ')|title }}:</strong> {{ v }}</li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}

  {# -------- Timeline chart (SVG, no JS — printa bien en PDF) -------- #}
  {% set timeline = variant.metrics.timeline if variant.metrics and variant.metrics.timeline else [] %}
  {% if timeline and timeline|length > 0 %}
  {% set max_posts = timeline|map(attribute='posts')|max %}
  {% set chart_w = 720 %}
  {% set chart_h = 160 %}
  {% set pad_l = 32 %}
  {% set pad_r = 16 %}
  {% set pad_t = 12 %}
  {% set pad_b = 28 %}
  {% set inner_w = chart_w - pad_l - pad_r %}
  {% set inner_h = chart_h - pad_t - pad_b %}
  {% set n = timeline|length %}

  <hr class="sharpz-section-divider">
  <h2>Actividad por hora · posts durante la sim</h2>
  <p style="color:var(--gray-500);margin-bottom:12px;">
    Distribución temporal de posts con contenido durante las 24 horas de simulación.
    Pico: {{ max_posts }} posts/h.
  </p>
  <figure class="sharpz-timeline-chart"
          style="margin:0;padding:16px;background:var(--gray-50);border-radius:8px;">
    <svg viewBox="0 0 {{ chart_w }} {{ chart_h }}" width="100%"
         preserveAspectRatio="xMidYMid meet"
         style="display:block;font-family:var(--font-ui);font-size:10px;color:var(--gray-700);">
      <!-- axis line -->
      <line x1="{{ pad_l }}" y1="{{ pad_t + inner_h }}"
            x2="{{ pad_l + inner_w }}" y2="{{ pad_t + inner_h }}"
            stroke="#cbd5e1" stroke-width="1"/>
      <!-- bars -->
      {% for t in timeline %}
      {% set bar_w = (inner_w / n) * 0.72 %}
      {% set bar_gap = (inner_w / n) * 0.28 %}
      {% set x = pad_l + loop.index0 * (inner_w / n) + bar_gap / 2 %}
      {% set h = (t.posts / max_posts * inner_h) if max_posts > 0 else 0 %}
      {% set y = pad_t + inner_h - h %}
      <rect x="{{ x }}" y="{{ y }}" width="{{ bar_w }}" height="{{ h }}"
            fill="var(--accent-warm, #c2410c)" rx="2">
        <title>h{{ t.hour }} · {{ t.posts }} posts</title>
      </rect>
      {% if loop.index0 % 4 == 0 or loop.last %}
      <text x="{{ x + bar_w / 2 }}" y="{{ pad_t + inner_h + 16 }}"
            text-anchor="middle" fill="#64748b">{{ t.hour }}h</text>
      {% endif %}
      {% endfor %}
      <!-- y-axis labels -->
      <text x="{{ pad_l - 6 }}" y="{{ pad_t + 4 }}" text-anchor="end"
            fill="#94a3b8">{{ max_posts }}</text>
      <text x="{{ pad_l - 6 }}" y="{{ pad_t + inner_h }}" text-anchor="end"
            fill="#94a3b8">0</text>
    </svg>
    <figcaption style="font-size:11px;color:var(--gray-500);margin-top:6px;">
      Eje X: hora de simulación (0–{{ n - 1 }}). Eje Y: posts publicados.
    </figcaption>
  </figure>
  {% endif %}

  <hr class="sharpz-section-divider">

  <h2>Narrativa de la simulación · 24 horas</h2>
  {{ narrative_html|safe }}

  {% if variant.initial_posts %}
  <hr class="sharpz-section-divider">
  <h2>Posts iniciales (publicados en T=0)</h2>
  <p style="color:var(--gray-500);">
    Los tweets que se publicaron en el minuto 0 de la simulación,
    según el diseño estratégico de esta variante.
  </p>
  <div style="margin-top:24px;">
    {% for p in variant.initial_posts %}
    <blockquote style="margin-bottom:24px;">
      {{ p.content }}
      {% if p._poster_agent_name %}
      <cite>— {{ p._poster_agent_name }} ({{ p.poster_type }})</cite>
      {% endif %}
    </blockquote>
    {% endfor %}
  </div>
  {% endif %}
</article>
{% endblock %}
```

### 5.4 `interviews.html` — Apéndice B · entrevistas

Un bloque Q&A por variante × archetype. Usa blockquotes para cada respuesta, con "Pregunta 1/2/3..." como eyebrow arriba.

```html
{% extends "base.html" %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">
      Voces de los compradores
    </span>
  </div>

  <h1>Entrevistas post-simulación</h1>

  <p style="font-size:18px;color:var(--gray-700);font-style:italic;margin-bottom:48px;">
    Al terminar cada variante, entrevistamos a los mismos {{ archetypes_count }} archetypes
    representativos con {{ questions_count }} preguntas específicas del tipo de test.
    Cada respuesta es el LLM actuando como ese agente, coherente con su biografía y
    lo que vivió durante las 24 horas simuladas.
  </p>

  <div class="sharpz-callout">
    <div class="sharpz-callout-title">Las {{ questions_count }} preguntas</div>
    <ol style="margin:0;padding-left:20px;">
      {% for q in questions %}<li>{{ q }}</li>{% endfor %}
    </ol>
  </div>

  {% for variant in variants %}
  <hr class="sharpz-section-divider">
  <h2>{{ variant.name }}</h2>

  {% if variant.interviews %}
    {% for archetype_key, arch in variant.interviews.items() %}
    <h3>{{ arch.label }}</h3>
    {% if arch.error %}
      <p style="color:var(--gray-500);font-style:italic;">
        (sin respuesta: {{ arch.error }})
      </p>
    {% else %}
      {% for i, answer in arch.parsed|default([])|enumerate %}
      {% if answer %}
      <blockquote>
        <strong style="display:block;font-size:12px;text-transform:uppercase;
                       letter-spacing:0.06em;color:var(--gray-500);
                       font-style:normal;margin-bottom:8px;">
          Pregunta {{ i + 1 }}
        </strong>
        {{ answer }}
      </blockquote>
      {% endif %}
      {% endfor %}
    {% endif %}
    {% endfor %}
  {% else %}
    <p style="color:var(--gray-500);"><em>(sin interviews guardadas)</em></p>
  {% endif %}
  {% endfor %}
</article>
{% endblock %}
```

### 5.5 `audience.html` — grafo + agent grid

Sección que muestra a quién testeamos. Usa **Cytoscape.js** para renderizar el grafo interactivo (pero con fallback si no carga JS o en PDF). Después, una tabla de composición por tipo + cards grid con cada agente individual.

```html
{% extends "base.html" %}

{% block head_extra %}
<script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
{% endblock %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">
      Audiencia Sintética
    </span>
  </div>

  <h1>La audiencia del experimento</h1>

  <p style="font-size:20px;color:var(--gray-700);font-style:italic;margin-bottom:48px;">
    El entorno controlado sobre el que se corrieron las variantes:
    {{ agent_count }} agentes representativos ({{ entity_types_summary }}),
    conectados por relaciones de influencia, rivalidad y cobertura mediática.
  </p>

  <div class="sharpz-callout">
    <div class="sharpz-callout-title">Qué significa "audiencia sintética"</div>
    Cada agente es una persona generada por IA con biografía específica: edad,
    país, profesión, preferencias, rivalidades, consumos mediáticos. Durante la
    simulación, cada uno actúa autónomamente en el venue según su perfil.
    Al final del test, entrevistamos a los archetypes clave para insights cualitativos.
  </div>

  <h2>Grafo de la audiencia</h2>
  <div class="sharpz-graph" id="sharpz-graph-container">
    <div style="padding:32px;font-family:var(--font-ui);color:var(--gray-500);font-size:13px;">
      Cargando visualización interactiva...
    </div>
  </div>
  <p class="sharpz-graph-legend">
    Cada nodo representa un agente. Los bordes muestran relaciones extraídas
    por IA (influencia, competencia, cobertura, rivalidad). Arrastrá para explorar.
  </p>

  <h2>Composición de la audiencia</h2>
  <table>
    <thead>
      <tr><th>Tipo</th><th>Cantidad</th><th>% del total</th></tr>
    </thead>
    <tbody>
      {% for et, count in entity_type_breakdown %}
      <tr>
        <td>{{ et }}</td>
        <td>{{ count }}</td>
        <td>{{ "%.1f"|format(count / agent_count * 100) }}%</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <h2>Los agentes</h2>
  <p>Listado completo de los {{ agent_count }} agentes que participaron de la simulación.</p>

  <div class="sharpz-agent-grid">
    {% for agent in agents %}
    <div class="sharpz-agent-card">
      <span class="type-tag">{{ agent.entity_type }}</span>
      <div class="name">{{ agent.entity_name }}</div>
      {% if agent.username %}
      <div class="handle">@{{ agent.username }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
</article>

<script>
  (function() {
    const graphData = {{ graph_data|tojson|safe }};
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) return;

    const container = document.getElementById('sharpz-graph-container');
    container.innerHTML = '';

    // Build elements
    const elements = [];
    for (const n of graphData.nodes) {
      elements.push({
        data: {
          id: n.id,
          label: n.name,
          type: (n.labels || []).filter(l => l !== 'Entity')[0] || 'Person',
        }
      });
    }
    for (const e of (graphData.edges || [])) {
      elements.push({
        data: {
          source: e.source || e.source_node,
          target: e.target || e.target_node,
          label: e.relation_type || e.name || '',
        }
      });
    }

    // Colores por tipo — adaptados a la paleta del deliverable
    const colors = {
      Executive:      '#B85C38',  // terracota
      GameDeveloper:  '#D97706',
      Streamer:       '#1E40AF',
      Journalist:     '#14532D',
      TechReviewer:   '#166534',
      Gamer:          '#4B5563',
      Parent:         '#7C3AED',
      Activist:       '#991B1B',
      Person:         '#6B7280',
      Organization:   '#0F172A',
    };

    cytoscape({
      container,
      elements,
      style: [
        { selector: 'node',
          style: {
            'background-color': (ele) => colors[ele.data('type')] || '#6B7280',
            'label': 'data(label)',
            'color': '#0A0E27',
            'font-family': 'Inter, sans-serif',
            'font-size': '10px',
            'text-valign': 'bottom',
            'text-margin-y': 4,
            'width': 14, 'height': 14,
            'border-width': 1,
            'border-color': '#FAF9F6',
          }
        },
        { selector: 'edge',
          style: {
            'width': 1,
            'line-color': '#E5E1D8',
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#E5E1D8',
            'arrow-scale': 0.7,
          }
        },
      ],
      layout: { name: 'cose', animate: false, idealEdgeLength: 60, nodeRepulsion: 2500 },
      minZoom: 0.3,
      maxZoom: 3,
    });
  })();
</script>
{% endblock %}
```

### 5.6 `forecast.html` — proyección (opcional)

Solo para test_types que amerítan forecast (pricing_test, campaign_test con estimación de conversion). Muestra pesimista/base/optimista por variante, asunciones explícitas (el CFO puede ajustarlas), análisis de sensibilidad al ratio sim-to-reality, y un checklist de validación.

```html
{% extends "base.html" %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">Forecast</span>
  </div>

  <h1>Forecast de volumen y revenue</h1>

  <p style="font-size:18px;color:var(--gray-700);font-style:italic;margin-bottom:32px;">
    Proyección cuantitativa de unidades y revenue por variante, para conversación
    con Operaciones y Finanzas. Incluye rangos optimista / medio / pesimista,
    asunciones explícitas y análisis de sensibilidad al ratio sim-to-reality.
  </p>

  <div class="sharpz-callout" style="margin-bottom:32px;">
    <div class="sharpz-callout-title">Confianza del modelo</div>
    <div style="display:flex;align-items:center;gap:12px;">
      <strong style="font-size:20px;text-transform:uppercase;">
        {{ forecast.confidence_level or '—' }}
      </strong>
      <span style="font-size:13px;color:var(--gray-500);">
        · ventana: {{ forecast.window_weeks or '—' }} semanas
      </span>
    </div>
    {% if forecast.confidence_reasoning %}
    <p style="font-size:13px;color:var(--gray-500);margin:8px 0 0 0;">
      {{ forecast.confidence_reasoning }}
    </p>
    {% endif %}
  </div>

  <h2>Asunciones del modelo</h2>
  <p>
    El forecast no es una predicción del mundo real: es una proyección
    <em>condicional</em> a un set de asunciones. Si cambian las asunciones,
    cambia el forecast. Cada una está explicitada para que el CFO las pueda ajustar.
  </p>
  <table>
    <thead>
      <tr><th>Parámetro</th><th>Valor asumido</th><th>Razonamiento</th></tr>
    </thead>
    <tbody>
      {% for a in (forecast.assumptions or []) %}
      <tr>
        <td><code>{{ a.key }}</code></td>
        <td><strong>{{ a.value }}</strong></td>
        <td>{{ a.rationale }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  <h2>Proyección por variante</h2>
  {% for v in (forecast.variants or []) %}
  <h3>
    {{ v.variant_name }}
    <span style="font-size:14px;color:var(--gray-500);font-weight:400;">
      · {{ v.price_ars|default(v.price, true) }} ARS
    </span>
  </h3>

  <table>
    <thead>
      <tr><th>Métrica</th><th>Pesimista</th><th>Base</th><th>Optimista</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Unidades (ventana)</td>
        <td>{{ v.units.pessimistic if v.units else '—' }}</td>
        <td><strong>{{ v.units.base if v.units else '—' }}</strong></td>
        <td>{{ v.units.optimistic if v.units else '—' }}</td>
      </tr>
      <tr>
        <td>Revenue bruto (ARS)</td>
        <td>{{ v.revenue_ars_gross.pessimistic if v.revenue_ars_gross else '—' }}</td>
        <td><strong>{{ v.revenue_ars_gross.base if v.revenue_ars_gross else '—' }}</strong></td>
        <td>{{ v.revenue_ars_gross.optimistic if v.revenue_ars_gross else '—' }}</td>
      </tr>
      {% if v.market_share_pct %}
      <tr>
        <td>Market share (%)</td>
        <td colspan="3">{{ v.market_share_pct.base }}%</td>
      </tr>
      {% endif %}
    </tbody>
  </table>

  <table style="margin-top:8px;">
    <thead><tr><th>Señal</th><th>Valor</th></tr></thead>
    <tbody>
      <tr>
        <td>Intent-rate sim (observado)</td>
        <td>{{ (v.intent_rate_sim * 100)|round(1) if v.intent_rate_sim else '—' }}%</td>
      </tr>
      <tr>
        <td>Intent-rate ajustado (post sim-to-reality discount)</td>
        <td><strong>{{ (v.intent_rate_adjusted * 100)|round(1) if v.intent_rate_adjusted else '—' }}%</strong></td>
      </tr>
    </tbody>
  </table>

  {% if v.break_even_vs_base %}
  <p style="font-size:13px;color:var(--gray-600);margin-top:8px;">
    <strong>Break-even:</strong> {{ v.break_even_vs_base }}
  </p>
  {% endif %}
  {% endfor %}

  {% if forecast.sensitivities %}
  <h2>Análisis de sensibilidad</h2>
  <p>Cómo cambia el revenue del winner si el ratio sim-to-reality resulta distinto al asumido.</p>
  {% for s in forecast.sensitivities %}
  <h3>{{ s.parameter }}</h3>
  <table>
    <thead>
      <tr>
        <th>Valor</th>
        {% for val in s.values %}<th>{{ val }}</th>{% endfor %}
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Revenue winner (ARS)</td>
        {% for val in s.impact_on_winner_revenue_ars %}<td>{{ val }}</td>{% endfor %}
      </tr>
    </tbody>
  </table>
  {% if s.interpretation %}
  <p style="font-size:13px;color:var(--gray-600);">{{ s.interpretation }}</p>
  {% endif %}
  {% endfor %}
  {% endif %}

  {% if forecast.caveats %}
  <h2>Caveats</h2>
  <ul>
    {% for c in forecast.caveats %}<li>{{ c }}</li>{% endfor %}
  </ul>
  {% endif %}

  {% if forecast.cfo_checklist %}
  <h2>Checklist para el CFO</h2>
  <p>Validaciones que el modelo recomienda hacer antes de comprometer P&amp;L:</p>
  <ul>
    {% for item in forecast.cfo_checklist %}<li>{{ item }}</li>{% endfor %}
  </ul>
  {% endif %}
</article>
{% endblock %}
```

### 5.7 `appendix_metrics.html` — Apéndice A · métricas crudas

Para auditores, analistas y tiers altos que piden raw data. Tablas por variante con reach, engagement, sentiment, fidelity, demografía, timeline — más CSV download + JSON en `<details>` para auditoría completa.

```html
{% extends "base.html" %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">Apéndice A</span>
  </div>

  <h1>Métricas completas por variante</h1>

  <p style="font-size:18px;color:var(--gray-700);font-style:italic;margin-bottom:24px;">
    Datos cuantitativos crudos capturados durante las 24 horas de simulación.
    Este apéndice es referenciado desde el reporte ejecutivo para todo detalle
    numérico. Cada variante tiene su propio bloque con reach, engagement,
    sentiment, fidelity, demografía y timeline hora por hora.
  </p>

  <p style="margin-bottom:48px;">
    <a href="/api/sharpz/tests/{{ test.test_id }}/metrics.csv"
       class="sharpz-btn" download
       style="display:inline-block;text-decoration:none;">
      ⇣ Descargar CSV completo
    </a>
  </p>

  {% for variant in variants %}
  <hr class="sharpz-section-divider">
  <h2>{{ variant.name }}</h2>

  {% if variant.metrics %}
  {% set m = variant.metrics %}

  <h3>Reach y amplificación</h3>
  <table>
    <thead><tr><th>Métrica</th><th>Valor</th></tr></thead>
    <tbody>
      <tr><td>Posts con contenido</td><td>{{ m.reach.posts_with_content if m.reach else '—' }}</td></tr>
      <tr><td>Posts originales (create_post)</td><td>{{ m.reach.create_post if m.reach else '—' }}</td></tr>
      <tr><td>Contenidos únicos</td><td>{{ m.reach.unique_contents if m.reach else '—' }}</td></tr>
      <tr><td>Reposts</td><td>{{ m.reach.reposts if m.reach else '—' }}</td></tr>
      <tr><td>Quotes</td><td>{{ m.reach.quotes if m.reach else '—' }}</td></tr>
      <tr><td>Likes</td><td>{{ m.reach.likes if m.reach else '—' }}</td></tr>
      <tr><td>Amplificación total</td><td>{{ m.reach.total_amplification if m.reach else '—' }}</td></tr>
      <tr>
        <td>Agentes activos</td>
        <td>{{ m.reach.active_users if m.reach else '—' }} /
            {{ m.reach.total_users if m.reach else '—' }}
            ({{ m.reach.reach_pct if m.reach else '—' }}%)</td>
      </tr>
    </tbody>
  </table>

  <h3>Engagement quality</h3>
  <table>
    <thead><tr><th>Métrica</th><th>Valor</th></tr></thead>
    <tbody>
      <tr><td>Engagement activo (quotes + creates)</td><td>{{ m.engagement.active_engagement if m.engagement else '—' }}</td></tr>
      <tr><td>Engagement pasivo (likes + reposts)</td><td>{{ m.engagement.passive_engagement if m.engagement else '—' }}</td></tr>
      <tr><td>Ratio activo</td><td>{{ m.engagement.active_ratio_pct if m.engagement else '—' }}%</td></tr>
    </tbody>
  </table>

  {% if m.sentiment and not m.sentiment.skipped %}
  <h3>Distribución de sentiment</h3>
  <table>
    <thead><tr><th>Categoría</th><th>%</th><th>Count</th></tr></thead>
    <tbody>
      <tr><td>Supportive</td><td>{{ m.sentiment.supportive_pct }}%</td><td>{{ m.sentiment.supportive }}</td></tr>
      <tr><td>Critical</td><td>{{ m.sentiment.critical_pct }}%</td><td>{{ m.sentiment.critical }}</td></tr>
      <tr><td>Neutral</td><td>{{ m.sentiment.neutral_pct }}%</td><td>—</td></tr>
      <tr><td>Offtopic</td><td>{{ m.sentiment.offtopic_pct }}%</td><td>—</td></tr>
    </tbody>
  </table>
  <p><strong>Backlash flag:</strong> {{ m.backlash.backlash_flag if m.backlash else '—' }}</p>
  {% endif %}

  {% if m.fidelity and not m.fidelity.skipped %}
  <h3>Fidelity del mensaje</h3>
  <p>
    <strong>Score:</strong> {{ m.fidelity.fidelity_score }}/100<br>
    <strong>Razonamiento:</strong> {{ m.fidelity.reasoning }}
  </p>
  {% endif %}

  {% if m.demographics and m.demographics.breakdown_by_entity_type %}
  <h3>Penetración por tipo de entidad</h3>
  <table>
    <thead><tr><th>Tipo</th><th>Activos</th><th>Total</th><th>Penetración %</th></tr></thead>
    <tbody>
      {% for et, data in m.demographics.breakdown_by_entity_type.items() %}
      <tr>
        <td>{{ et }}</td>
        <td>{{ data.active }}</td>
        <td>{{ data.total }}</td>
        <td>{{ data.penetration_pct }}%</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  {% endif %}

  {% if m.timeline %}
  <h3>Timeline de actividad (posts por hora)</h3>
  <table>
    <thead><tr><th>Hora</th><th>Posts</th></tr></thead>
    <tbody>
      {% for t in m.timeline %}
      <tr><td>h{{ t.hour }}</td><td>{{ t.posts }}</td></tr>
      {% endfor %}
    </tbody>
  </table>
  {% endif %}

  <details style="margin-top:24px;">
    <summary style="cursor:pointer;font-weight:600;">Raw JSON completo (para auditoría)</summary>
    <pre style="font-size:11px;background:var(--gray-100);padding:16px;
                border-radius:4px;overflow-x:auto;margin-top:12px;">{{ m | tojson(indent=2) }}</pre>
  </details>

  {% else %}
  <p style="color:var(--gray-500);font-style:italic;">
    Métricas no disponibles para esta variante.
  </p>
  {% endif %}
  {% endfor %}
</article>
{% endblock %}
```

### 5.8 `appendix_methodology.html` — Apéndice D · "es serio?"

La página que responde la pregunta de fondo: *¿esto es serio? ¿cómo lo hicieron?*. Explica audiencia sintética, estructura del test (ceteris paribus), duración simulada, entrevistas, **stack de modelos de IA** (Qwen3-235B, Claude Haiku, Sonnet-4, OpenAI embeddings), quality gates, y —crítico— **5 limitaciones conocidas** listadas explícitamente. Honestidad metodológica como ventaja competitiva.

```html
{% extends "base.html" %}

{% block content %}
<article class="sharpz-article">
  <div style="margin-bottom:32px;">
    <span class="sharpz-cover-brand" style="color:var(--accent-warm);">Apéndice D</span>
  </div>

  <h1>Metodología y limitaciones</h1>

  <p style="font-size:18px;color:var(--gray-700);font-style:italic;margin-bottom:48px;">
    Cómo se diseñó, ejecutó y analizó este experimento. Esta sección se incluye
    para que el cliente pueda evaluar la validez de las conclusiones y replicar
    el proceso si lo desea.
  </p>

  <h2>El experimento</h2>
  <p>
    Este test fue ejecutado sobre la plataforma Sharpz Analytics. La metodología
    central es la simulación de audiencias sintéticas con IA generativa — una
    técnica que permite testear estrategias de comunicación contra audiencias
    virtuales calibradas a un mercado específico, antes de exponerlas al mundo real.
  </p>

  <h2>Audiencia sintética</h2>
  <p>
    La audiencia está compuesta por <strong>{{ num_agents }} agentes</strong>
    generados por IA, cada uno con biografía extensa (edad, país, profesión,
    preferencias, historial, rivalidades, consumo mediático). Los agentes están
    conectados entre sí por relaciones extraídas del seed inicial: influencia,
    cobertura mediática, rivalidad, afinidad. Durante la simulación, cada agente
    actúa de forma autónoma en el venue correspondiente, publicando, comentando,
    reposteando y quoteando en función de su perfil y lo que ve en su feed.
  </p>

  <p>La audiencia incluye:</p>
  <ul>
    {% for et in entity_types_with_counts %}
    <li><strong>{{ et.type }}:</strong> {{ et.count }} agentes ({{ et.pct }}%)</li>
    {% endfor %}
  </ul>

  <h2>Estructura del test</h2>
  <p>
    Las <strong>{{ variants_count }} variantes</strong> se corrieron
    {% if sim_mode == "parallel" %}
    <strong>en paralelo</strong>
    {% else %}
    <strong>secuencialmente</strong> (una sim por vez para evitar saturación de memoria)
    {% endif %}
    sobre la MISMA audiencia sintética (mismos agentes, mismas relaciones, misma
    semilla aleatoria). Lo único que varió entre variantes fue la propia campaña:
    el brief estratégico, el concepto creativo, los artefactos iniciales y los hechos
    clave (precio, fecha, modelo). Esta configuración <em>ceteris paribus</em>
    permite aislar el efecto de la variante sobre las reacciones observadas.
  </p>

  <h2>Duración simulada</h2>
  <p>
    Cada variante simuló <strong>{{ simulation_hours|default(24) }} horas</strong>
    post-lanzamiento. En cada ronda (= 1 hora simulada), una fracción de los
    agentes se "despierta" según su perfil de actividad individual (hora pico,
    hora valle, horario laboral, etc.) y toma una acción autónoma informada por
    su perfil + lo que ve en su timeline.
  </p>

  <h2>Entrevistas post-simulación</h2>
  <p>
    Después de las {{ simulation_hours|default(24) }} horas, entrevistamos a
    <strong>{{ archetypes_count }} buyer archetypes</strong>
    con las mismas {{ questions_count|default(5) }} preguntas en cada variante,
    para obtener feedback cualitativo directo que complementa las métricas
    cuantitativas. Los archetypes son seleccionados para representar distintos
    segmentos demográficos, económicos e ideológicos del mercado.
    Las transcripciones completas están en el Apéndice B.
  </p>

  <h2>Modelos de IA utilizados</h2>
  <p>
    La plataforma opera con una arquitectura multi-tier. Los modelos concretos
    usados en este test (expuestos aquí para auditoría):
  </p>
  <ul>
    {% for row in model_stack|default([]) %}
    <li>
      <strong>{{ row.task_display }}:</strong> {{ row.model_id }}
      {% if row.notes %}— <em>{{ row.notes }}</em>{% endif %}
    </li>
    {% endfor %}
    {% if not model_stack %}
    <li><strong>Generación en bulk (simulación, personas, entrevistas):</strong>
        Qwen3-235B-A22B vía OpenRouter (MoE de 235B parámetros con 22B activos).</li>
    <li><strong>Extracción estructurada (grafo, ontología, facts, fidelity):</strong>
        Claude 3.5 Haiku — estricto con schemas, bajo costo.</li>
    <li><strong>Síntesis y reporte ejecutivo:</strong> Claude Sonnet-4 —
        narrativa cliente-facing.</li>
    <li><strong>Embeddings para el grafo de relaciones:</strong>
        text-embedding-3-large de OpenAI.</li>
    {% endif %}
  </ul>

  <h2>Validación de calidad</h2>
  <p>
    Cada etapa del pipeline pasa por quality gates automáticos antes de continuar.
    Se verifica: cobertura de archetypes críticos, distribución de artefactos
    iniciales, heartbeat de la simulación, consistencia del sentiment, validación
    del idioma del reporte, parseabilidad del veredicto, y ausencia de alucinaciones
    sobre hechos clave (precios, fechas, specs).
  </p>

  <h2>Limitaciones conocidas</h2>
  <p>Honestidad metodológica — el equipo de Sharpz considera importante que el
     cliente conozca explícitamente las limitaciones del enfoque:</p>
  <ul>
    <li><strong>Efectos de competencia reactiva no simulados:</strong> la simulación
        asume que la competencia mantiene su posicionamiento actual durante las
        24 horas. En el mundo real, un anuncio grande puede disparar respuestas
        competitivas en tiempo real que alteran la dinámica.</li>
    <li><strong>Shock mediático offline:</strong> el simulador cubre los venues
        digitales. No modela cobertura de TV, prensa impresa, conversación offline,
        ni efectos de generación espontánea de memes en plataformas no simuladas.</li>
    <li><strong>Variabilidad entre corridas:</strong> a diferencia de experimentos
        deterministas, los LLMs tienen variabilidad inherente. Un mismo escenario
        corrido dos veces puede producir reacciones ligeramente distintas. Para
        decisiones de alto impacto, recomendamos múltiples corridas con distintas
        seeds aleatorias para medir la robustez del hallazgo (disponible en tiers
        Pro y Enterprise).</li>
    <li><strong>Escala poblacional:</strong> los agentes simulados son representantes,
        no una muestra estadística del mercado. Los porcentajes reportados son
        señales relativas entre variantes, no predicciones de conversion rate
        absoluto en el mercado real.</li>
    <li><strong>Horizonte temporal:</strong> el experimento cubre 24 horas. Efectos
        de largo plazo (fatiga de marca, recall post-6-meses, impacto en recompra)
        requieren metodologías complementarias.</li>
  </ul>

  <h2>Reproducibilidad</h2>
  <p>
    Toda corrida se ejecuta con una semilla RNG fija para maximizar reproducibilidad.
    El audit log completo (cada llamada a LLM, cada quality gate, cada transición
    de estado) se preserva y está disponible para revisión técnica bajo pedido.
    El ID técnico de este test es <code>{{ test_id }}</code>.
  </p>

  <h2>Sobre Sharpz</h2>
  <p>
    Sharpz Analytics es una plataforma de testing de estrategias sobre audiencias
    sintéticas calibradas por mercado. Combinamos modelado de audiencias con IA
    generativa + simulación dinámica de interacciones sociales + síntesis ejecutiva
    automatizada para entregar a marcas, partidos y consultoras la posibilidad de
    testear 3-5 movidas estratégicas contra una audiencia virtual en horas, no meses.
  </p>

  <hr class="sharpz-section-divider">
  <p style="font-size:13px;color:var(--gray-500);font-style:italic;">
    Para consultas técnicas sobre metodología, auditoría del proceso o replicación
    del experimento, contactar al equipo de Sharpz.
  </p>
</article>
{% endblock %}
```

---

## 6. Stylesheet completa — `sharpz.css`

Este es el archivo único que todos los templates consumen. Cubre reset, layout, sidebar, cover, article body, callouts, graph, agent cards, y —crítico— los estilos `@media print` que hacen que el PDF quede limpio.

```css
/* ==========================================================================
   SHARPZ — Client Deliverable Stylesheet
   Design language: quiet authority · FT × McKinsey × Stratechery
   Used for both screen rendering and print/PDF export.
   ========================================================================== */

:root {
  /* Colors */
  --ink: #0A0E27;
  --ink-soft: #1F2441;
  --canvas: #FAF9F6;
  --paper: #FFFFFF;
  --accent-warm: #B85C38;
  --accent-warm-soft: #E8CFC4;
  --accent-cool: #1E40AF;
  --accent-cool-hover: #1E3A8A;
  --gray-100: #F4F2ED;
  --gray-200: #E5E1D8;
  --gray-400: #A8A29A;
  --gray-500: #6B7280;
  --gray-700: #374151;

  /* Typography */
  --font-ui: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-serif: "Source Serif 4", "Charter", "Iowan Old Style",
                "Palatino Linotype", "Hoefler Text", Georgia, serif;
  --font-mono: "JetBrains Mono", "SF Mono", Menlo, Consolas, monospace;

  /* Layout */
  --sidebar-width: 280px;
  --reading-width: 720px;
  --content-padding: 48px;
}

/* ---------- Reset + base ---------- */
* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--canvas);
  color: var(--ink);
  font-family: var(--font-ui);
  font-size: 16px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  color: var(--accent-cool);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 2px;
  transition: color 120ms ease;
}
a:hover { color: var(--accent-cool-hover); }

/* ---------- Layout: sidebar + main ---------- */
.sharpz-layout { display: flex; min-height: 100vh; }

.sharpz-sidebar {
  width: var(--sidebar-width);
  background: var(--paper);
  border-right: 1px solid var(--gray-200);
  padding: 48px 28px;
  position: fixed; left: 0; top: 0;
  height: 100vh; overflow-y: auto;
}

.sharpz-sidebar h1 {
  font-family: var(--font-ui);
  font-size: 22px; font-weight: 700;
  color: var(--ink); letter-spacing: -0.02em;
  margin: 0 0 4px 0; line-height: 1.2;
}

.sharpz-sidebar .sharpz-brand-tag {
  display: inline-block;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--accent-warm); font-weight: 600;
  margin-bottom: 32px;
}

.sharpz-sidebar .sharpz-client-logo {
  display: block;
  max-width: 140px; max-height: 48px;
  height: auto; width: auto;
  margin-bottom: 18px; object-fit: contain;
}

.sharpz-sidebar .sharpz-meta {
  font-size: 11px; color: var(--gray-500); line-height: 1.5;
  margin-bottom: 32px; padding-bottom: 24px;
  border-bottom: 1px solid var(--gray-200);
}
.sharpz-sidebar .sharpz-meta strong {
  color: var(--gray-700); font-weight: 600;
  display: block;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em;
  margin-top: 8px; margin-bottom: 2px;
}
.sharpz-sidebar .sharpz-meta code { font-family: var(--font-mono); font-size: 10px; }

.sharpz-nav { list-style: none; padding: 0; margin: 0; }

.sharpz-nav .sharpz-nav-label {
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--gray-400); font-weight: 600;
  margin-bottom: 12px; margin-top: 20px;
}

.sharpz-nav-item { margin-bottom: 2px; }

.sharpz-nav-item a {
  display: block;
  padding: 8px 12px;
  border-radius: 2px;
  text-decoration: none;
  color: var(--ink-soft);
  font-size: 14px; line-height: 1.4;
  transition: background 100ms ease, color 100ms ease;
}
.sharpz-nav-item a:hover { background: var(--gray-100); color: var(--ink); }
.sharpz-nav-item a.active {
  background: var(--gray-100); color: var(--ink);
  font-weight: 600;
  border-left: 2px solid var(--accent-warm);
  padding-left: 10px;
}

.sharpz-nav-icon {
  display: inline-block; width: 18px; margin-right: 8px;
  color: var(--gray-400); font-size: 12px;
}

.sharpz-pdf-btn {
  display: block;
  margin-top: 8px;
  padding: 4px 12px;
  font-size: 11px; color: var(--gray-500);
  text-decoration: none; border-radius: 2px;
}
.sharpz-pdf-btn:hover { color: var(--accent-cool); }

.sharpz-sidebar-footer {
  margin-top: 48px; padding-top: 24px;
  border-top: 1px solid var(--gray-200);
  font-size: 10px; color: var(--gray-400); line-height: 1.6;
}

/* ---------- Main content area ---------- */
.sharpz-main {
  margin-left: var(--sidebar-width);
  flex: 1;
  padding: 64px var(--content-padding) 96px;
}
.sharpz-content { max-width: var(--reading-width); margin: 0 auto; }

/* ---------- Cover page ---------- */
.sharpz-cover {
  padding: 120px 0 80px;
  border-bottom: 1px solid var(--gray-200);
  margin-bottom: 64px;
}

.sharpz-cover-brand {
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.18em;
  color: var(--accent-warm); font-weight: 600;
  margin-bottom: 48px;
}

.sharpz-cover h1 {
  font-family: var(--font-serif);
  font-size: 56px; line-height: 1.08; letter-spacing: -0.03em;
  color: var(--ink);
  margin: 0 0 24px 0; font-weight: 700;
}

.sharpz-cover .sharpz-subtitle {
  font-family: var(--font-serif);
  font-size: 24px; line-height: 1.3;
  color: var(--gray-700); font-style: italic;
  margin-bottom: 80px;
}

.sharpz-cover .sharpz-cover-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 24px; font-size: 12px;
}
.sharpz-cover .sharpz-cover-meta > div strong {
  display: block;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--gray-500);
  margin-bottom: 4px; font-weight: 600;
}
.sharpz-cover .sharpz-cover-meta > div span {
  color: var(--ink);
  font-family: var(--font-mono); font-size: 12px;
}

/* ---------- Article body (the reading experience) ---------- */
.sharpz-article {
  font-family: var(--font-serif);
  font-size: 18px; line-height: 1.75;
  color: var(--ink-soft);
}

.sharpz-article h1, .sharpz-article h2, .sharpz-article h3, .sharpz-article h4 {
  font-family: var(--font-serif);
  color: var(--ink);
  line-height: 1.25; letter-spacing: -0.015em;
}

.sharpz-article h1 { font-size: 40px; font-weight: 700; margin: 0 0 32px; }
.sharpz-article h2 { font-size: 28px; font-weight: 600; margin: 56px 0 20px; padding-top: 8px; }
.sharpz-article h3 { font-size: 22px; font-weight: 600; margin: 40px 0 12px; }
.sharpz-article h4 {
  font-size: 18px; font-weight: 600; margin: 32px 0 8px;
  font-family: var(--font-ui);
}

.sharpz-article p { margin: 0 0 24px 0; }
.sharpz-article strong { font-weight: 600; color: var(--ink); }
.sharpz-article em { font-style: italic; }

.sharpz-article blockquote {
  border-left: 3px solid var(--accent-warm);
  padding: 4px 0 4px 24px;
  margin: 32px 0;
  font-style: italic;
  color: var(--gray-700);
  font-size: 19px; line-height: 1.55;
}
.sharpz-article blockquote cite {
  display: block; margin-top: 8px;
  font-style: normal; font-size: 14px;
  color: var(--gray-500);
  font-family: var(--font-ui);
}

.sharpz-article ul, .sharpz-article ol { margin: 16px 0 24px; padding-left: 28px; }
.sharpz-article li { margin-bottom: 10px; line-height: 1.6; }

.sharpz-article hr {
  border: none;
  border-top: 1px solid var(--gray-200);
  margin: 48px 0;
}

.sharpz-article code {
  font-family: var(--font-mono);
  font-size: 0.88em;
  background: var(--gray-100);
  padding: 1px 6px; border-radius: 2px;
}

.sharpz-article pre {
  font-family: var(--font-mono);
  font-size: 13px;
  background: var(--gray-100);
  padding: 16px 20px; border-radius: 4px;
  overflow-x: auto; line-height: 1.5;
  margin: 24px 0;
}
.sharpz-article pre code { background: transparent; padding: 0; font-size: inherit; }

/* Tablas estilo "bold rule" — inspiradas en papers y reportes McKinsey */
.sharpz-article table {
  width: 100%;
  border-collapse: collapse;
  margin: 32px 0;
  font-family: var(--font-ui);
  font-size: 14px; line-height: 1.5;
}
.sharpz-article thead {
  border-top: 2px solid var(--ink);
  border-bottom: 1px solid var(--ink);
}
.sharpz-article tbody { border-bottom: 2px solid var(--ink); }
.sharpz-article th {
  padding: 12px 16px; text-align: left;
  font-weight: 600;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--ink);
}
.sharpz-article td {
  padding: 12px 16px;
  border-top: 1px solid var(--gray-200);
  vertical-align: top;
}

/* ---------- Special blocks ---------- */
.sharpz-callout {
  background: var(--gray-100);
  border-left: 3px solid var(--gray-500);
  padding: 20px 24px;
  margin: 32px 0;
  border-radius: 0 2px 2px 0;
  font-family: var(--font-ui);
  font-size: 14px; line-height: 1.55;
}
.sharpz-callout-title {
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--gray-500); font-weight: 600;
  margin-bottom: 8px;
}

.sharpz-section-divider {
  border: none;
  border-top: 1px solid var(--gray-200);
  margin: 72px 0 56px;
}

/* ---------- Graph viewer container ---------- */
.sharpz-graph {
  width: 100%; height: 640px;
  background: var(--paper);
  border: 1px solid var(--gray-200);
  border-radius: 4px;
  position: relative;
  margin: 32px 0;
  overflow: hidden;
}

.sharpz-graph-legend {
  font-family: var(--font-ui);
  font-size: 12px; color: var(--gray-500);
  margin-top: 8px;
}

.sharpz-agent-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin: 32px 0;
  font-family: var(--font-ui);
}

.sharpz-agent-card {
  background: var(--paper);
  border: 1px solid var(--gray-200);
  padding: 16px 18px;
  border-radius: 2px;
}
.sharpz-agent-card .type-tag {
  display: inline-block;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--accent-warm); font-weight: 600;
  margin-bottom: 6px;
}
.sharpz-agent-card .name {
  font-size: 16px; font-weight: 600;
  color: var(--ink);
  margin-bottom: 4px; line-height: 1.3;
}
.sharpz-agent-card .handle {
  font-family: var(--font-mono);
  font-size: 12px; color: var(--gray-500);
}

/* ==========================================================================
   Print / PDF styles
   ========================================================================== */
@media print {
  :root { --content-padding: 0; }

  body { background: var(--paper); font-size: 11pt; }

  .sharpz-layout { display: block; }
  .sharpz-sidebar { display: none; }             /* no sidebar en print */
  .sharpz-main { margin-left: 0; padding: 0; }
  .sharpz-content { max-width: none; margin: 0; }

  .sharpz-article { font-size: 11pt; line-height: 1.6; }

  .sharpz-article h1 { font-size: 24pt; }
  .sharpz-article h2 { font-size: 16pt; margin-top: 32pt; }
  .sharpz-article h3 { font-size: 13pt; margin-top: 20pt; }
  .sharpz-article blockquote { font-size: 11pt; }

  .sharpz-cover { page-break-after: always; padding: 60pt 0 40pt; }
  .sharpz-cover h1 { font-size: 32pt; }

  .sharpz-pdf-btn, .sharpz-nav, .sharpz-sidebar-footer { display: none; }

  /* Page-break rules */
  h2, h3 { page-break-after: avoid; }
  p, blockquote, table { page-break-inside: avoid; }

  /* Link URL annotation (classic print behavior) */
  a { color: var(--ink); text-decoration: none; }
  a[href^="http"]:after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: var(--gray-500);
  }
}

/* ==========================================================================
   Responsive (mobile — collapse sidebar)
   ========================================================================== */
@media (max-width: 900px) {
  .sharpz-sidebar {
    position: static;
    width: 100%; height: auto;
    border-right: none;
    border-bottom: 1px solid var(--gray-200);
    padding: 24px;
  }
  .sharpz-main { margin-left: 0; padding: 32px 20px; }
  .sharpz-cover h1 { font-size: 36px; }
  .sharpz-article h1 { font-size: 28px; }
  .sharpz-article h2 { font-size: 22px; }
}
```

---

## 7. `manifest.json` — registro de assets del deliverable

Cada test publicado genera un directorio con HTML files + `manifest.json`. El manifest lista TODO lo que el cliente puede consumir, en qué orden, con qué título. El backend usa este manifest para construir el sidebar dinámicamente, registrar views (log analítico) y servir los archivos con auth check.

**Estructura del directorio publicado:**

```
uploads/tests/<test_id>/deliverable_v1_snapshot/
├── manifest.json
├── index.html                  # redirect a executive.html, o landing propia
├── executive.html
├── audience.html
├── variant_<variant_id>.html   # una por variante
├── variant_<variant_id>.html
├── variant_<variant_id>.html
├── interviews.html
├── forecast.html               # opcional
├── appendix_metrics.html       # opcional
├── appendix_methodology.html
└── static/
    └── sharpz.css
```

**Ejemplo real** (del deliverable McAllister Burger / Arcos Dorados, publicado 21-Abr-2026):

```json
{
  "deliverable_id": "deliv_a0948690bb",
  "test_id": "test_a00e02c5c0fa",
  "client_display_name": "Arcos Dorados Argentina (McDonald's)",
  "test_display_title": "McAllister Burger · Pricing Argentina Q2 2026",
  "test_display_subtitle": "Identificar el punto de pricing óptimo para el lanzamiento de la McAllister Burger en Argentina que maximice volumen de unidades sin erosionar la percepción premium del producto como edición especial atada a la selección argentina. Necesitamos saber si el mercado tolera pricing por encima de nuestra línea premium habitual ($8.000–$12.000) dada la carga emocional del nombre.",

  "assets": [
    { "asset_id": "asset_555d13b1", "kind": "executive_report",
      "title": "Reporte Ejecutivo",
      "html_path": "executive.html",  "pdf_path": null, "order": 1 },

    { "asset_id": "asset_4a7f4529", "kind": "audience",
      "title": "Audiencia",
      "html_path": "audience.html",   "pdf_path": null, "order": 2 },

    { "asset_id": "asset_a8eef6d9", "kind": "individual_report",
      "title": "$9.900 ARS",
      "html_path": "variant_var_88dc28ce.html", "pdf_path": null, "order": 10 },

    { "asset_id": "asset_dda53920", "kind": "individual_report",
      "title": "$19.900 ARS",
      "html_path": "variant_var_e4c26221.html", "pdf_path": null, "order": 11 },

    { "asset_id": "asset_cfb7297a", "kind": "individual_report",
      "title": "$29.900 ARS",
      "html_path": "variant_var_ddb54e64.html", "pdf_path": null, "order": 12 },

    { "asset_id": "asset_d0876a18", "kind": "interviews",
      "title": "Apéndice B · Entrevistas",
      "html_path": "interviews.html", "pdf_path": null, "order": 30 },

    { "asset_id": "asset_7ee265a5", "kind": "appendix_methodology",
      "title": "Apéndice D · Metodología",
      "html_path": "appendix_methodology.html", "pdf_path": null, "order": 50 }
  ],

  "base_path": "/.../uploads/tests/test_a00e02c5c0fa/deliverable",
  "access_token": null,            // si se sirve bajo JWT, acá va el token / null = abierto
  "expires_at": null,              // null = sin expiración
  "views": 25,
  "view_log": [
    { "ts": "2026-04-21T10:24:56.200610", "ip": "127.0.0.1", "ua": "Mozilla/5.0 ..." },
    // … cada visita queda loggeada
  ],
  "published_at": "2026-04-21T10:24:05.775846",
  "created_at":   "2026-04-21T10:24:05.354327",
  "updated_at":   "2026-04-21T11:23:35.455916"
}
```

**Convenciones de `order`:**
- `1–9` → páginas obligatorias principales (executive, audience).
- `10–19` → reportes individuales por variante.
- `20–29` → sections opcionales (forecast).
- `30–39` → apéndices "voces" (interviews).
- `40–49` → apéndices "data cruda" (metrics, CSV).
- `50–59` → apéndices "metodología, nosotros".

**Kinds válidos** (enumerables, para type-safety del sidebar):
- `executive_report` · `audience` · `individual_report` · `interviews`
- `forecast` · `appendix_metrics` · `appendix_methodology`

**Flag `pdf_path`:** opcional por asset. Cuando el backend genera un PDF individual con WeasyPrint (triggered on-demand), actualiza el manifest con la ruta al PDF cacheado. Además existe un PDF "full" (`download/full.pdf`) que concatena todo.

---

## 8. Flujo de navegación del cliente

```
1. Cliente recibe email: "Tu test 'McAllister Burger · Pricing Argentina Q2 2026' está listo."
   Link: https://app.sharpz.io/d/deliv_a0948690bb?token=<jwt>

2. Click → aterriza en executive.html.
   Lee la cover (cliente, tipo, variantes, agentes, ID, fecha).
   Ve el botón "Descargar deliverable completo (PDF)" arriba-derecha.
   Lee la methodology disclosure de 30s.
   Lee el reporte ejecutivo (5–8 min de lectura).
   Ve el veredicto callout abajo (confidence + quote integrity).

3. Click en sidebar "$9.900 ARS" → variant_var_88dc28ce.html.
   Ve hechos clave, SVG de posts/hora, narrativa 24h, tweets iniciales.
   Repite para las otras variantes.

4. Click "Audiencia" → audience.html.
   Grafo cytoscape interactivo, tabla de composición, agent cards.

5. Click "Apéndice B · Entrevistas" → interviews.html.
   Lee quotes de los 5 archetypes en las 3 variantes.

6. (opcional, tier pro+) Click "Apéndice A · Métricas crudas" →
   appendix_metrics.html. Descarga CSV si quiere, o expande raw JSON.

7. Click "Apéndice D · Metodología" → appendix_methodology.html.
   Lee las 5 limitaciones conocidas, qué modelos se usaron,
   cómo se validó calidad. Toma confianza en el proceso.

8. Eventualmente → descarga el PDF completo y lo manda al board.
```

**Tiempo total promedio estimado:** 12–20 minutos de lectura activa, 3 minutos de skim ejecutivo.

---

## 9. Branding hooks por cliente

El template soporta **2 hooks de branding** via contexto Jinja:

```python
context = {
    ...,
    "branding": {
        "primary_color": "#FFC72C",   # McDonald's yellow
        "logo_url": "https://cdn.sharpz.io/clients/arcos-dorados/logo.png",
    },
}
```

**Qué cambia con estos hooks:**

| Hook | Efecto visual |
|---|---|
| `primary_color` | Color del brand tag "SHARPZ ANALYTICS" · borde izq. del nav item activo · background del chip de "variante ganadora" · color de los links. |
| `logo_url` | Aparece un `<img>` del logo del cliente arriba de todo en la sidebar (sobre el brand tag), con `max-width: 140px; max-height: 48px; object-fit: contain`. |

Todo lo demás se mantiene constante — el serif body, el acento terracota del blockquote, la paleta gray. El branding se aplica en zonas *periféricas* (sidebar, veredict chip, links); el cuerpo del reporte preserva su identidad Sharpz. Es intencional: el cliente debe sentir el reporte como *suyo* pero reconocer la firma del proveedor.

---

## 10. Checklist de QA visual del deliverable

Antes de publicar cualquier deliverable, el operador valida:

- [ ] **Cover page:** título no corta, subtítulo cabe en el viewport, metadata grid con al menos 4 campos.
- [ ] **Methodology disclosure:** visible en primera pantalla si el lector scrollea 200px.
- [ ] **Sidebar:** nombre del cliente visible sin truncar, todos los assets del manifest aparecen en el orden correcto, el item activo tiene el border-left.
- [ ] **Article body:** headings respetan jerarquía (H1 > H2 > H3), blockquotes con border terracota, tablas con top-rule bold.
- [ ] **Variant pages:** SVG de posts/hora renderiza, hechos clave en callout, posts iniciales en blockquotes con `<cite>`.
- [ ] **Audience page:** grafo cytoscape carga (sin JS, muestra mensaje "cargando"), tabla de composición suma 100%, cards alineados en grid.
- [ ] **Interviews page:** quotes organizadas por variante → archetype → pregunta, con eyebrow "Pregunta N".
- [ ] **Appendices:** methodology lista las 5 limitaciones explícitas, metrics tiene CSV download + raw JSON colapsable.
- [ ] **PDF export:** sidebar desaparece, page-break entre variantes, page numbers, URL annotation en links externos, font-size baja a 11pt.
- [ ] **Mobile:** en <900px, sidebar colapsa arriba, reading width ocupa 100% con 20px padding, tablas scrollean horizontal si no caben.
- [ ] **Dark-mode del navegador:** NO respetar — el deliverable siempre se ve claro (el serif en dark looks feo y rompe la intención de "papel").

---

## 11. Anti-patterns explícitos

Cosas que **no** van en el deliverable, aunque sean tentadoras:

- ❌ **Emojis en títulos** ("✨ Veredicto", "📊 Métricas"). El deliverable es sobrio.
- ❌ **Gradients o glass morphism.** Es para landing/marketing, no para un reporte que se imprime.
- ❌ **Charts con 20 colores.** Un solo acento por gráfico (terracota o azul frío). Grises para todo lo demás.
- ❌ **"Powered by Sharpz" en footer.** Ya está el brand tag arriba; repetirlo parece inseguro.
- ❌ **Botones "Share on Twitter" / "Copy link".** Es confidencial — no queremos facilitar leaks.
- ❌ **Autoplay de audio/video**, animaciones en loop, parallax.
- ❌ **Popups / toasters / chat bubbles.** El cliente lee. Punto.
- ❌ **Esconder limitaciones.** El apéndice D es un feature, no un bug. La honestidad vende más que la ilusión de perfección.
- ❌ **Dark mode.** Rompe la intención de "papel", el serif se ve mal sobre negro.

---

## 12. Entregables de diseño

En la entrega a V2, este documento va acompañado por:

| Archivo | Qué contiene |
|---|---|
| `sharpz.css` | El stylesheet completo (sección 6). ~620 líneas. |
| `base.html` | Template maestro con sidebar + branding injection (sección 5.1). |
| `executive.html` | Reporte ejecutivo / landing page del deliverable (sección 5.2). |
| `variant.html` | Template por variante con SVG timeline (sección 5.3). |
| `interviews.html` | Apéndice B · Q&A por variante × archetype (sección 5.4). |
| `audience.html` | Grafo cytoscape + agent cards (sección 5.5). |
| `forecast.html` | Proyección opcional con sensitivities (sección 5.6). |
| `appendix_metrics.html` | Apéndice A · data cruda (sección 5.7). |
| `appendix_methodology.html` | Apéndice D · metodología + limitaciones (sección 5.8). |
| `manifest.schema.json` | Schema del manifest.json (sección 7) — para type-safety del writer backend. |

Fuentes externas (vía Google Fonts):
- **Inter** (400, 500, 600, 700).
- **Source Serif 4** (400, 500, 600 · italic 400).
- **JetBrains Mono** (400, 500).

Dependencias JS (CDN, único archivo externo):
- **Cytoscape.js 3.26.0** — solo usado en `audience.html` para el grafo.

Sin framework (no React, no Vue). Todos los templates son Jinja2 puro renderizados server-side. Esto es deliberado: el deliverable tiene que ser estático, portable (abrir el HTML offline desde el mail archivado), y printeable sin JavaScript.

---

**Fin del documento.** Este es el tercero de la trilogía de diseño (landing · intake · deliverable). Los tres archivos, juntos, cubren la superficie de diseño completa de Sharpz Analytics V2.
