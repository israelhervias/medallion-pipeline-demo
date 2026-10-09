# Medallion Pipeline Demo

Mini pipeline local para enseñar claramente el patrón **Bronze -> Silver -> Gold** con Python, pandas y Parquet.

## Arquitectura

```text
data/raw/*.csv
     |
     v
BRONZE  copia ingerida + timestamp
     |
     v
SILVER  tipado + limpieza + deduplicación
     |
     v
GOLD    agregado de negocio sales_by_city
```

## Estructura

```text
medallion-pipeline-demo/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── src/
│   └── pipeline.py
├── requirements.txt
└── README.md
```

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
```

El resultado final queda en `data/gold/sales_by_city.csv` y `.parquet`.

## Qué demuestra

- **Bronze:** preserva una copia cercana a la fuente y añade metadatos de ingesta.
- **Silver:** aplica calidad básica: tipos, nulos, importes válidos y duplicados.
- **Gold:** crea un dataset orientado a negocio, listo para Power BI u otro consumidor.

## Siguiente evolución natural

Migrar el mismo patrón a Azure Databricks + Delta Lake y parametrizar fuentes/tablas mediante metadatos, como base para ATLAS Data Platform.
