import optuna
import mlflow
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
import pickle
import os

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
    pkl_path = os.path.join(output, "modelo_xgboost.pkl")
    with open(pkl_path, "wb") as f:
        pickle.dump(best_model, f)

    print(f"Modelo guardado en {pkl_path}")

    return best_model
