# DNA Catalog — Sharpz V2

Los 15 test_types del producto, cada uno como archivo YAML declarativo. Schema completo en `docs/dna-spec.md`.

## Status de los 15 test_types

| # | test_type | venue primario | sim mode | status |
|---|---|---|---|---|
| 1 | [investor_pitch](investor_pitch.yaml) | pitch_meeting | deliberation | **active** |
| 2 | [pricing_test](pricing_test.yaml) | retail_decision | survey_batch | **active** |
| 3 | [crisis_response](crisis_response.yaml) | split_public_private | deliberation | **active** |
| 4 | [creative_test](creative_test.yaml) | social_viral | survey_batch | **active** |
| 5 | [narrative_framing](narrative_framing.yaml) | social_viral + press_cycle | hybrid | **active** |
| 6 | [brand_sentiment_shift](brand_sentiment_shift.yaml) | social_viral + press_cycle | deliberation | **active** |
| 7 | [competitive_response](competitive_response.yaml) | press_cycle + social_viral | deliberation | **active** |
| 8 | [controversial_launch](controversial_launch.yaml) | polarized_social | deliberation | **active** |
| 9 | [product_launch](product_launch.yaml) | product_usage_simulation | usage_simulation | **active** |
| 10 | [campaign_planning](campaign_planning.yaml) | campaign_exposure_mix | deliberation | **active** |
| 11 | [churn_analysis](churn_analysis.yaml) | support_ticket | hybrid | **active** |
| 12 | [electoral_sentiment](electoral_sentiment.yaml) | electoral_ecosystem | deliberation/forecast | **active** |
| 13 | [policy_rollout](policy_rollout.yaml) | town_hall | hybrid | **active** |
| 14 | [audience_targeting](audience_targeting.yaml) | cross_audience_comparison | survey_batch | **active** |
| 15 | [b2b_pricing](b2b_pricing.yaml) | b2b_sales_cycle | hybrid | **active** |

**15/15 DNAs completos.** Los test_types son declarativamente funcionales. Ejecución completa de cada uno requiere los action prompts específicos del venue (en `prompts/<test_type>/`) que se completan progresivamente.

## Los 3 DNAs activos (v0) — por qué estos

- **investor_pitch** → el caso Invernea es el benchmark m1. Valida el contrato completo (deliberation + in_person + privado).
- **pricing_test** → el modo más diferente (survey_batch con 800 agents). Si el engine soporta ambos sin código especial, el DNA-first funciona.
- **crisis_response** → el más complejo (hybrid multi-canal con 5 canales paralelos, NO-GO legítimo). Stress test del framework.

Los 3 cubren los 3 simulation modes principales (deliberation, survey_batch, deliberation multi-canal hybrid) y sus venues respectivos. Si funcionan, los 12 restantes son configuración, no código nuevo.

## Cómo leer un DNA

Cada archivo tiene:

1. **client_facing** — decisión que ayuda, buyer profile, triggers
2. **panel** — anchors spec, ecosystem spec, amplification rules, composition targets
3. **simulation** — mode + panel_size + rounds + propagation
4. **setting** — contexto físico/virtual (hereda defaults de tono)
5. **venue** — ref a `venues/<id>.yaml`
6. **stimulus** — formatos aceptados + required_fields + delivery
7. **metrics** — primary / secondary / never_emphasize
8. **report** — required_sections + unique_sections + length + quote_requirements
9. **one_pager** — siempre SHARED_V1
10. **qa_review** — checklists por stage con anti-bias invariants
11. **tier_overrides** — qué cambia per tier (modelos + multi_run + panel_size)
12. **limits** — caveats estáticos que entran al report
13. **cross_test_learning** — patterns extraídos + scoping
14. **pricing_recommendation** — default tier + upgrade triggers
15. **prompts** — refs a archivos YAML de prompts

## Agregar un test_type

Ver `docs/dna-spec.md` sección 6 "Extension guide". Pasos core:

1. Escribir DNA YAML en `dna/<id>.yaml`
2. Crear `prompts/<id>/` con los YAML requeridos
3. Verificar venue existente o crear custom en `venues/`
4. CI validation con pydantic schema
5. Test end-to-end con caso sintético

## Versionado

Cada DNA tiene `version` semver. Snapshot embebido en cada Test record al dispararlo → reproducibilidad perfecta años después.
