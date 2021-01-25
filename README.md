# Airflow + Python + ENV

## Source
http://airflow.apache.org/docs/apache-airflow/stable/start.html

0. venv

1. install

pip install apache-airflow

3. set the path for airflow_home

export AIRFLOW_HOME=$(pwd)

(for example: AIRFLOW=/Users/yuyatinnefeld/Desktop/projects/py_airflow)

4. create a folder /dags

mkdir dags

5. create init db
airflow db init

(if the db need reset => airflow db reset)

6. these files were created
/airflow.cfg
/unitests.cfg
/airflow.db #SQLite

7. create super user

airflow users create \
    --username admin \
    --firstname yuya \
    --lastname tinnefeld \
    --role Admin \
    --email yuya@admin.com

8. run the webserver
# start the web server, default port is 8080
airflow webserver --port 8080

9. open 
http://0.0.0.0:8080


11. start the schedueler 
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler