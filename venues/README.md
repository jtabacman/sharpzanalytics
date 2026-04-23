# Venues Catalog — Sharpz V2

Los 13 interaction surfaces donde ocurren las simulaciones. Cada venue es un archivo YAML declarativo con schema definido en `docs/dna-spec.md` sección 3.8.

## Catálogo v0 (13 venues)

| Venue | Test_types que lo usan | Setting default | Sim mode típico |
|---|---|---|---|
| [`pitch_meeting`](pitch_meeting.yaml) | investor_pitch | in_person_meeting | deliberation |
| [`retail_decision`](retail_decision.yaml) | pricing_test, product_launch (partial) | retail_context | survey_batch |
| [`social_viral`](social_viral.yaml) | campaign_planning, brand_sentiment_shift, creative_test | digital_feed | deliberation / hybrid |
| [`support_ticket`](support_ticket.yaml) | churn_analysis, crisis_response (partial) | phone_support + email_async | deliberation (per thread) |
| [`b2b_sales_cycle`](b2b_sales_cycle.yaml) | b2b_pricing | hybrid_multi_channel | hybrid |
| [`town_hall`](town_hall.yaml) | policy_rollout | in_person_panel + digital_threaded | hybrid |
| [`electoral_ecosystem`](electoral_ecosystem.yaml) | electoral_sentiment | hybrid_multi_channel | deliberation / forecast |
| [`press_cycle`](press_cycle.yaml) | crisis_response, narrative_framing | broadcast_one_to_many | deliberation |
| [`polarized_social`](polarized_social.yaml) | controversial_launch | digital_feed | deliberation |
| [`product_usage_simulation`](product_usage_simulation.yaml) | product_launch | individual_journey | usage_simulation |
| [`cross_audience_comparison`](cross_audience_comparison.yaml) | audience_targeting | individual_journey_parallel | survey_batch |
| [`split_public_private`](split_public_private.yaml) | crisis_response | hybrid_multi_channel | deliberation |
| [`campaign_exposure_mix`](campaign_exposure_mix.yaml) | campaign_planning | hybrid_multi_channel | deliberation |

## Cómo leer un venue YAML

Cada archivo tiene las siguientes secciones:

1. **Metadata:** `venue`, `version`, `status`, `description`, `used_by_test_types`
2. **Setting:** categoría física/virtual + rationale
3. **Channels:** lista de canales de mensaje con visibility / length / formality / actor_types
4. **Visibility matrix:** quién ve qué canal
5. **Turn dynamics:** mode + phases con actor / channel / timing
6. **Propagation rules:** cómo se propaga info entre agents
7. **Special behaviors:** comportamientos específicos del venue
8. **QA hints per stage:** checks que el QA review debe correr (post stage 2, 4, 6, 7)
9. **Stimulus delivery:** cómo se entrega el stimulus al panel
10. **Metrics surfaced:** qué métricas primarias/secundarias/únicas emite
11. **Limits of venue:** qué NO modela (honestidad sobre limitaciones)

## Cómo referenciar un venue desde una DNA

En `dna/<test_type>.yaml`:

```yaml
venue:
  reference: "venues/pitch_meeting.yaml"
  # overrides opcional permitidos per-DNA (ej. ajuste de rounds, channels)
```

## Cómo agregar un venue custom per-cliente

Para un cliente que necesita un surface específico no en el catálogo:

1. Crear `venues/client_<nombre>.yaml` siguiendo el schema
2. Referenciar solo desde DNAs custom del cliente
3. No agregar al catálogo standard salvo que sea generalizable

## Status

- **13/13 venues definidos** (v0)
- **Pendiente:** validación cross-venue de coherencia + primer test end-to-end para detectar gaps
- **Futuro:** revisar + iterar post primer cliente real
