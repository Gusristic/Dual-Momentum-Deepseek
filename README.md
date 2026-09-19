# Dual Momentum â€” App con datos reales

Web app estÃ¡tica que muestra seÃ±ales y backtest de Dual Momentum
(Modelo H: equilibrado 12M / 6M / 3M) usando datos reales de Yahoo Finance.

## CÃ³mo funciona

1. GitHub Actions descarga precios de Yahoo Finance cada dÃ­a a las 06:00 UTC.
2. Guarda los datos en `data/prices.json` dentro del repositorio.
3. GitHub Pages sirve `index.html`.
4. La web lee `data/prices.json` y calcula las seÃ±ales en el navegador.

## Estructura

- `index.html` â€” la web completa (una sola pÃ¡gina, sin dependencias).
- `scripts/fetch_data.py` â€” descarga precios.
- `scripts/requirements.txt` â€” dependencias Python.
- `.github/workflows/update-data.yml` â€” cron diario de GitHub Actions.
- `data/prices.json` â€” datos generados automÃ¡ticamente.

## Despliegue

1. Crear repositorio en GitHub (pÃºblico).
2. Subir todos los archivos.
3. Settings â†’ Pages â†’ Source: Deploy from branch â†’ main â†’ / (root).
4. Settings â†’ Actions â†’ General â†’ Workflow permissions â†’ Read and write.
5. Actions â†’ "Update market data" â†’ Run workflow (primera vez manual).
6. Abrir `https://tu-usuario.github.io/dual-momentum/`.

## Aviso legal

Uso educativo. No es asesoramiento financiero ni fiscal.
