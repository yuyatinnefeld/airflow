from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

import datetime as dt

def source1_to_s3():
    # code that writes our data from source 1 to s3
    print('source1 > s3')

def source3_to_s3():
    # code that writes our data from source 3 to s3
    print('source3 > s3')

def source2_to_hdfs(config, ds, **kwargs):
    # code that writes our data from source 2 to hdfs
    # ds: the date of run of the given task.
    # kwargs: keyword arguments containing context parameters for the run.
    print('source2 > hdfs')

def get_hdfs_config():
    #return HDFS configuration parameters required to store data into HDFS.
    return None

default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2021, 1, 24, 6, 30, 00),
    'concurrency': 1,
    'retries': 0
}


with DAG("data_to_s3_dag", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:

  config = get_hdfs_config()

  src1_s3 = PythonOperator(
    task_id='source1_to_s3', 
    python_callable=source1_to_s3, 
  )

  src2_hdfs = PythonOperator(
    task_id='source2_to_hdfs', 
    python_callable=source2_to_hdfs, 
    op_kwargs = {'config' : config},
    provide_context=True,
  )

  src3_s3 = PythonOperator(
    task_id='source3_to_s3', 
    python_callable=source3_to_s3, 
  )

  spark_job = BashOperator(
    task_id='spark_task_etl',
    bash_command='echo "spark-submit --master spark://localhost:7077 spark_job.py"',
  )

  src1_s3 >> spark_job
  src2_hdfs >> spark_job
  src3_s3 >> spark_job

