import logging
import os
import requests
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from common import download_file, delete_old_folders
from plot_ukmet import plot_ukmet

SCHEDULES = {
    0: '30 6 * * *',
    12: '30 18 * * *'
}

BASE_URL = "http://www.ftp.ncep.noaa.gov/data/nccf/com/ukmet/prod/"

def download_grib(data_dir, year, month, day, cycle):
    datestr = '%04d%02d%02d' % (year, month, day)

    remote_folder = "ukmet.%s" % (datestr)
    output_path = '%s/NWP_UKMET/%02d/%s/' % (data_dir, cycle, datestr)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = "nrukmet.t%02dz.ukm25.grib2" % (cycle)
    
    url = "%s/%s/%s" % (BASE_URL, remote_folder, filename)
    filepath = "%s/%s" % (output_path, filename)

    # If file exists locally, do not download it again
    if not os.path.isfile(filepath):
        logging.info("Downloading %s to %s" % (url, filepath))
        download_file(url, filepath)
    else:
        logging.info("Skipping %s" % filename)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 14),
    'email': ['fabiosato@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=15),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dags = {}

forecast_date = datetime.utcnow().date()
year = forecast_date.year
month = forecast_date.month
day = forecast_date.day

for cycle in SCHEDULES.keys():
    dag_id = 'RETRIEVE_UKMET_%02dZ' % (cycle)
    dag_description = 'Download UKMET %02dZ forecasts' % (cycle)
    schedule = SCHEDULES[cycle]

    logging.info("Creating DAG for UKMET %02dZ scheduled at '%s'" % (cycle, schedule))

    dag = DAG(
        dag_id, 
        description=dag_description, 
        default_args=default_args, 
        start_date=datetime(2019,1,14,0,0), 
        schedule_interval=schedule, 
        catchup=False)

    dags[dag_id] = dag

    operator = PythonOperator(
        task_id='download_ukmet_%02dZ' % (cycle), 
        python_callable=download_grib, 
        op_args=['/data', year, month, day, cycle], dag=dag)

    plotting_task = PythonOperator(
        task_id='plot_ukmet_%02dZ' % (cycle),
        python_callable=plot_ukmet,
        op_args=['/data', '/images', year, month, day, cycle],
        dag=dag)

    operator >> plotting_task

    evict_task = PythonOperator(
        task_id='evict_ukmet_%02dZ' % (cycle),
        python_callable=delete_old_folders,
        op_args=['/data/NWP_UKMET/%02d' % cycle, 1],
        dag=dag)
    
    operator >> evict_task

# Export DAGS so Airflow can use them
for d in dags.keys():
    globals()[d] = dags[d]