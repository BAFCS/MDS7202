import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_DIR = Path(
    "/Users/bryan/Desktop/MDS/segundo semestre/Laboratorio de ciencia de datos/Repo/MDS7202/Labs/Lab_9/data"
)  # AJUSTA esta ruta
OUTPUT_PATH = Path("/tmp/spotify_data.parquet")

PARAM_COLS = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "tempo",
    "duration_ms",
    "year",
]


# ── Funciones auxiliares (dadas) ─────────────────────────────────────────────


def load_batch(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_all_parallel(data_dir: Path, n_batches: int = 5) -> pd.DataFrame:
    paths = sorted(data_dir.glob("*.parquet"))[:n_batches]
    with ThreadPoolExecutor(max_workers=None) as executor:
        dfs = list(executor.map(load_batch, [str(p) for p in paths]))
    return pd.concat(dfs, ignore_index=True)


def build_pipeline(n_jobs: int = -1) -> Pipeline:
    return Pipeline(
        [
            (
                "column_transformer",
                ColumnTransformer(
                    [
                        ("ohe", OneHotEncoder(handle_unknown="ignore"), ["key", "mode", "genre"]),
                        ("numerical", "passthrough", PARAM_COLS),
                    ]
                ),
            ),
            ("random_forest", RandomForestRegressor(n_jobs=n_jobs, random_state=42)),
        ]
    )


# ── Funciones de las tareas de Airflow ───────────────────────────────────────


def task_load_data_fn(**context):
    """
    Carga 5 batches de datos en paralelo y guarda el resultado en disco.
    TODO: implementa esta función.
    - Usa load_all_parallel para cargar los datos.
    - Guarda el DataFrame resultante en OUTPUT_PATH (formato parquet).
    - Usa XCom para pasar la ruta del archivo a la siguiente tarea.
    """
    data_pd = load_all_parallel(DATA_DIR, 5)  # Cargar los datos en batches
    data_pd.to_parquet(OUTPUT_PATH)  # Guardar en formato parquet

    # Se envia la información

    tarea = context["task_instance"]  # Extraer la instancia de la tarea desde el contexto de Airflow

    tarea.xcom_push(key="archivo_parquet_path", value=str(OUTPUT_PATH))  # Se envia la ruta del archivo a través de XCom


def task_train_model_fn(**context):
    """
    Carga los datos desde disco y entrena el pipeline.
    TODO: implementa esta función.
    - Recupera la ruta del archivo desde XCom.
    - Lee el DataFrame desde esa ruta.
    - Prepara X e y, realiza el split 80/20.
    - Entrena build_pipeline(n_jobs=-1).
    - Imprime el tiempo de entrenamiento.
    """
    tarea = context["task_instance"]

    data_cargada_path = tarea.xcom_pull(
        key="archivo_parquet_path", task_ids="load_data"
    )  # Se busca la ruta que guardó la tarea anterior ('load_data')

    data_pd = pd.read_parquet(data_cargada_path)

    X = data_pd.drop(columns=["valence"])
    y = data_pd["valence"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    pipeline = build_pipeline(n_jobs=-1)

    t0 = time.perf_counter()
    pipeline.fit(X_train, y_train)
    time_entrenado = time.perf_counter() - t0

    # Calcula RMSE de ambos modelos
    rmse = root_mean_squared_error(y_test, pipeline.predict(X_test))

    print(f"n_jobs=-1  → tiempo: {time_entrenado:.1f}s | RMSE: {rmse:.4f}")


# ── Definición del DAG ────────────────────────────────────────────────────────

with DAG(
    dag_id="spotify_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["mds7202", "spotify"],
) as dag:
    load_data = PythonOperator(
        task_id="load_data",
        python_callable=task_load_data_fn,
    )

    train_model = PythonOperator(
        task_id="train_model",
        python_callable=task_train_model_fn,
    )

    # TODO: define la dependencia entre tareas (load_data debe ejecutarse antes que train_model)
    load_data >> train_model
