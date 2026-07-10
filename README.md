# MDS7202 - Laboratorio de Programación Científica para Ciencia de Datos

Repositorio del curso MDS7202 (Otoño 2026), Facultad de Ciencias Físicas y Matemáticas, Universidad de Chile.

Este repositorio contiene los laboratorios y entregas del curso, organizados por carpetas según cada laboratorio.

## Integrantes

| Nombre | GitHub |
|--------|--------|
| Gonzalo Sobarzo | [@Litr0](https://github.com/Litr0) |
| Bryan Cabezas | [@BAFCS](https://github.com/BAFCS) |

## Estructura del repositorio

.
├── Labs/
│   ├── Lab_1/
│   ├── Lab_2/
│   ├── Lab_3/
│   ├── Lab_4/
│   ├── Lab_5/
│   ├── Lab_6/
│   ├── Lab_7/
│   ├── Lab_8/
│   ├── Lab_9/
│   └── Lab_10/
├── proyecto/
│   ├── backend/
│   └── frontend/
├── pyproject.toml
├── .pre-commit-config.yaml
├── uv.lock
└── README.md

## Configuración del entorno

uv venv
source .venv/bin/activate
uv sync
pre-commit install
uv run ruff check .
