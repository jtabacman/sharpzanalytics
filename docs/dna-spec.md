# Sharpz V2 — DNA Specification

> **Status:** v0.2 — open questions resueltas, pre-code.
> **Owner:** Julian (operator) + build Claude (architect).
> **Purpose:** este documento define el contrato declarativo que convierte a Sharpz en plataforma extensible. Cada `test_type` se describe como un YAML structured — no como código. Agregar un test_type #16 o un venue custom per-cliente = agregar un archivo YAML, no modificar el pipeline.

---

## 1. Propósito y principios de diseño

### 1.1 Por qué "DNA-first"

El prototipo anterior (MiroFish) tenía el venue y la lógica de simulación **hardcoded** (Twitter/Reddit para todos los test_types). El resultado: 13 de 15 test_types corrían en un venue incorrecto, generando outputs artificiales. V2 invierte la relación: **el código del pipeline es genérico; la DNA del test_type dicta el comportamiento.**

Análogo conceptual: el pipeline es un intérprete, la DNA es el programa.

### 1.2 Principios

1. **Declarativo > imperativo.** Un test_type se define por lo que **es**, no por lo que hace paso a paso.
2. **Composable.** Venues, settings, simulation modes y QA checklists se mezclan sin cambios al core.
3. **Versionable.** Cada DNA tiene `version`. Tests viejos se re-corren con su DNA histórica exacta (reproducibilidad).
4. **Inspectable.** El operador lee el YAML y entiende el test_type en 5 minutos sin abrir código.
5. **Validable.** Hay un schema estricto (pydantic) que un DNA nuevo debe pasar en CI antes de merge.
6. **Sin sorpresas.** Toda customización que un cliente puede pedir cae dentro del schema — no hay "poner un if en pipeline.py para el cliente X".

### 1.3 Anti-patterns explícitamente prohibidos

- Lógica del test_type dispersa entre múltiples archivos de código Python.
- Prompts concatenados en strings dentro de funciones.
- Venue hardcoded en el pipeline core.
- Un test_type que requiere cambios al engine para funcionar → es señal de que falta un campo en la spec.

---

## 2. Anatomía de una DNA

Una DNA es un archivo YAML con las siguientes secciones top-level:

```yaml
# dna/investor_pitch.yaml

test_type: investor_pitch        # identifier único, snake_case
version: "1.0.0"                  # semver, bump en cambios de schema
status: active                    # active | deprecated | experimental

# Quién y para qué
client_facing:
  one_liner: "..."
  decision_question: "..."
  buyer_profile: [...]
  typical_trigger: "..."

# El panel (quién responde)
panel:
  anchors_spec: {...}
  ecosystem_spec: {...}
  amplification: {...}
  exclude_entity_types: [...]

# Cómo se simula
simulation:
  mode: deliberation | survey_batch | forecast | usage_simulation | hybrid
  panel_size: {...}
  duration: {...}
  rounds: {...}
  propagation: {...}

# Dónde ocurre (físico/virtual)
setting:
  category: in_person | digital | hybrid | async
  description: "..."
  message_tone_defaults: {...}

# Canales y reglas (el venue lógico)
venue:
  channels: [...]
  visibility_matrix: {...}
  turn_dynamics: {...}

# Qué recibe el panel
stimulus:
  formats_accepted: [...]
  delivery_format: {...}

# Qué se mide
metrics:
  primary: [...]
  secondary: [...]
  never_emphasize: [...]

# Cómo se reporta
report:
  required_sections: [...]
  optional_sections: [...]
  length_target: {...}
  quote_min: N
  unique_sections: [...]

# QA checklists
qa_review:
  post_stage_2: [...]
  post_stage_4: [...]
  post_stage_6: [...]
  post_stage_7: [...]

# Tier overrides
tier_overrides:
  economy: {...}
  pro: {...}
  premium: {...}
  ultra: {...}

# Caveats estáticos (lo que el test NO puede decir)
limits: [...]

# Cross-test learning
cross_test_learning:
  patterns_to_extract: [...]
  priors_relevance: {...}

# Pricing hint
pricing_recommendation:
  default_tier: pro
  notes: "..."

# Prompts reference
prompts:
  intake_schema: "prompts/investor_pitch/intake.yaml"
  amplifier: "prompts/investor_pitch/amplifier.yaml"
  persona_generator: "prompts/investor_pitch/persona.yaml"
  # ... etc
```

---

## 3. Field reference

### 3.1 `test_type`

String snake_case. Identifier único en el sistema. Es el filename del YAML sin extensión. No se puede cambiar después de release (tests históricos referencian).

### 3.2 `version`

Semver. Bump rules:
- **major (1.x → 2.x):** cambio incompatible (ej. rename de campo requerido)
- **minor (1.0 → 1.1):** nueva capability opt-in (ej. nuevo canal en venue)
- **patch (1.0.0 → 1.0.1):** fix de typo en prompt, sin cambio de comportamiento

### 3.3 `status`

- `active` — disponible para clientes
- `deprecated` — existe para retrocompatibilidad, no disponible para nuevos tests
- `experimental` — disponible solo para tier Ultra con flag explícito

### 3.4 `client_facing`

```yaml
client_facing:
  one_liner: "Validar si un pitch deck está listo para roadshow LP antes de gastar tiempo y reputación."
  decision_question: "¿Salir a roadshow formal con este deck, o volver al drawing board?"
  buyer_profile:
    - "Fundador o GP de fondo que está por levantar $10M-$1B"
    - "Head of IR / capital formation en un fondo establecido"
  typical_trigger: "Pre-roadshow LP, $100M+ raise, 2-6 semanas antes de primeras reuniones"
  decision_outputs: [GO, CONDITIONAL_GO, DELAY_AND_FIX, NO_GO]
```

### 3.5 `panel`

Define la composición del panel y cómo se genera.

```yaml
panel:
  anchors_spec:
    count: {min: 6, max: 8, recommended: 8}
    field_schema_ref: "prompts/investor_pitch/intake.yaml#anchors"
    examples:
      - "LP institucional — agri specialist (tipo TIAA/Nuveen)"
      - "LP sovereign wealth — food security mandate"
      - "Family office — Argentino/LatAm"

  ecosystem_spec:
    extract_from_stimulus: true
    target_types:
      - law_firm: {count: 3-5, rationale: "Advisors de due diligence"}
      - media_trade: {count: 3-5, rationale: "Publicaciones que LPs leen"}
      - comparable_company: {count: 5-8, rationale: "Competidores citables"}
      - regulator: {count: 1-3, rationale: "Ministerios / CNV / SEC relevantes"}

  amplification:
    strategy: deterministic_llm
    target_pool: 48
    per_anchor_cap: [2, 15]
    formula: "M = round(target_pool / K)"   # K = anchors count

  composition_targets:
    primary_panel_pct: {min: 50, max: 60}     # LPs target
    ecosystem_pct: {min: 15, max: 25}
    context_pct: {min: 20, max: 30}

  exclude_entity_types:
    - ConsumerBrand
    - RetailCustomer
    - IndividualInvestorRetail
    - InfluencerSocialMedia

  quality_requirements:
    bio_length_min_words: 300
    bio_length_target_words: 450
    persona_realism_score_min: 0.7     # LLM self-evaluation 0-1
```

### 3.6 `simulation` — el campo más importante

Aquí se resuelve el polimorfismo. Cinco modos posibles, cada uno con lógica de Stage 4 distinta.

```yaml
simulation:
  mode: deliberation      # deliberation | survey_batch | forecast | usage_simulation | hybrid

  # Campos comunes a todos los modos
  panel_size:
    default: 48
    min: 32
    max: 80

  duration:
    simulated_time: "pitch_meeting_day + 7d_followup"
    wall_clock_target_minutes: 12

  # Campos específicos del modo deliberation
  rounds:
    min: 15
    default: 20
    max: 30
    delivery_round: 1               # en qué round se entrega el stimulus
    interview_cutoff_round: 20      # después de N rounds se pasa a entrevistas

  propagation:
    type: venue_rules               # venue_rules | none | custom
    cross_agent_visibility: controlled   # all | controlled | none
    info_decay: round_by_round

  # Solo para mode=survey_batch
  # survey_questions_ref: "prompts/pricing_test/survey.yaml"
  # batch_size: 100
  # parallelism: 50

  # Solo para mode=forecast
  # forecast_target: vote_share     # qué outcome predicir
  # confidence_interval: 0.90
  # named_entity_sampling: 5%       # % de agents que son named entities reales para quotes ilustrativos

  # Solo para mode=usage_simulation
  # simulated_days: 7
  # touchpoints_per_day: 2-4
  # individual_only: true           # no hay interacción entre agents
```

#### 3.6.1 Los 5 modos en detalle

| Modo | Semántica | Output natural | Cuándo usarlo |
|---|---|---|---|
| `deliberation` | Multi-round back-and-forth entre agents. Cada round un subset actúa, otros reaccionan, se forman opiniones, hay inflection points y cascades. | Sim log rico + temporal analysis + quotes verbatim | Decisiones donde importa el proceso social (pitch meetings, crisis, debates políticos, crisis de marca) |
| `survey_batch` | Una sola ronda. Cada agent responde un cuestionario structured en paralelo. No hay interacción cross-agent. | Distribution + segmentation + outliers | Decisiones donde importa la **respuesta individual** (pricing, creative, audience fit, product feature prioritization) |
| `forecast` | Modelado aggregate con N grande. Few named entities se "entrevistan" deep para color. El resto son data points para calibrar. | Prediction + CI + segment breakdown + illustrative quotes | Predicciones macro (electoral turnout, policy impact, market adoption curves) |
| `usage_simulation` | Cada agent simula día-por-día su interacción con el producto. Individual, no cross-agent. | Journey per segment + friction points + NPS estimate | Product launch, onboarding design, feature prioritization |
| `hybrid` | Combina dos modos. Típicamente survey_batch amplio + deliberation en top-K agents identificados como pivotales. | Mix — depende de la config | Test_types que necesitan volumen Y profundidad (policy_rollout, b2b_pricing, churn_analysis) |

#### 3.6.2 Panel size por modo (guidelines)

| Modo | Panel default | Min | Max | Cost scaling |
|---|---|---|---|---|
| deliberation | 40-120 | 30 | 150 | O(agents × rounds × runs) |
| survey_batch | 500-1500 | 200 | 3000 | O(agents × runs) |
| forecast | 2000-5000 | 1000 | 10000 | O(agents) batch + O(K × deep) |
| usage_simulation | 100-300 | 50 | 500 | O(agents × days) |
| hybrid | varía | varía | varía | varía |

**Regla dura:** un test `deliberation` con panel > 150 está mal diseñado. Si necesitás más, es `hybrid` o `forecast`.

### 3.7 `setting` (nuevo campo)

El **entorno físico/virtual** donde ocurre la interacción. Distinto de venue (que describe canales y reglas). El setting afecta el tono de los mensajes, la latencia entre turnos, y el tipo de non-verbal implícito.

```yaml
setting:
  category: in_person_meeting     # ver catálogo abajo
  description: >
    Sala de reunión profesional. GP presenta deck frente a IC del LP.
    3-5 personas del lado LP, 1-2 del lado GP. Duración típica 60-90 min.
    Se toman notas. Non-verbals importan. Follow-up es por email/call.
  message_tone_defaults:
    formality: high
    technical_density: high
    emotion_expression: low
    hedging_norm: moderate     # cuánto hedging es natural en este setting
  non_verbal_signals_accepted: true    # el agent puede "notar" que otro se puso tenso
  latency_between_turns: short          # short (minutes) | medium (hours) | long (days)
```

#### 3.7.1 Catálogo de settings (v0)

| setting.category | Descripción | Ejemplos de venues que lo usan |
|---|---|---|
| `in_person_meeting` | Sala física, cara a cara, tiempo continuo | pitch_meeting, b2b_sales_cycle (demo) |
| `in_person_panel` | Escenario, audiencia, varios hablantes | town_hall (hearings), debate |
| `digital_feed` | Timeline algorítmico, posts cortos, emoción alta | social_viral, polarized_social |
| `digital_threaded` | Forums, Reddit, comments largos | press_cycle (comments), community |
| `email_async` | Email chains, formal, slow | b2b_sales_cycle (procurement), crisis (regulator) |
| `messaging_private` | DM, WhatsApp, grupos cerrados | electoral_ecosystem (family WhatsApp), b2b_sales_cycle (internal Slack) |
| `broadcast_one_to_many` | Press release, CEO statement, announcement | press_cycle, crisis_response (official) |
| `retail_context` | Punto de compra, decisión individual, exposure breve | retail_decision |
| `phone_support` | Llamada sincrónica 1-on-1 | support_ticket (call mode) |
| `hybrid_multi_channel` | Varios settings simultáneos | split_public_private (crisis), electoral_ecosystem |

Cada setting lleva defaults de tono que el prompt de generación de acciones hereda automáticamente. Así no hay que repetir en cada prompt "sé formal, técnico, hedged".

### 3.8 `venue`

El **venue** es la capa lógica: canales permitidos, quién ve qué, cómo se alternan los turnos, cómo se propaga la info. Es el mecanismo de la interacción.

```yaml
venue:
  reference: "venues/pitch_meeting.yaml"   # venue puede referenciar el catálogo central

  channels:
    - id: dd_question
      description: "Due-diligence question pública en la reunión"
      message_length: {min_words: 20, max_words: 150}
      visibility: all_attendees
      formality: high

    - id: ic_memo_internal
      description: "Memo interno del LP post-meeting circulado entre IC members"
      message_length: {min_words: 100, max_words: 400}
      visibility: own_lp_firm_only
      formality: very_high

    - id: dm_to_gp
      description: "DM privado al GP con follow-up question específica"
      message_length: {min_words: 15, max_words: 80}
      visibility: sender_and_gp_only
      formality: medium

    - id: peer_dm_crosslp
      description: "DM privado entre LPs discutiendo el pitch"
      message_length: {min_words: 15, max_words: 80}
      visibility: dyadic_between_lps
      frequency_cap: rare      # sucede poco — LPs no siempre cotillean
      formality: medium_low

  visibility_matrix:
    # qué canal ve qué tipo de agente
    gp:
      sees: [dd_question, dm_to_gp]
      does_not_see: [ic_memo_internal, peer_dm_crosslp]
    lp_primary:
      sees: [dd_question, own_ic_memos, dms_sent_received, peer_dms_involved]
    ecosystem_law_firm:
      sees: [dd_question_if_invited]
      does_not_see: [ic_memos, dms]

  turn_dynamics:
    mode: structured_then_async
    phases:
      - phase: pitch_delivery
        rounds: 1
        actor: gp
        channel: stimulus_delivery
      - phase: live_qa
        rounds: 4-6
        actor: lp_primary (rotation weighted by engagement_probability)
        channel: dd_question
      - phase: post_meeting_internal
        rounds: 3-5
        actor: lp_primary (all, parallel)
        channel: ic_memo_internal
      - phase: followup_private
        rounds: 5-10
        actor: lp_primary (subset)
        channel: dm_to_gp

  propagation_rules:
    dd_question_response: "gp responds conceptually based on brief (no LLM for GP in v0)"
    cross_lp_influence: "minimal — LPs evalúan independientemente"
    info_leakage: "none — confidencialidad del pitch se respeta"
```

#### 3.8.1 Catálogo de venues (v0)

Los 13 venues del brief original, cada uno con setting por default y los test_types que lo usan:

| Venue | Setting default | Test_types |
|---|---|---|
| `pitch_meeting` | in_person_meeting | investor_pitch |
| `retail_decision` | retail_context | pricing_test, product_launch (partial) |
| `social_viral` | digital_feed | campaign_planning, brand_sentiment_shift, creative_test |
| `support_ticket` | phone_support + email_async | churn_analysis, crisis_response (partial) |
| `b2b_sales_cycle` | hybrid_multi_channel (demo + Slack + email) | b2b_pricing |
| `town_hall` | in_person_panel + digital_threaded | policy_rollout |
| `electoral_ecosystem` | hybrid_multi_channel | electoral_sentiment |
| `press_cycle` | broadcast_one_to_many + digital_threaded | crisis_response, narrative_framing |
| `polarized_social` | digital_feed | controversial_launch |
| `product_usage_simulation` | individual_journey | product_launch |
| `cross_audience_comparison` | individual_journey_parallel | audience_targeting |
| `split_public_private` | hybrid_multi_channel | crisis_response |
| `campaign_exposure_mix` | hybrid_multi_channel | campaign_planning |

### 3.9 `stimulus`

```yaml
stimulus:
  formats_accepted:
    - pdf
    - text_paste
  formats_rejected_with_message:
    - video: "investor_pitch acepta video solo en tier Ultra (v1+)"
    - image: "imágenes solo como complemento del PDF"

  required_fields:
    - pitch_deck_file
    - check_size_target
    - raise_total_target
    - fund_thesis_one_paragraph

  optional_fields:
    - track_record
    - team_bios
    - market_research_attached

  delivery_format:
    round_1_content: "GP presenta deck + statement de apertura (inferido del brief)"
    max_pages_panel_sees: 30
    extraction_method: vision_llm_plus_text    # claude-sonnet vision extracts if PDF has charts
```

### 3.10 `metrics`

```yaml
metrics:
  primary:
    - follow_up_meeting_intent_pct
    - check_size_floated_distribution
    - red_flags_ranked
    - term_sheet_likelihood_by_segment
    - ask_clarity_score

  secondary:
    - competitive_benchmark_mentions
    - geographic_comfort_gap
    - esg_sensitivity_distribution
    - operational_skepticism_level

  never_emphasize:
    - raw_sentiment_score           # no es el metric que el buyer necesita
    - viral_coefficient             # N/A para pitch privado
    - boycott_probability           # N/A

  aggregation_rules:
    follow_up_meeting_intent_pct:
      computation: "% of LPs that said yes to follow-up"
      confidence: "bootstrap 1000, 90% CI"
      breakdown_by: [archetype, geography, check_size]
```

### 3.11 `report`

```yaml
report:
  required_sections:
    - executive_summary
    - context_of_experiment
    - reaction_by_segment           # 1 subsection por archetype
    - variant_ranking               # si hay A/B
    - red_flags
    - strongest_elements
    - actionable_recommendations
    - what_to_monitor
    - honest_caveats
    - appendices

  optional_sections:
    - ideal_investor_profile_reverse_engineered
    - re_pitch_per_segment_recommendations

  length_target:
    min_words: 5000
    target_words: 6500

  quote_requirements:
    min_validated: 15
    validation_method: embedding_similarity_or_rapidfuzz
    threshold_embedding: 0.85
    threshold_rapidfuzz: 90

  unique_sections:
    - ideal_investor_profile_reverse_engineered
    - re_pitch_per_segment_recommendations

  language_policy:
    default: match_intake_locale
    quotes_preserve_original: true
```

### 3.12 `one_pager`

Estructura fija compartida entre todos los test_types.

```yaml
one_pager:
  structure: SHARED_V1              # referencia a spec compartida
  length: {min_words: 400, max_words: 600}
  sections:
    - decision: {label: "Decisión", length_max_words: 30}
    - top_insights: {label: "Top 3 insights", items: 3, item_length_max_words: 25}
    - actions: {label: "3 acciones para el lunes 9am", items: 3, format: "verb + object + measure"}
    - monitor: {label: "Qué mirar la próxima semana", length_words: 40-80}
    - caveats: {label: "Caveats honestos", length_words: 30-60}
```

### 3.13 `qa_review`

Esta es la parte crítica del anti-hallucination. Cada stage del pipeline pasa por un QA LLM-based antes de avanzar. La DNA declara qué checks corren.

```yaml
qa_review:
  # Post Stage 2 (Environment build)
  post_stage_2:
    checks:
      - phantom_entities:
          method: "llm + local_ner + pattern_filter"
          auto_fix: remove_on_high_confidence
          escalate_on: "phantom detected with < 0.8 confidence"
          budget_usd: 0.15

      - off_target_archetype:
          method: "llm compares persona.archetype_label vs persona.bio"
          prompt: "¿Esta persona es un matche legítimo para el archetype 'X'? Responder solo si hay clear mismatch."
          auto_fix: regenerate_variant
          escalate_on: "2+ variants of same anchor fail"

      - law_firm_plausibility:             # custom check para investor_pitch
          method: "llm"
          prompt: "¿Este law firm trabaja con LPs institucionales en el mercado geográfico del deal?"
          auto_fix: remove
          escalate_on: "> 20% of law firms flagged"

      - ecosystem_balance:
          method: "count_by_type vs ecosystem_spec"
          auto_fix: request_regen_of_missing_types
          escalate_on: "missing >1 required type after retry"

      - duplicates_encoding:
          method: "local — dedup by lowered name, encoding normalize"
          auto_fix: always

    halt_threshold:
      total_issues_for_halt_alert: 5
      critical_issue_types: [phantom_above_10pct, balance_violated]

  # Post Stage 4 (Simulation) — solo si mode=deliberation o hybrid
  post_stage_4:
    checks:
      - persona_coherence:
          method: "llm reviews actions of each agent against persona bio"
          scope: "sample 20% of agents + 100% of high-activity agents"
          flag_types:
            - character_break: "agente actúa contra su valor declarado (ej. ESG allocator apoyando una weapons deal)"
            - competitor_support: "competidor apoyando activamente al subject del test"
            - knowledge_mismatch: "agent cita datos que no podría saber (ej. un US endowment citando specifics de una ley argentina que no conocería sin research)"
          auto_fix: regenerate_action
          escalate_on: "> 5% of actions flagged"

      - factual_hallucination:
          method: "embedding_similarity vs stimulus + llm check of claimed facts"
          flag_types:
            - invented_law: "cita ley, regulación, o institución que no existe"
            - invented_number: "cita número específico no respaldado por stimulus"
          auto_fix: remove_action
          escalate_on: ">= 1 invented_law OR > 3% invented_number"

      - language_drift:
          method: "local language detector per action"
          auto_fix: regenerate_in_correct_locale
          escalate_on: "> 5% off-locale"

      - copy_propagation:
          method: "embedding_similarity between actions of distinct agents"
          threshold: 0.92
          auto_fix: regenerate_duplicate
          escalate_on: "> 5% of actions have a duplicate"

      - on_topic:
          method: "embedding_similarity action vs stimulus topic"
          threshold: 0.35
          auto_fix: flag_for_exclusion_from_report
          escalate_on: "> 20% off-topic"

      - dominance:
          method: "action_count per agent / total_actions"
          threshold: 0.30
          auto_fix: weight_redistribution_next_rounds
          escalate_on: "agent > 40% of actions"

  # Post Stage 6 (Narratives)
  post_stage_6:
    checks:
      - quote_validation:
          method: "100% of quotes in narrative matched vs sim log"
          auto_fix: force_rewrite_remove_unmatched
          escalate_on: "> 10% unmatched after 1 retry"

      - exaggeration:
          method: "llm compares narrative tone vs raw sim sentiment"
          prompt: "¿La narrativa amplifica o dramatiza sentimientos que en la sim cruda eran neutrales o leves?"
          auto_fix: request_rewrite_with_less_drama
          escalate_on: "narrative diverges > 2 std dev from sim aggregate"

      - agent_attribution:
          method: "llm verifies quote → agent mapping"
          auto_fix: fix_attribution
          escalate_on: "> 5% misattributed"

  # Post Stage 7 (Executive judge)
  post_stage_7:
    checks:
      - winner_confidence_calibration:
          method: "compare quantitative gap top-2 vs judge verdict strength"
          rule: "if confidence < 60 → verdict must include hedging language"
          auto_fix: re_ask_with_calibration_instruction
          escalate_on: "miscalibration detected"

      - caveat_erosion:
          method: "llm checks caveats section against known limits from DNA + warnings from gates"
          auto_fix: insert_missing_caveats
          escalate_on: "> 3 caveats missing"

      - optimism_bias:
          method: "llm reads report and flags 'everything is great' language when data contradicts"
          auto_fix: re_ask_with_balance_instruction
          escalate_on: "report tone contradicts winner_confidence < 60"

      - structural_compliance:
          method: "regex check required_sections markers"
          auto_fix: re_ask_with_missing_sections
          escalate_on: "still missing after retry"

  # Anti-bias invariants — aplican a todos los post_stage_X
  anti_bias_invariants:
    - "QA no modifica opiniones del panel — solo coherencia y factualidad"
    - "Toda corrección se loguea con razón explícita en el event log"
    - "QA no transforma bearish → bullish ni vice versa"
    - "Si un agent legítimamente dice algo inusual pero coherente con su persona, se mantiene"
    - "El reporte final menciona: N correcciones aplicadas (sin detalles que filtren info)"
```

### 3.14 `tier_overrides`

Qué cambia de la DNA base según el tier pago.

```yaml
tier_overrides:
  economy:
    simulation:
      panel_size: {default: 32}      # smaller panel
      rounds: {default: 15}
    multi_run: 1
    models:
      amplifier: economy_structured     # ver LLM routing table
      persona_generator: economy
      sim_agent_action: economy
      interview: economy
      narrative: pro
      executive_judge: pro              # no ultra
      qa_reviewer: economy_structured

  pro:
    simulation: {panel_size: {default: 48}, rounds: {default: 20}}
    multi_run: 3
    models:
      amplifier: pro
      persona_generator: pro
      sim_agent_action: pro
      interview: pro
      narrative: pro
      executive_judge: premium          # reasoning-heavy
      qa_reviewer: pro

  premium:
    simulation: {panel_size: {default: 64}, rounds: {default: 25}}
    multi_run: 5
    models:
      amplifier: premium
      persona_generator: premium
      sim_agent_action: pro             # cost control — scale con N
      interview: premium
      narrative: premium
      executive_judge: ultra
      qa_reviewer: premium

  ultra:
    simulation: {panel_size: {default: 80}, rounds: {default: 30}}
    multi_run: 10
    models:
      amplifier: ultra
      persona_generator: ultra
      sim_agent_action: premium
      interview: ultra
      narrative: ultra
      executive_judge: ultra
      qa_reviewer: ultra
    features_unlocked:
      - multi_modal_stimulus_video_audio
      - multi_language_panel
      - agent_memory_across_tests
      - live_operator_intervention
```

### 3.15 `limits`

Caveats estáticos — lo que el test estructuralmente NO puede decir. Se insertan automáticamente en la sección "caveats" del reporte final.

```yaml
limits:
  - "NO puede predecir si el raise cierra — depende de condiciones macro fuera del panel"
  - "NO puede evaluar competencia concreta en tiempo real (otro fondo raising simultáneamente)"
  - "Panel no captura química personal de la reunión IRL ni chemistry del GP en vivo"
  - "Los LPs simulados reflejan mandatos/conocimiento público — posiciones internas actuales pueden diferir"
  - "El test no sustituye due diligence legal, fiscal, o de background checks del GP"
```

### 3.16 `cross_test_learning`

```yaml
cross_test_learning:
  patterns_to_extract:
    count_per_test: 5-10
    examples:
      - "fee_transparency_sensitivity"
      - "geographic_preference_pattern"
      - "track_record_threshold_implicit"

  priors_relevance:
    window: "tests_same_client_same_test_type_last_12_months"
    max_priors_injected: 8

  scoping_rules:
    strict: "priors NEVER cross test_type boundaries"
    strict: "priors NEVER cross client boundaries (unless explicit benchmark opt-in)"
```

### 3.17 `pricing_recommendation`

Hint para el operator / intake form — qué tier tiene más sentido para este test_type.

```yaml
pricing_recommendation:
  default_tier: pro
  upgrade_triggers:
    - trigger: "raise_total_target > 100M_usd"
      suggest: premium
    - trigger: "raise_total_target > 500M_usd OR first_institutional_raise"
      suggest: ultra
  downgrade_acceptable:
    - trigger: "raise_total_target < 10M_usd AND exploratory"
      suggest: economy
```

### 3.18 `prompts`

Referencia a los YAMLs de prompts. La DNA no contiene prompts — los delega. Esto permite portar los 75 YAMLs de MiroFish sin tocar la DNA.

```yaml
prompts:
  intake_schema: "prompts/investor_pitch/intake.yaml"
  amplifier: "prompts/investor_pitch/amplifier.yaml"
  entity_extractor: "prompts/investor_pitch/entity_extractor.yaml"
  persona_generator: "prompts/investor_pitch/persona.yaml"
  stimulus_delivery: "prompts/investor_pitch/stimulus_delivery.yaml"
  agent_action_dd_question: "prompts/investor_pitch/action_dd_question.yaml"
  agent_action_ic_memo: "prompts/investor_pitch/action_ic_memo.yaml"
  agent_action_dm: "prompts/investor_pitch/action_dm.yaml"
  interview: "prompts/investor_pitch/interview.yaml"
  narrative_per_variant: "prompts/investor_pitch/narrative.yaml"
  executive_judge: "prompts/investor_pitch/executive_judge.yaml"
  one_pager: "prompts/shared/one_pager_v1.yaml"
  qa_reviewer: "prompts/shared/qa_reviewer_v1.yaml"
```

---

## 4. Ejemplos completos

### 4.1 Ejemplo A — `investor_pitch` (modo deliberation + in_person_meeting)

```yaml
# dna/investor_pitch.yaml

test_type: investor_pitch
version: "1.0.0"
status: active

client_facing:
  one_liner: "Validar si un pitch deck está listo para roadshow LP antes de gastar tiempo y reputación."
  decision_question: "¿Salir a roadshow formal con este deck, o volver al drawing board?"
  buyer_profile:
    - "Fundador o GP de fondo que está por levantar $10M-$1B"
    - "Head of IR / capital formation en fondo establecido"
  typical_trigger: "Pre-roadshow LP, 2-6 semanas antes de primeras reuniones"
  decision_outputs: [GO, CONDITIONAL_GO, DELAY_AND_FIX, NO_GO]

panel:
  anchors_spec:
    count: {min: 6, max: 8, recommended: 8}
    examples:
      - "LP institucional — agri specialist (tipo TIAA/Nuveen)"
      - "LP sovereign wealth — food security mandate"
      - "Family office — Argentino/LatAm"
      - "US Endowment / foundation allocator"
      - "Agri PE GP emeritus"
      - "LatAm-skeptic US HNW investor"
      - "Brazilian agri family office"
      - "Impact / ESG allocator"

  ecosystem_spec:
    extract_from_stimulus: true
    target_types:
      - {type: law_firm, count: "3-5"}
      - {type: media_trade, count: "3-5"}
      - {type: comparable_company, count: "5-8"}
      - {type: regulator, count: "1-3"}

  amplification:
    strategy: deterministic_llm
    target_pool: 48
    per_anchor_cap: [2, 15]

  composition_targets:
    primary_panel_pct: {min: 50, max: 60}
    ecosystem_pct: {min: 15, max: 25}
    context_pct: {min: 20, max: 30}

  exclude_entity_types:
    - ConsumerBrand
    - RetailCustomer
    - IndividualInvestorRetail
    - InfluencerSocialMedia

  quality_requirements:
    bio_length_min_words: 300
    bio_length_target_words: 450

simulation:
  mode: deliberation
  panel_size: {default: 48, min: 32, max: 80}
  duration: {simulated_time: "pitch_day + 7d_followup", wall_clock_target_minutes: 12}
  rounds: {min: 15, default: 20, max: 30}
  propagation: {type: venue_rules, cross_agent_visibility: controlled}

setting:
  category: in_person_meeting
  description: >
    Sala de reunión profesional. GP presenta deck frente a IC del LP.
    3-5 personas del lado LP, 1-2 del lado GP. Duración 60-90 min.
    Post-meeting: IC memos internos + follow-up privado.
  message_tone_defaults:
    formality: high
    technical_density: high
    emotion_expression: low
    hedging_norm: moderate
  non_verbal_signals_accepted: true
  latency_between_turns: short

venue:
  reference: "venues/pitch_meeting.yaml"
  channels:
    - {id: dd_question, visibility: all_attendees, length_words: "20-150", formality: high}
    - {id: ic_memo_internal, visibility: own_lp_firm_only, length_words: "100-400", formality: very_high}
    - {id: dm_to_gp, visibility: sender_and_gp_only, length_words: "15-80", formality: medium}
    - {id: peer_dm_crosslp, visibility: dyadic_between_lps, length_words: "15-80", frequency_cap: rare}

  turn_dynamics:
    mode: structured_then_async
    phases:
      - {phase: pitch_delivery, rounds: 1, actor: gp, channel: stimulus_delivery}
      - {phase: live_qa, rounds: "4-6", actor: lp_primary, channel: dd_question}
      - {phase: post_meeting_internal, rounds: "3-5", actor: lp_primary_all, channel: ic_memo_internal}
      - {phase: followup_private, rounds: "5-10", actor: lp_primary_subset, channel: dm_to_gp}

stimulus:
  formats_accepted: [pdf, text_paste]
  required_fields: [pitch_deck_file, check_size_target, raise_total_target, fund_thesis_one_paragraph]
  delivery_format: {round_1_content: "GP presenta deck + statement", max_pages: 30, extraction: vision_llm_plus_text}

metrics:
  primary:
    - follow_up_meeting_intent_pct
    - check_size_floated_distribution
    - red_flags_ranked
    - term_sheet_likelihood_by_segment
    - ask_clarity_score
  secondary:
    - competitive_benchmark_mentions
    - geographic_comfort_gap
    - esg_sensitivity_distribution
  never_emphasize: [raw_sentiment_score, viral_coefficient, boycott_probability]

report:
  required_sections:
    [executive_summary, context_of_experiment, reaction_by_segment, variant_ranking,
     red_flags, strongest_elements, actionable_recommendations, what_to_monitor,
     honest_caveats, appendices]
  unique_sections:
    [ideal_investor_profile_reverse_engineered, re_pitch_per_segment_recommendations]
  length_target: {min_words: 5000, target_words: 6500}
  quote_requirements: {min_validated: 15, threshold_embedding: 0.85}
  language_policy: {default: match_intake_locale, quotes_preserve_original: true}

one_pager:
  structure: SHARED_V1
  length: {min_words: 400, max_words: 600}

qa_review:
  post_stage_2:
    checks:
      - {name: phantom_entities, auto_fix: remove_on_high_confidence, escalate_on: "phantom < 0.8 confidence"}
      - {name: off_target_archetype, auto_fix: regenerate_variant}
      - {name: law_firm_plausibility, auto_fix: remove, escalate_on: "> 20% flagged"}
      - {name: ecosystem_balance, auto_fix: request_regen}
      - {name: duplicates_encoding, auto_fix: always}

  post_stage_4:
    checks:
      - {name: persona_coherence, scope: "20% sample + high-activity 100%"}
      - {name: factual_hallucination, critical: invented_law}
      - {name: competitor_coherence, escalate_on: "competidor aparece apoyando el deal"}
      - {name: language_drift, escalate_on: "> 5% off-locale"}
      - {name: copy_propagation, threshold: 0.92}
      - {name: on_topic, threshold: 0.35}
      - {name: dominance, threshold: 0.30}

  post_stage_6:
    checks:
      - {name: quote_validation, critical: true}
      - {name: exaggeration}
      - {name: agent_attribution}

  post_stage_7:
    checks:
      - {name: winner_confidence_calibration, critical: true}
      - {name: caveat_erosion}
      - {name: optimism_bias}
      - {name: structural_compliance}

tier_overrides:
  economy: {multi_run: 1, panel_size_default: 32, rounds_default: 15}
  pro: {multi_run: 3, panel_size_default: 48, rounds_default: 20}
  premium: {multi_run: 5, panel_size_default: 64, rounds_default: 25}
  ultra: {multi_run: 10, panel_size_default: 80, rounds_default: 30, features: [multi_lang, agent_memory]}

limits:
  - "NO puede predecir si el raise cierra — depende de condiciones macro"
  - "NO evalúa competencia simultánea (otro fondo raising al mismo tiempo)"
  - "No captura chemistry del GP en vivo"
  - "Posiciones internas actuales de LPs pueden diferir de mandato público"
  - "No sustituye DD legal, fiscal, o background checks"

cross_test_learning:
  patterns_to_extract: {count_per_test: "5-10"}
  priors_relevance: {window: "same_client_same_type_12mo", max_injected: 8}

pricing_recommendation:
  default_tier: pro
  upgrade_triggers:
    - {trigger: "raise_total > 100M", suggest: premium}
    - {trigger: "raise_total > 500M OR first_institutional_raise", suggest: ultra}

prompts:
  intake_schema: "prompts/investor_pitch/intake.yaml"
  amplifier: "prompts/investor_pitch/amplifier.yaml"
  entity_extractor: "prompts/investor_pitch/entity_extractor.yaml"
  persona_generator: "prompts/investor_pitch/persona.yaml"
  stimulus_delivery: "prompts/investor_pitch/stimulus_delivery.yaml"
  agent_action_dd_question: "prompts/investor_pitch/action_dd_question.yaml"
  agent_action_ic_memo: "prompts/investor_pitch/action_ic_memo.yaml"
  agent_action_dm: "prompts/investor_pitch/action_dm.yaml"
  interview: "prompts/investor_pitch/interview.yaml"
  narrative_per_variant: "prompts/investor_pitch/narrative.yaml"
  executive_judge: "prompts/investor_pitch/executive_judge.yaml"
  one_pager: "prompts/shared/one_pager_v1.yaml"
  qa_reviewer: "prompts/shared/qa_reviewer_v1.yaml"
```

### 4.2 Ejemplo B — `pricing_test` (modo survey_batch + retail_context)

Demuestra: panel grande (500-1000), 1 ronda, sin deliberation cross-agent, cost-efficient.

```yaml
# dna/pricing_test.yaml

test_type: pricing_test
version: "1.0.0"
status: active

client_facing:
  one_liner: "Testear 2-5 precios distintos para descubrir el punto óptimo de intent-to-buy."
  decision_question: "¿A qué precio lanzamos?"
  buyer_profile:
    - "CMO o Head of Product de marca de consumo"
    - "Head of Growth / Pricing lead en SaaS consumer"
  typical_trigger: "Pre-launch de producto, re-pricing de línea existente"
  decision_outputs: [GO_PRICE_A, GO_PRICE_B, GO_PRICE_C, NEED_MORE_DATA]

panel:
  anchors_spec:
    count: {min: 5, max: 8}
    examples:
      - "Consumer regular del target demographic"
      - "Opinion leader / reviewer del category"
      - "Critic / skeptic price-sensitive"
      - "Brand loyalist de competidor"
      - "Early adopter tech-forward"

  ecosystem_spec:
    extract_from_stimulus: true
    target_types:
      - {type: competing_brand, count: "3-5"}
      - {type: retailer_category, count: "2-3"}
      - {type: review_platform, count: "1-2"}

  amplification:
    strategy: deterministic_llm
    target_pool: 800                     # MUCHO MAYOR que deliberation
    per_anchor_cap: [80, 200]

  composition_targets:
    consumers_regular_pct: {min: 65, max: 75}
    opinion_leaders_pct: {min: 8, max: 12}
    critics_pct: {min: 8, max: 12}
    media_pct: {min: 5, max: 10}

  exclude_entity_types:
    - InvestorFund
    - RegulatorGovernmentAgency
    - CorporateProcurement

  quality_requirements:
    bio_length_min_words: 150            # más chico que deliberation (no necesita tanta profundidad)
    bio_length_target_words: 200

simulation:
  mode: survey_batch                     # KEY DIFFERENCE
  panel_size: {default: 800, min: 200, max: 2000}
  duration: {wall_clock_target_minutes: 10}
  rounds: 1                              # SOLO 1 ROUND
  propagation: {type: none}              # NO cross-agent interaction

  survey_config:
    questions_ref: "prompts/pricing_test/survey_questions.yaml"
    response_format: structured          # pydantic schema
    batch_size: 100                      # agents batched por LLM call
    parallelism: 50

setting:
  category: retail_context
  description: >
    El agente "encuentra" el producto en su contexto de compra habitual
    (supermercado, e-commerce, local físico). Tiene exposure breve,
    decide individualmente, puede comentar post-decisión pero NO interactúa
    con otros agents del panel en real-time.
  message_tone_defaults:
    formality: low
    technical_density: low
    emotion_expression: moderate
    hedging_norm: low
  non_verbal_signals_accepted: false
  latency_between_turns: N/A              # no hay turnos

venue:
  reference: "venues/retail_decision.yaml"
  channels:
    - {id: decision_monologue, visibility: private_internal, length_words: "50-150", formality: low}
    - {id: review_public, visibility: all, length_words: "20-100", frequency: "50% of agents"}
    - {id: wom_private, visibility: dyadic_same_segment, length_words: "15-50", frequency: "30% of agents"}

  turn_dynamics:
    mode: batch_parallel
    phases:
      - {phase: stimulus_encounter, rounds: 1, actor: all_agents_parallel, channel: decision_monologue}
      - {phase: optional_share, rounds: 1, actor: subset, channel: [review_public, wom_private]}

stimulus:
  formats_accepted: [pdf, image, text_paste]
  required_fields: [product_description, pricing_variants, packaging_image_optional]
  variants_min: 2
  variants_max: 5
  delivery_format: {one_variant_per_agent: random_assignment_weighted, extraction: vision_llm}

metrics:
  primary:
    - intent_to_buy_pct_by_variant
    - price_elasticity_between_variants
    - willingness_to_pay_ceiling
    - reasons_to_reject_ranked
    - upsell_accept_rate
  secondary:
    - segment_price_sensitivity_clusters
    - brand_association_strength_delta
    - competitor_comparison_mentions
  never_emphasize: [deliberation_dynamics, inflection_points, cascade_detection]

report:
  required_sections:
    [executive_summary, context_of_experiment, demand_curve, segmentation_by_sensitivity,
     variant_ranking, reasons_to_reject, strongest_elements, anchor_pricing_recommendations,
     what_to_monitor, honest_caveats, appendices]
  unique_sections:
    [estimated_demand_curve, price_sensitivity_clusters, anchor_pricing]
  length_target: {min_words: 4500, target_words: 5500}
  quote_requirements: {min_validated: 20}     # MÁS quotes porque hay MÁS agents
  language_policy: {default: match_intake_locale}

one_pager: {structure: SHARED_V1, length: {min_words: 400, max_words: 600}}

qa_review:
  post_stage_2:
    checks:
      - phantom_entities
      - off_target_archetype
      - demographic_distribution_sanity     # custom para survey: ¿la distribución refleja el target?
      - duplicates_encoding

  post_stage_4:
    checks:
      - response_coherence                  # ¿las respuestas matchean el persona?
      - factual_hallucination
      - language_drift
      - duplicate_responses                 # muchos agents no pueden dar la misma respuesta literal
      - structured_output_compliance        # responses follow schema

  post_stage_6:
    checks:
      - quote_validation
      - distribution_vs_narrative           # ¿la narrativa refleja la distribución real?
      - exaggeration

  post_stage_7:
    checks:
      - winner_confidence_calibration
      - caveat_erosion
      - optimism_bias
      - structural_compliance

tier_overrides:
  economy: {multi_run: 1, panel_size_default: 200}
  pro: {multi_run: 3, panel_size_default: 800}
  premium: {multi_run: 5, panel_size_default: 1500}
  ultra: {multi_run: 10, panel_size_default: 2000, features: [multi_modal_package]}

limits:
  - "Intent-to-buy simulated ≠ actual purchase — gap típico 20-40%"
  - "No captura efecto competitivo dinámico (precio del rival podría cambiar)"
  - "No mide repeat purchase — solo first-buy"
  - "No incluye channel dynamics (retailer margin, shelf placement)"
  - "Price elasticity estimada es direccional, no absoluta"

cross_test_learning:
  patterns_to_extract: {count_per_test: "5-10"}
  priors_relevance: {window: "same_client_same_category_12mo", max_injected: 8}

pricing_recommendation:
  default_tier: pro
  upgrade_triggers:
    - {trigger: "product_launch_budget > 10M OR first_of_line", suggest: premium}

prompts:
  intake_schema: "prompts/pricing_test/intake.yaml"
  amplifier: "prompts/pricing_test/amplifier.yaml"
  entity_extractor: "prompts/pricing_test/entity_extractor.yaml"
  persona_generator: "prompts/pricing_test/persona.yaml"
  survey_questions: "prompts/pricing_test/survey_questions.yaml"
  response_generator: "prompts/pricing_test/response.yaml"
  narrative_per_variant: "prompts/pricing_test/narrative.yaml"
  executive_judge: "prompts/pricing_test/executive_judge.yaml"
  one_pager: "prompts/shared/one_pager_v1.yaml"
  qa_reviewer: "prompts/shared/qa_reviewer_v1.yaml"
```

### 4.3 Ejemplo C — `crisis_response` (modo deliberation + hybrid_multi_channel)

Demuestra: multi-canal simultáneo, varios settings mezclados, timing crítico, NO-GO legítimo.

```yaml
# dna/crisis_response.yaml

test_type: crisis_response
version: "1.0.0"
status: active

client_facing:
  one_liner: "Evaluar variantes de respuesta a una crisis de reputación antes de enviar la respuesta real."
  decision_question: "¿Cómo respondemos al crisis? ¿O mejor silencio con action slow?"
  buyer_profile:
    - "Head of comms / PR lead"
    - "CEO / COO en crisis management"
    - "PR firm con cliente en crisis"
  typical_trigger: "Durante o post crisis (first 48h son críticos)"
  decision_outputs: [GO_VARIANT_A, GO_VARIANT_B, GO_VARIANT_C, GO_SILENCE, NO_GO_ALL]

panel:
  anchors_spec:
    count: {min: 6, max: 8}
    examples:
      - "Afectado directo (customer con daño real)"
      - "Público general interesado"
      - "Periodista de trade press"
      - "Regulator / watchdog relevante"
      - "Advocacy group / activist"
      - "Competidor observando"
      - "Empleado interno"
      - "Shareholder / inversor"

  ecosystem_spec:
    extract_from_stimulus: true
    target_types:
      - {type: competitor, count: "2-4"}
      - {type: regulator, count: "1-3"}
      - {type: advocacy_group, count: "1-3"}
      - {type: media_outlet, count: "5-8"}
      - {type: class_action_law_firm, count: "1-2"}

  amplification:
    strategy: deterministic_llm
    target_pool: 80
    per_anchor_cap: [5, 15]

  composition_targets:
    affected_pct: {min: 25, max: 35}
    general_public_pct: {min: 15, max: 25}
    press_pct: {min: 12, max: 18}
    regulator_pct: {min: 10, max: 18}
    advocacy_pct: {min: 8, max: 12}
    competitor_pct: {min: 5, max: 10}

  exclude_entity_types:
    - UnrelatedConsumerCategory
    - DistantInternationalMarket_not_involved

simulation:
  mode: deliberation
  panel_size: {default: 80, min: 60, max: 120}
  duration: {simulated_time: "10d_post_response", wall_clock_target_minutes: 15}
  rounds: {min: 18, default: 24, max: 30}
  propagation: {type: venue_rules, cross_agent_visibility: mixed}

setting:
  category: hybrid_multi_channel
  description: >
    Crisis requiere respuesta simultánea en múltiples canales:
    press conference (broadcast), customer support (1-on-1),
    social media (digital feed), regulator engagement (email_async).
    Cada canal tiene tono y latency propios.
  channels_with_settings:
    press_conference: {setting: broadcast_one_to_many, formality: high}
    customer_support: {setting: phone_support_or_email, formality: medium}
    social_response: {setting: digital_feed, formality: low_to_medium}
    regulator_engagement: {setting: email_async, formality: very_high}
    internal_memo: {setting: email_async, formality: medium_high}

venue:
  reference: "venues/split_public_private.yaml"
  channels:
    - {id: press_statement, visibility: all, length_words: "100-400", formality: high, frequency: per_variant_once}
    - {id: journalist_writeup, visibility: all, length_words: "200-600", formality: high, actor_type: press}
    - {id: public_social_reaction, visibility: all, length_words: "20-150", formality: low, actor_type: affected_or_public}
    - {id: support_ticket_reply, visibility: customer_and_support, length_words: "50-200", formality: medium, actor_type: affected_or_support}
    - {id: regulator_formal_letter, visibility: regulator_and_company, length_words: "200-500", formality: very_high, actor_type: regulator}
    - {id: advocacy_press_release, visibility: all, length_words: "200-500", formality: medium_high, actor_type: advocacy}
    - {id: competitor_positioning, visibility: all, length_words: "50-200", formality: medium, actor_type: competitor, frequency_cap: low}
    - {id: internal_leak, visibility: all, length_words: "100-300", formality: low, actor_type: employee, frequency_cap: rare}

  visibility_matrix:
    # Resumen: casi todo público, excepción regulator (privado), support (privado customer-company), internal_memo (privado empleados)
    affected:
      sees: [press_statement, journalist_writeup, public_social, their_own_support_reply, advocacy_press, competitor_positioning]
    regulator:
      sees: [press_statement, journalist_writeup, own_formal_letter_exchange]
      does_not_see: [support_tickets, internal_leaks_usually]
    competitor:
      sees: [press_statement, journalist_writeup, public_social, advocacy_press]

  turn_dynamics:
    mode: event_driven_with_cascades
    phases:
      - {phase: stimulus_delivery, rounds: 1, actor: company, channel: press_statement}
      - {phase: first_48h, rounds: "8-10", actor: all_parallel_waves, timing: "6h_per_round_simulated"}
      - {phase: coverage_arc, rounds: "8-12", actor: press_and_reactions, timing: "24h_per_round_simulated"}
      - {phase: settlement_or_escalation, rounds: "3-5", actor: regulator_and_legal, timing: "multi_day"}

stimulus:
  formats_accepted: [pdf, text_paste, video_optional_ultra]
  required_fields: [crisis_summary, company_statement_variants, timeline_of_events, affected_parties_description]
  variants_min: 2
  variants_max: 4
  variants_examples_for_intake:
    - "Apology + immediate remediation + compensation fund"
    - "Denial + legal stance + countersuit warning"
    - "Silence + slow action behind scenes"
    - "Counter-narrative + blame external factors"

metrics:
  primary:
    - trust_restoration_pct_by_segment
    - escalation_risk_boycott
    - escalation_risk_class_action
    - escalation_risk_regulator_action
    - narrative_control_score
  secondary:
    - employee_internal_sentiment
    - competitor_opportunistic_moves
    - simulated_press_coverage_arc_10d
  never_emphasize: [vanity_metrics, reach_without_sentiment]

report:
  required_sections:
    [executive_summary, context_of_crisis, variant_comparison, reaction_by_segment,
     simulated_coverage_arc, regulator_action_probability, boycott_risk,
     recommended_variant_with_rationale, what_to_monitor, honest_caveats,
     silence_option_analysis, appendices]
  unique_sections:
    [simulated_press_coverage_arc, regulator_action_probability, silence_option_analysis]
  length_target: {min_words: 5500, target_words: 7000}
  quote_requirements: {min_validated: 18}
  language_policy: {default: match_intake_locale, regional_variants: aware}
  special_output:
    no_go_legitimate: true
    silence_option_always_evaluated: true

one_pager: {structure: SHARED_V1, length: {min_words: 400, max_words: 600}}

qa_review:
  post_stage_2:
    checks:
      - phantom_entities
      - off_target_archetype
      - regulator_jurisdiction_match       # ¿el regulator extraído tiene jurisdicción sobre la empresa?
      - media_outlet_relevance             # ¿el outlet cubre esta industria/geo?
      - duplicates_encoding

  post_stage_4:
    checks:
      - persona_coherence
      - factual_hallucination
      - competitor_coherence               # CRITICAL: competitor no debe apoyar a la empresa en crisis
      - affected_party_coherence           # afectado genuino no debe sonar neutral o positivo sin causa
      - language_drift
      - channel_formality_match            # regulator en formal, social en casual
      - copy_propagation
      - temporal_realism                   # ¿el timing de las respuestas es plausible?
      - cascade_plausibility               # ¿una story muere 24h o tiene legs?

  post_stage_6:
    checks:
      - quote_validation
      - exaggeration
      - agent_attribution
      - coverage_arc_plausibility

  post_stage_7:
    checks:
      - winner_confidence_calibration
      - caveat_erosion
      - optimism_bias
      - no_go_considered                   # verificar que silence/no_go option fue evaluada
      - structural_compliance

tier_overrides:
  economy: {multi_run: 1, panel_size_default: 60, rounds_default: 18}
  pro: {multi_run: 3, panel_size_default: 80, rounds_default: 24}
  premium: {multi_run: 5, panel_size_default: 100, rounds_default: 28}
  ultra: {multi_run: 10, panel_size_default: 120, rounds_default: 30, features: [multi_lang, multi_modal, live_operator_intervention]}

limits:
  - "El test no sustituye asesoramiento legal real de litigation counsel"
  - "Regulators reales tienen información no-pública que el panel no modela"
  - "Crisis dynamics evolutivas (new info emerges hour-by-hour) no están en el test — es snapshot"
  - "El test asume que la respuesta se ejecuta bien — no modela falla de ejecución"
  - "Panel no captura tail risks de celebrities o individuos high-profile con impacto desproporcionado"
  - "Regional/cultural differences en crisis response pueden requerir test per región"

cross_test_learning:
  patterns_to_extract: {count_per_test: "5-10"}
  priors_relevance: {window: "same_client_same_type_24mo", max_injected: 6}

pricing_recommendation:
  default_tier: premium
  notes: "Crisis response rara vez amerita tier economy — el costo de decisión mala es alto"
  upgrade_triggers:
    - {trigger: "exposed_liability > 50M OR public_company", suggest: ultra}

prompts:
  intake_schema: "prompts/crisis_response/intake.yaml"
  amplifier: "prompts/crisis_response/amplifier.yaml"
  entity_extractor: "prompts/crisis_response/entity_extractor.yaml"
  persona_generator: "prompts/crisis_response/persona.yaml"
  stimulus_delivery: "prompts/crisis_response/stimulus_delivery.yaml"
  agent_action_press: "prompts/crisis_response/action_press.yaml"
  agent_action_social: "prompts/crisis_response/action_social.yaml"
  agent_action_support: "prompts/crisis_response/action_support.yaml"
  agent_action_regulator: "prompts/crisis_response/action_regulator.yaml"
  agent_action_advocacy: "prompts/crisis_response/action_advocacy.yaml"
  agent_action_competitor: "prompts/crisis_response/action_competitor.yaml"
  interview: "prompts/crisis_response/interview.yaml"
  narrative_per_variant: "prompts/crisis_response/narrative.yaml"
  executive_judge: "prompts/crisis_response/executive_judge.yaml"
  one_pager: "prompts/shared/one_pager_v1.yaml"
  qa_reviewer: "prompts/shared/qa_reviewer_v1.yaml"
```

---

## 5. Validation rules (CI check)

Antes de aceptar una DNA nueva en el repo, un CI check (en Python con pydantic + custom validators) verifica:

### 5.1 Schema compliance

- Todos los required fields presentes
- Types correctos
- Enum values válidos (simulation.mode ∈ {5 modos}, etc.)

### 5.2 Internal consistency

- `simulation.mode=deliberation` requiere `venue.channels`, `rounds`, `propagation.type=venue_rules`
- `simulation.mode=survey_batch` requiere `simulation.survey_config`, `rounds=1`, `propagation.type=none`
- `simulation.mode=forecast` requiere `simulation.forecast_target`
- `setting.category` debe existir en el catálogo de settings
- `venue.reference` debe apuntar a un archivo que existe en `venues/`
- Todos los `prompts.*` refs deben apuntar a archivos YAML existentes
- `exclude_entity_types` intersección con `panel.composition_targets` → warning si overlap

### 5.3 Coverage checks

- `qa_review` tiene al menos checks para las stages que aplican al modo
- `report.required_sections` incluye las 10 base + `unique_sections`
- `metrics.primary` tiene ≥ 3 items
- `limits` tiene ≥ 3 items
- `tier_overrides` cubre los 4 tiers

### 5.4 Cross-DNA checks (globales)

- No hay dos DNAs con el mismo `test_type` identifier
- Todos los `prompts.one_pager` apuntan al `shared/one_pager_v1.yaml` (consistencia del deliverable base)

### 5.5 Bump de version

- Si el schema cambia incompatible → major bump obligatorio
- CI detecta diffs entre DNA commits y sugiere bump apropiado

---

## 6. Extension guide — agregar un nuevo test_type

Ejemplo: agregar `employee_engagement_survey` como test_type #16.

### Pasos

1. **Analizar el espacio de decisión.** ¿Qué decisión concreta ayuda? ¿Quién la toma?
2. **Elegir `simulation.mode`.** Employee survey es típicamente `survey_batch` puro.
3. **Elegir o crear venue.** Si existe un venue `internal_async_survey`, usarlo. Si no, crear `venues/internal_async_survey.yaml`.
4. **Elegir `setting.category`.** Probablemente `email_async` + `messaging_private` hybrid.
5. **Definir archetypes anchors.** ¿Qué roles / niveles / departments importan?
6. **Definir metrics.** Engagement score, retention risk, manager NPS, ideas count.
7. **Definir report.unique_sections.** Ej. `manager_action_list`, `retention_risk_by_dept`.
8. **Escribir prompts específicos.** En `prompts/employee_engagement_survey/`.
9. **Escribir DNA YAML.** En `dna/employee_engagement_survey.yaml`.
10. **Correr CI validation.**
11. **Test end-to-end con un caso sintético.**
12. **Operator approval para production.**

**Tiempo estimado:** 2-4 días de trabajo para un test_type nuevo standard. Menos si reusa venue/setting existentes.

### Regla de oro

Si al agregar un test_type necesitás modificar código del pipeline core — **la DNA spec tiene un gap**. Volver a esta spec, agregar el campo necesario, bump version, y completar a través de declaración, no de código.

---

## 7. Decisiones de diseño resueltas (2026-04-23)

1. **Referencia a venues:** archivos separados en `venues/*.yaml` para los 13 del catálogo v0. Inline permitido solo para venues custom per-cliente. Rationale: reuso entre test_types + catálogo central inspeccionable.

2. **QA checklists:** shared base en `prompts/shared/qa_reviewer_base.yaml` + overrides per-DNA en `qa_review`. Un check declarado en el base corre siempre salvo opt-out; checks custom per-DNA extienden.

3. **Edit rights de DNA:** flujo de PR vía Git. En v0 con equipo de 1 = "edit + commit + push con mensaje claro". Workflow PR formal se activa cuando crece el equipo.

4. **Versionado y reproducibilidad:** snapshot embebido en el Test record (immutable). Cuando un test se dispara, la DNA actual se serializa completa dentro del Test. Así un test de v1.0.0 se re-renderiza años después aunque la DNA haya evolucionado a v2.x.

5. **Anchors count:** `{min: 4, max: 10, recommended: 6-8}`.

### Mapping test_type → simulation_mode (validado)

Tabla de sección 3.6.1 + ejemplos queda como está. Tres casos con flag de revisión post primer cliente real:

- `narrative_framing` → mantenemos `hybrid`. Revisar si survey-only funciona después de test #5.
- `b2b_pricing` → mantenemos `hybrid` (40 delib buying team + 200 survey external).
- `churn_analysis` → mantenemos `hybrid` (60 delib intervention + 300 survey baseline).

### Setting catalog

Los 10 settings de sección 3.7.1 cubren los 15 test_types. Adicionales solo si un venue custom per-cliente lo requiere en v1+.

---

**Fin del doc v0.2.** Siguiente paso: construir venues catalog + engine del pipeline usando este contrato. Cualquier capability que el pipeline necesite y no esté expresable vía DNA → volver a esta spec, agregar el campo, bump version, y recién entonces escribir código.
