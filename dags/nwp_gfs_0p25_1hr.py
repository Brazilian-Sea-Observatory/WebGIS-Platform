import logging
import os
import requests
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from common import download_file

from plotting import plot_gfs

VARIABLES = {
    'TMP': ['2_m_above_ground', '850_mb'],
    'RH': ['2_m_above_ground', '850_mb', '700_mb', '500_mb'],
    'PRMSL': ['mean_sea_level'],
    'UGRD': ['10_m_above_ground'],
    'VGRD': ['10_m_above_ground'],
    'HGT': ['1000_mb', '850_mb', '500_mb'],
    'ACPCP': ['surface'], # convective precipitation
    'APCP': ['surface'], # precipitation
    'SNOD': ['surface'] # snow depth
}

SCHEDULES = {
    0: '0 5 * * *',
    6: '0 12 * * *',
    12: '0 17 * * *',
    18: '0 23 * * *'
}

AOIS = {
    'AREA_1': {
        'llat': 29,
        'ulat': 33.5,
        'llon': 34,
        'ulon': 39
    },
    # 'AREA_2': {
    #     'llat': 16,
    #     'ulat': 30,
    #     'llon': 37,
    #     'ulon': 53
    # },
    'AREA_2': {
        'llat': 11,
        'ulat': 38,
        'llon': 31.5,
        'ulon': 61
    }
}

TIMESTEPS = list([i for i in range(0, 121)])
TIMESTEPS.extend([i for i in range(120, 241, 3)])
TIMESTEPS.extend([i for i in range(240, 384, 12)])

BASE_URL = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl"

def download_grib(cycle, variable, levels, aoi, llat, ulat, llon, ulon, base_dir):
    now = datetime.utcnow()
    datestr = now.strftime('%Y%m%d')
    output_path = '%s/NWP_GFS_0p25_1hr/%02d/%s/downloading/%s' % (base_dir, cycle, aoi, variable)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for i in TIMESTEPS:
        filename = "gfs.t%02dz.pgrb2.0p25.f%03d" % (cycle, i)
        level_params = "&".join(["lev_%s=on" % l for l in VARIABLES[variable]])
        url = "%s?file=%s&%s&var_%s=on&subregion=&leftlon=%f&rightlon=%f&toplat=%f&bottomlat=%f&dir=/gfs.%s%02d" % (BASE_URL, filename, level_params, variable, llon, ulon, ulat, llat, datestr, cycle)
        filepath = "%s/%s" % (output_path, filename)

        # If file exists locally, do not download it again
        if not os.path.isfile(filepath):
            logging.info("Downloading %s to %s" % (url, filepath))
            download_file(url, filepath)
        else:
            logging.info("Skipping %s" % filename)

def rename_folder(cycle, aoi, base_dir):
    # delete older folder and rename processing folder
    latest_path = '%s/NWP_GFS_0p25_1hr/%02d/%s/latest' % (base_dir, cycle, aoi)
    download_path = '%s/NWP_GFS_0p25_1hr/%02d/%s/downloading' % (base_dir, cycle, aoi)
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
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dags = {}
for aoi in AOIS.keys():
    llat = AOIS[aoi]['llat']
    ulat = AOIS[aoi]['ulat']
    llon = AOIS[aoi]['llon']
    ulon = AOIS[aoi]['ulon']

    for cycle in SCHEDULES.keys():
        dag_id = 'RETRIEVE_GFS_0p25_1hr_%02dZ_%s' % (cycle, aoi)
        dag_description = 'Download GFS 0p25_1hr %02dZ forecasts retrieval for %s' % (cycle, AOIS[aoi])
        schedule = SCHEDULES[cycle]

        logging.info("Creating DAG for GFS 0p25_1hr %02dZ %s scheduled at '%s'" % (cycle, AOIS[aoi], schedule))

        dag = DAG(dag_id, description=dag_description, default_args=default_args, start_date=datetime(2019,1,8,12,0), schedule_interval=schedule, catchup=False)
        dags[dag_id] = dag
        operators = []

        for v in VARIABLES.keys():
            levels = VARIABLES[v]
            #logging.info("Adding %s pressure levels %s" % (v, levels))
            operator = PythonOperator(task_id='download_gfs_0p25_1hr_%s_%s_%02dZ' % (aoi, v, cycle), python_callable=download_grib, op_args=[cycle, v, levels, aoi, llat, ulat, llon, ulon, '/data'], dag=dag)
            operators.append(operator)

        # Link operators sequentially
        #logging.info("Linking operators")
        for i in range(1, len(operators)):
            operators[i - 1].set_downstream(operators[i])

        #logging.info("Creating folder renaming task")
        renaming_task = PythonOperator(task_id='rename_folder_%s_%02d' % (aoi, cycle), python_callable=rename_folder, op_args=[cycle, aoi, '/data'], dag=dag)
        renaming_task.set_upstream(operators[len(operators) - 1])

        plotting_task = PythonOperator(task_id='plot_%s_%02d' % (aoi, cycle), python_callable=plot_gfs, op_args=[cycle, aoi, '/data', '/images'], dag=dag)
        plotting_task.set_upstream(renaming_task)

# Export DAGS so Airflow can use them
for d in dags.keys():
    globals()[d] = dags[d]