from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import datetime as dt
import json
from pandas import json_normalize

default_args = {
    'start_date': dt.datetime(2021,2,28),
}

def _processing_price(ti):
    prices = ti.xcom_pull(task_ids=['extracting_price'])
    
    if not len(prices):
        raise ValueError('Price is empty')

    today = dt.datetime.today()
    doller = prices[0]['USD'].get('last')
    euro = prices[0]['EUR'].get('last')
    yen = prices[0]['JPY'].get('last')

    processed_price = json_normalize({
        'date': today,
        'euro': euro,
        'doller': doller,
        'yen': yen,
    })

    processed_price.to_csv('data/processed_price.csv', index=None, header=False)

with DAG('bitcoin_price_dag', schedule_interval='@daily', 
        default_args=default_args, 
        catchup=False) as dag:

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS bitcoin(
                date TEXT NOT NULL PRIMARY KEY,
                euro INTEGER NOT NULL,
                doller INTEGER NOT NULL,
                yen INTEGER NOT NULL
            );
            '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='bitcoin_api',
        endpoint='ticker'
    )

    extracting_price = SimpleHttpOperator(
        task_id='extracting_price',
        http_conn_id='bitcoin_api',
        endpoint='ticker',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    processing_price = PythonOperator(
        task_id='processing_price',
        python_callable=_processing_price

    )

    storing_price = BashOperator(
        task_id='storing_price',
        bash_command='echo -e ".separator ","\n.import /Users/yuyatinnefeld/Desktop/projects/airflow/data/processed_price.csv bitcoin" | sqlite3 /Users/yuyatinnefeld/Desktop/projects/airflow/airflow.db'
    )

    creating_table >> is_api_available >> extracting_price >> processing_price >> storing_price