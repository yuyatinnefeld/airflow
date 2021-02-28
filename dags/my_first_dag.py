from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import datetime as dt

def write_sample2():
    with open('data/sample2.txt', 'a') as f:
        f.write('Hello\n')

def write_sample3():
    with open('data/sample3.txt', 'a') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        f.write(str(t) + '\n')

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 1, 24, 7, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG("my_first_dag", default_args=default_args, schedule_interval="*/5 * * * *", catchup=False) as dag:

    t1 = BashOperator(
        task_id='create_sample_file1',
        bash_command="""
            cd /Users/yuyatinnefeld/Desktop/projects/airflow/data
            touch sample1.txt
            date >> sample1.txt""",
    )

    t2 = PythonOperator(
        task_id='create_sample_file2',
        python_callable=write_sample2,
    )

    t3 = BashOperator(
        task_id='sleep_5',
        bash_command='sleep 5',
    )

    t4 = PythonOperator(
        task_id='create_sample_file3',
        python_callable=write_sample3,
    )

    t1 >> t2 >> t3 >> t4