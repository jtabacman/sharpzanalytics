# Landing — `sharpzanalytics.com`

Marketing público + operator login entry.

- Stack: HTML + CSS vanilla + Three.js (hero graph 3D)
- Deploy: **Netlify** (recomendado — soporta `_redirects` para rutear a backend)
- Status: **pendiente import** desde deploy actual de Netlify

Design reference: `docs/landing-design.md`.

## Import plan

1. Clonar / descargar el repo/folder de deploy Netlify actual (está en `/Users/juliantabacman/sharpz-analytics-web/` en la Mac)
2. Copiar `index.html`, `login/index.html`, assets en subcarpetas `css/`, `js/`, `fonts/`
3. Extraer el script de Three.js completo (no el simplificado del doc) para el hero graph
4. Agregar `_redirects` con las rules de routing:

```
/intake/*     https://backend.sharpzanalytics.com/intake/:splat     200
/report/*     https://backend.sharpzanalytics.com/report/:splat     200
/api/*        https://backend.sharpzanalytics.com/api/:splat        200
```

5. Deploy a Netlify apuntando el `@` CNAME de `sharpzanalytics.com` acá
