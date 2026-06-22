#!/bin/bash

# Configurar la carpeta actual como base de Airflow
export AIRFLOW_HOME=$(pwd)

echo "Inicializando la base de datos..."
airflow db migrate

# Ver la contraseña. Si no se en un comienzo, ejecutar airflow standalone, parar el proceso y luego ejecutar nuevamente este comando.
cat $AIRFLOW_HOME/simple_auth_manager_passwords.json.generated

# # levanta scheduler + webserver en http://localhost:8080
echo "Levantando Airflow Standalone en http://localhost:8080..."
airflow standalone
