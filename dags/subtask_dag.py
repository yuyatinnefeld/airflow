from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup

import datetime as dt


default_args = {
    'start_date': dt.datetime(2021, 2, 24),
}

with DAG('subtask_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    task_1 = BashOperator(
        task_id='task_1',
        bash_command='sleep 1'
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        
        task_2 = BashOperator(
            task_id='task_2',
            bash_command='sleep 1'
        )

        task_3 = BashOperator(
            task_id='task_3',
            bash_command='sleep 1',
        )

    task_4 = BashOperator(
        task_id='task_4',
        bash_command='sleep 1',
    )

    task_1 >> processing_tasks >> task_4