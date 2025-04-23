from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from scrapper_mercadolibre import save
# Definindo os argumentos padrões da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),   # Data de início da DAG
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Criando a DAG
dag = DAG(
    'mercado_libre',                       
    default_args=default_args,
    description='Script que extrai dados da página do mercado livre',
    schedule_interval='@daily',
    catchup=False  
)

# Definindo uma tarefa usando o PythonOperator
task = PythonOperator(
    task_id='executa_script', 
    python_callable=save, 
    dag=dag                   
)