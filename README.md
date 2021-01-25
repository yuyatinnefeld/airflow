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
python -m venv env
source env/bin/activate (Mac) or env\Scripts\activate (Windows)
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

if the db need reset:
```bash
airflow db reset
```

### 6. these files were created
/airflow.cfg
/unitests.cfg
/airflow.db #SQLite

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
airflow webserver --port 8080
```

### 9. open 
http://0.0.0.0:8080


### 10. start the schedueler 
open a new terminal or else run webserver with ``-D`` option to run it as a daemon
```bash
airflow scheduler
```