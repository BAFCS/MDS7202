import pandas as pd
import optuna
import mlflow
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
import pickle
import os
import kaleido #Necesario para guardar los gráficos de Optuna en formato PNG
import plotly
import subprocess #esto sera para crear el requirements.txt

def optimize_model(X_train, X_test, y_train, y_test):
    experiment_name = "xgboost_optuna_water"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 200),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        }
        run_name = f"XGBoost_water_lr_{params['learning_rate']:.3f}_depth_{params['max_depth']}"

        with mlflow.start_run(run_name=run_name):
            model = XGBClassifier(**params, random_state=42)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            f1 = f1_score(y_test, preds)
            mlflow.log_metric("valid_f1", f1)

            mlflow.sklearn.log_model(model, "model")

            return f1
    print("Optimizing hyperparameters with Optuna...")
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=15)

    #Creación de grafico
    plots_dir = "plots"
    os.makedirs(plots_dir, exist_ok=True)

    #Gráfico de importancia
    fig_importance = optuna.visualization.plot_param_importances(study)
    fig_importance.write_image(os.path.join(plots_dir, "importancia_hiperparametros.png"))

    # Gráfico de historial de optimización
    fig_history = optuna.visualization.plot_optimization_history(study)
    fig_history.write_image(os.path.join(plots_dir, "historial_optimizacion.png"))

    # Gráfico de distribución de hiperparámetros
    fig_parallel = optuna.visualization.plot_parallel_coordinate(study)
    fig_parallel.write_image(os.path.join(plots_dir, "distribucion_hiperparametros.png"))

    return experiment # Retornamos el objeto experiment para poder sacar su id más adelante


def get_best_model(experiment_id):
    runs = mlflow.search_runs(experiment_ids=[experiment_id]) #Se pasa la ID dentro de una lista a experiments_ids porque esta función espera una lista de IDs de experimentos, incluso si solo se está buscando en uno. Esto es necesario para que la función pueda manejar múltiples experimentos a la vez, aunque en este caso solo estemos interesados en uno.
    best_run = runs.sort_values("metrics.valid_f1", ascending=False).iloc[0] #Ordenamos las corridas por la métrica valid_f1 de mayor a menor y seleccionamos la primera fila (la mejor corrida)
    best_model_id = best_run["run_id"]
    best_f1 = best_run["metrics.valid_f1"]

    print(f"Best F1-Score: {best_f1:.4f} (Run ID: {best_model_id})")

    #Cargar el modelo desde MLflow
    best_model = mlflow.sklearn.load_model(f"runs:/{best_model_id}/model") #La ruta para cargar el modelo desde MLflow se construye usando el ID de la corrida (best_model_id) y el nombre del artefacto donde se guardó el modelo ("model").

    #Guardar como .pkl el modelo
    output = "models"
    os.makedirs(output, exist_ok=True) #Creamos el directorio "models" si no existe
    pkl_path = os.path.join(output, f"xgb_{pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')}.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"Modelo guardado en {pkl_path}")

    return best_model


if __name__ == "__main__":
    # Aqui se cargan los datos y se llama a las funciones
    db = pd.read_csv("water_potability.csv")
    X = db.drop("Potability", axis=1)
    y = db["Potability"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



    experiment = optimize_model(X_train, X_test, y_train, y_test)

    # Se busca y guarda el mejor modelo usando el ID del experimento devuelto
    mejor_modelo = get_best_model(experiment.experiment_id)

    #Crear el requirements.txt con las dependencias necesarias para replicar en docker
    with open("requirements.txt", "w", encoding="utf-8") as f:
        subprocess.run(["pip", "freeze"], stdout=f, check=True)

