

from importlib.machinery import SourceFileLoader
import sys
import os


from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime, timedelta


##DirScript
DIR = os.path.dirname(os.path.realpath(__file__))



# list_of_parameters = [
# 	'sea_surface_height' 
# 	]


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 25),
    'email': ['henning_lucas@hotmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=15),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('routineMercator', default_args=default_args, schedule_interval=timedelta(minutes=25))


def downloadNCFile():
	#Import External Dicitonary
	print('Local: ' + DIR)
	scriptDir = 'python ' + DIR + '/' + 'downloadProducts.py sea_surface_height'
	os.system(scriptDir)

	return;


def printSuccess():
	#Import External Dicitonary
	print("\n\nDeuu boa!\n\n")
	return;


t1 = PythonOperator(
    task_id='downloadNC',
    python_callable=downloadNCFile,
    dag=dag)

t2 = PythonOperator(
    task_id='printFinish',
    python_callable=printSuccess,
    dag=dag)


t1.set_downstream(t2)


# for d in dags.keys():
#     globals()[d] = dags[d]










