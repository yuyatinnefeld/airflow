from airflow import DAG
from airflow.operators.python import PythonOperator

import datetime as dt

def check_oauth():
    print("check oauth")

def check_api():
    print("check api")

def get_ga_data():
    print("get ga data")

def store_data_as_csv():
    print("save_data_csv")

def csv_to_postgres():
    print("csv to pg")

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 1, 24),
    'concurrency': 1,
    'retries': 0
}

with DAG("ga_to_postgres_dag", default_args=default_args, schedule_interval="*/5 * * * *", catchup=False) as dag:

    t1 = PythonOperator(
        task_id='check_oauth',
        python_callable=check_oauth,
    )

    t2 = PythonOperator(
        task_id='check_api',
        python_callable=check_api,
    )

    t3 = PythonOperator(
        task_id='get_ga_data',
        python_callable=get_ga_data,
    )

    t4 = PythonOperator(
        task_id='store_ga_csv',
        python_callable=store_data_as_csv,
    )

    t5 = PythonOperator(
        task_id='csv_to_postgres',
        python_callable=csv_to_postgres,
    )

    t1 >> t2 >> t3 >> t4 >> t5