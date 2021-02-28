<h1 align="center">Airflow ETL Pipeline</h1> <br>
<h2 align="center">🚀 🐍 🚀 🐍 🚀 🐍 🚀 🐍 🚀 🐍 🚀 🐍 </h2> <br>

## Table of Contents

- [About](#about)
- [Benefit](#benefit)
- [Info](#info)
- [Setup](#setup)

## About
Airflow is a platform to programmatically author, schedule and monitor workflows.

Use Airflow to author workflows as Directed Acyclic Graphs (DAGs) of tasks. The Airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. (Airflow)


## Benefit
* Dynamic: Airflow pipelines are configuration as code (Python), allowing for dynamic pipeline generation. This allows for writing code that instantiates pipelines dynamically.
* Extensible: Easily define your own operators, executors and extend the library so that it fits the level of abstraction that suits your environment.
* Elegant: Airflow pipelines are lean and explicit. Parameterizing your scripts is built into the core of Airflow using the powerful Jinja templating engine.
* Scalable: Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. Airflow is ready to scale to infinity.


## Info
http://airflow.apache.org/docs/apache-airflow/stable/start.html


## Setup
### 0. activate venv
```bash
python -m venv ./venv
source ./venv/bin/activate (Mac) or env\Scripts\activate (Windows)
```

### 1. install the package

```bash
pip install apache-airflow
```

### 3. set the path for airflow_home

```bash
export AIRFLOW_HOME=$(pwd)
```
(for example: AIRFLOW=/Users/yuyatinnefeld/Desktop/projects/py_airflow)

### 4. create a folder /dags
```bash
mkdir dags
```

### 5. create init db
```bash
airflow db init
```

if the db need upgrade:
```bash
airflow db upgrade
```

### 6. these files were created
```bash
/airflow.cfg
/unitests.cfg
/airflow.db
```

### 7. create super user

```bash
airflow users create \
    --username admin \
    --firstname yuya \
    --lastname tinnefeld \
    --role Admin \
    --email yuya@admin.com
```

### 8. run the webserver
start the web server, default port is 8080

```bash
airflow webserver
```

### 9. open 
http://localhost:8080


### 10. start the schedueler 
open a new terminal or else run webserver with ``-D`` option to run it as a daemon
```bash
airflow scheduler
```

## Project GET Bitcoin Price ##

1. Create the dag
dags/bitcoin_price_dag.py

2. Create SQLConnector (Task1 Table Create)
```python
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

...

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS bitcoin(
                date TEXT NOT NULL PRIMARY KEY,
                price INTEGER NOT NULL,
                time TEXT NOT NULL
            );
            '''
    )
```
3. Create Connector by Airflow  (Task1 Table Create)
Admin > Connections > create new >
Conn Id => db_sqlite
Conn Type => Sqlite
Host => airflow.db director (ex. /Users/.../airflow/airflow.db)

4. test the connection & task(Task1 Table Create)
```bash
airflow tasks test [YOUR DAG NAME] [TASK NAME] [YYYY-MM]
```

Ex.
```bash
airflow tasks test bitcoin_price_dag creating_table 2021-02
```

5. Create API sensor (Task2 API available check)

```python
from airflow.providers.http.sensors.http import HttpSensor

...

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='bitcoin_api',
        endpoint='ticker'
    )

```

6. Create REST API connector (Task2 API available check)
Admin > Connections > create new >
Conn Id => bitcoin_api
Conn Type => HTTP
Host => http://blockchain.info/

bitcoin price
URL = https://blockchain.info/ticker

7. Testing the connection & task (Task2 API available check)
```bash
airflow tasks test bitcoin_price_dag is_api_available 2021-02
```

8. create extracting task (Task3 get API data)
```python
from airflow.providers.http.operators.http import SimpleHttpOperator
import json

...

    extracting_price = SimpleHttpOperator(
        task_id='extracting_price',
        http_conn_id='bitcoin_api',
        endpoint='ticker',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

```

9. Testing the extracting task (Task3 get API data)
```bash
airflow tasks test bitcoin_price_dag extracting_price 2021-02
```

10. Processing the Json Result and export as CSV (Task4 Processing)

```python
from airflow.operators.python import PythonOperator
from pandas import json_normalize

processing_bitcoin_price = PythonOperator(
        task_id='processing_price',
        python_callable=_processing_price

    )

```

11. Define the function (Task4 Processing) & Test
Here is xcom used to get/share the extracting data which is created from Task3 (extracting_price)

```python

def _processing_price(ti):
    prices = ti.xcom_pull(task_ids=['extracting_price'])
    if not len(prices):
        raise ValueError('Price is empty')
    
    today = dt.datetime.today()
    doller = prices['USD'].get('last')
    euro = price['EUR'].get('last')
    yen = price['JPY'].get('last')
    
    processed_price = json_normalize({
        'date': today,
        'euro': euro,
        'doller': doller,
        'yen': yen,
    })
```

12. Store the csv data to SQLite DB & Test

```python
storing_price = BashOperator(
    task_id='storing_price',
    bash_command='echo -e ".separator ","\n.import /Users/yuyatinnefeld/Desktop/projects/airflow/data/processed_price.csv bitcoin" | sqlite3 /Users/yuyatinnefeld/Desktop/projects/airflow/airflow.db'
)

```

13. Create the dependencies 

```python
creating_table >> is_api_available >> extracting_price >> processing_price >> storing_price
```