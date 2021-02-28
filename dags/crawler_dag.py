import datetime as dt
from airflow import DAG
from airflow.operators.python import PythonOperator
from requests_utils import request_url, save_text, save_json, save_csv


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 1, 24, 6, 30, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG("crawler_dag", default_args=default_args, schedule_interval="*/2 * * * *", catchup=False) as dag:

    t1 = PythonOperator(
        task_id='request_url',
        python_callable=request_url,
    )

    t2 = PythonOperator(
        task_id='save_text',
        python_callable=save_text,
    )

    t3 = PythonOperator(
        task_id='save_json',
        python_callable=save_json,
    )

    t4 = PythonOperator(
        task_id='save_csv',
        python_callable=save_csv,
    )

    t1 >> t2 >> t3 >> t4