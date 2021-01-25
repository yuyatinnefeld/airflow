#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


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

dag = DAG(
    'my_simple_dag',
    catchup=False,
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    # schedule_interval=None,
)

time_stamp_cmd = """
cd /Users/yuyatinnefeld/Desktop/projects/py_airflow/data
touch sample1.txt
date >> sample1.txt
"""


t1 = BashOperator(
    task_id='create_sample1',
    bash_command=time_stamp_cmd,
    dag=dag,
)

t2 = PythonOperator(
    task_id='create_sample2',
    python_callable=write_sample2,
    dag=dag,
)

t3 = BashOperator(
    task_id='sleep_me',
    bash_command='sleep 5',
    dag=dag,
)

t4 = PythonOperator(
    task_id='create_sample3',
    python_callable=write_sample3,
    dag=dag,
)
# TODO: the dag is successfully located in the airflow but the program does not execute. 

print('run: t1 >> t2 >> t3 >> t4')
t1 >> t2 >> t3 >> t4