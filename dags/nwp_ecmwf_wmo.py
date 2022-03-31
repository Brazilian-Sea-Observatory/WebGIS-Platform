import ftplib
import logging
import os
import requests
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from common import download_file
from plot_ecmwf import *

VARIABLES = {
    'msl': 'HPX',
    'gh_500': 'HHX',
    't_850': 'HTX',
    'u_850': 'HUX',
    'v_850': 'HVX'
}

SCHEDULES = {
    0: '0 7 * * *',
    12: '0 19 * * *'
}

TIMESTEPS = list([i for i in range(0, 241, 24)])

LETTERS = {
    0:  'A',
    24: 'E',
    48: 'I',
    72: 'K',
    96: 'M',
    120: 'O',
    144: 'Q',
    168: 'S',
    192: 'W',
    216: 'Y',
    240: 'T'
}

BASE_DIR = '/data/NWP_ECMWF_WMO'

def download_grib(cycle, variable, base_dir):
    now = datetime.utcnow()
    mday = now.day
    datestr = now.strftime('%Y%m%d')

    output_path = '%s/%02d/downloading/%s' % (base_dir, cycle, variable)
    remote_dir = '%s%02d0000' % (datestr, cycle)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    logging.info("Connecting to ECMWF FTP server")
    ftp = ftplib.FTP("dissemination.ecmwf.int")
    ftp.login("wmo", "essential")
    logging.info("Connected")
    ftp.set_pasv(True)
    ftp.cwd(remote_dir)

    for i in TIMESTEPS:
        letter = LETTERS[i]
        prefix = VARIABLES[variable]
        if variable == "gh_500":
            level = "50"
        elif variable in ["t_850", "u_850", "v_850"]:
            level = "85"
        else:
            level = "89"

        if i == 0:
            if variable == "msl":
                remote_filename = "A_%s%s%sECMF%02d%02d00_C_ECMF_%s%02d0000_an_%s_global_0p5deg_grib2.bin" % (prefix, letter, level, mday, cycle, datestr, cycle, variable)
            else: 
                remote_filename = "A_%s%s%sECMF%02d%02d00_C_ECMF_%s%02d0000_an_%shPa_global_0p5deg_grib2.bin" % (prefix, letter, level, mday, cycle, datestr, cycle, variable)
        else:
            if variable == "msl":
                remote_filename = "A_%s%s%sECMF%02d%02d00_C_ECMF_%s%02d0000_%dh_%s_global_0p5deg_grib2.bin" % (prefix, letter, level, mday, cycle, datestr, cycle, i, variable)
            else:
                remote_filename = "A_%s%s%sECMF%02d%02d00_C_ECMF_%s%02d0000_%dh_%shPa_global_0p5deg_grib2.bin" % (prefix, letter, level, mday, cycle, datestr, cycle, i, variable)
        
        local_filename = "%s_%03dZ_global_0p5deg_grib2.bin" % (variable, i)

        filepath = "%s/%s" % (output_path, local_filename)

        # If file exists locally, do not download it again
        if not os.path.isfile(filepath):
            logging.info("Downloading %s to %s" % (remote_filename, filepath))
            ftp.retrbinary("RETR %s" % remote_filename, open(filepath, "wb").write)
        else:
            logging.info("Skipping %s" % remote_filename)

    logging.info("Disconnecting")
    ftp.close()

def rename_folder(cycle, base_dir):
    # delete older folder and rename processing folder
    latest_path = '%s/%02d/latest' % (base_dir, cycle)
    download_path = '%s/%02d/downloading' % (base_dir, cycle)
    if os.path.exists(latest_path):
        logging.info("Deleting old data")
        shutil.rmtree(latest_path)
    logging.info("Renaming 'downloading' folder to 'latest'")
    os.rename(download_path, latest_path)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
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

def plot_ecmwf(cycle, data_dir, images_dir):
    for t in TIMESTEPS:
            plot_ecmwf_mslp_gh500mb(cycle, t, data_dir, images_dir)
            # plot_gefs_1000_500mb_thickness(area, cycle, t, data_dir, images_dir)
            plot_ecmwf_t850mb(cycle, t, data_dir, images_dir)
            plot_ecmwf_wind850mb(cycle, t, data_dir, images_dir)

dags = {}

for cycle in SCHEDULES.keys():
    dag_id = 'RETRIEVE_ECMWF_WMO_%02dZ' % cycle
    dag_description = 'Download ECMWF_WMO %02dZ forecasts' % cycle
    schedule = SCHEDULES[cycle]

    logging.info("Creating DAG for ECMWF WMO %02dZ scheduled at '%s'" % (cycle, schedule))

    dag = DAG(dag_id, description=dag_description, default_args=default_args, start_date=datetime(2019,1,8,12,0), schedule_interval=schedule, catchup=False)
    dags[dag_id] = dag
    operators = []

    for v in VARIABLES:
        operator = PythonOperator(task_id='download_ecmwf_wmo_%s_%02dZ' % (v, cycle), python_callable=download_grib, op_args=[cycle, v, BASE_DIR], dag=dag)
        operators.append(operator)

    # Link operators sequentially
    #logging.info("Linking operators")
    for i in range(1, len(operators)):
        operators[i - 1].set_downstream(operators[i])

    #logging.info("Creating folder renaming task")
    renaming_task = PythonOperator(task_id='rename_folder_%02d' % cycle, python_callable=rename_folder, op_args=[cycle, BASE_DIR], dag=dag)
    renaming_task.set_upstream(operators[len(operators) - 1])

    plotting_task = PythonOperator(task_id='plot_ecmwf_%02d' % cycle, python_callable=plot_ecmwf, op_args=[cycle, '/data', '/images'], dag=dag)
    plotting_task.set_upstream(renaming_task)

# Export DAGS so Airflow can use them
for d in dags.keys():
    globals()[d] = dags[d]