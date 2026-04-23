# Prompts catalog

YAMLs de prompts consumidos por el pipeline engine. Cada prompt declara inputs, model_tier, system_prompt, user_prompt_template, output_format, y qa_hints.

## Structure

```
prompts/
├── shared/                  # prompts reutilizados across test_types
│   ├── one_pager_v1.yaml    # stage 7 pass 2 — condensar a one-pager 5-section
│   └── qa_reviewer_base.yaml# QA review LLM reasoning-heavy per stage
└── <test_type>/             # prompts específicos per test_type
    ├── intake.yaml
    ├── amplifier.yaml
    ├── entity_extractor.yaml
    ├── persona.yaml
    ├── stimulus_delivery.yaml
    ├── action_*.yaml        # uno por channel del venue
    ├── interview.yaml
    ├── narrative.yaml
    ├── executive_judge.yaml
    ├── qa_reviewer.yaml     # extends shared/qa_reviewer_base
    └── pattern_extractor.yaml
```

## Estado

- `shared/` — 2/2 placeholders funcionales (one_pager_v1, qa_reviewer_base)
- `<test_type>/` — 0/15 — prompts per-test_type pendientes

## Fuente

El brief menciona 75+ YAMLs afinados en MiroFish. Import pendiente acceso a
`/Users/juliantabacman/MiroFish/` en la Mac. Mientras tanto, el loader del
backend falla gracefully si el prompt no existe y el operador tiene que
aprobar el test con prompts v1 default escritos desde cero.

## Convenciones

- Filename = `snake_case.yaml`
- Cada prompt tiene `id` + `version` (semver)
- `model_tier` ∈ {economy, pro, premium, ultra} — el router decide el model_id concreto
- `system_prompt` + `user_prompt_template` usan Jinja2 syntax para variable substitution
- `output_format` ∈ {text, markdown, structured_json, enum}
- `qa_hints` son strings que el QA reviewer usa como checklist
- `cost_budget_per_call` permite circuit breakers

## Agregar un prompt nuevo

1. Crear YAML con schema de los existentes
2. Referenciarlo desde el DNA correspondiente en `dna/<test_type>.yaml#prompts`
3. CI valida que el path existe antes de aceptar el DNA
4. Test: cargar prompt + render user_prompt_template con fixture inputs
