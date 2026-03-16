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
├── labs/
│   ├── lab_1/
│   └── ...
├── pyproject.toml
├── .pre-commit-config.yaml
└── README.md

## Configuración del entorno

uv venv
source .venv/bin/activate
uv sync
pre-commit install
uv run ruff check .
