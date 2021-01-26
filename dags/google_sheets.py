#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from airflow import DAG
from airflow.operators.python import PythonOperator


def request_url():
    print("request URL")

def save_json():
    print("json file created")

def save_google_sheets():
    print("data in sheets")


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 1, 24, 6, 30, 00),
    'concurrency': 1,
    'retries': 0
}

dag = DAG(
    'google_sheets_dag',
    catchup=False,
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    # schedule_interval=None,
)


t1 = PythonOperator(
    task_id='request_url',
    python_callable=request_url,
    dag=dag,
)

t2 = PythonOperator(
    task_id='save_json',
    python_callable=save_json,
    dag=dag,
)

t3 = PythonOperator(
    task_id='save_google_sheets',
    python_callable=save_google_sheets,
    dag=dag,
)


print('run: t1 >> t2 >> t3')
t1 >> t2 >> t3