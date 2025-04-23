from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Definindo os argumentos padrões da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),   # Data de início da DAG
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Criando a DAG
dag = DAG(
    'minha_dag',                        # Nome da DAG
    default_args=default_args,
    description='Uma DAG de exemplo que imprime a data atual',
    schedule_interval=timedelta(days=1)  # Define a periodicidade: uma vez por dia
)

# Definindo uma tarefa usando o BashOperator
tarefa_imprimir_data = BashOperator(
    task_id='imprimir_data',  # Identificador único da tarefa
    bash_command='date',      # Comando que será executado no terminal
    dag=dag                   # Associa a tarefa à DAG criada
)