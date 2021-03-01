from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

from datetime import datetime
from requests_utils import _extracting_data


default_args = {
    'start_date': datetime(2021, 1, 24),
}

with DAG("scraping_dag", default_args=default_args, 
        schedule_interval="@daily", catchup=False) as dag:


    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS jobs(
                date TEXT NOT NULL PRIMARY KEY,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT NOT NULL,
                link TEXT NOT NULL
            );
            '''
    )

    extracting_data = PythonOperator(
        task_id='extracting_data',
        python_callable=_extracting_data,
    )

    storing_price = BashOperator(
        task_id='storing_data',
        bash_command='echo -e ".separator ","\n.import /Users/yuyatinnefeld/Desktop/projects/airflow/data/processed_jobs.csv jobs" | sqlite3 /Users/yuyatinnefeld/Desktop/projects/airflow/airflow.db',
        do_xcom_push=False
    )