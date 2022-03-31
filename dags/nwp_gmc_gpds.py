import logging
import os
import requests
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from common import download_file, delete_old_folders
from plot_gmc import plot_gmc_1000_500mb_thickness
from plot_gmc import plot_gmc_mslp_gh500mb
from plot_gmc import plot_gmc_t2m
from plot_gmc import plot_gmc_rh2m
from plot_gmc import plot_gmc_precipitation
# from plot_gmc import plot_gmc_wind10m

VARIABLES = [
    'TMP_TGL_2', # temperature at 2 m above ground
    'DPT_TGL_2', # dew point temperature at surface
    'RH_TGL_2', # average surface relative humidity
    'PRMSL_MSL_0', # mean sea level pressure
    'APCP_SFC_0', # accumulated precipitation
    'SNOD_SFC_0', # snow depth
    'SPFH_ISBL_850', # specific humidity 850 mb
    'SPFH_ISBL_700', # specific humidity 700 mb
    'SPFH_ISBL_500', # specific humidity 500 mb
    'HGT_ISBL_500', # geopotential height 500 mb
    'HGT_ISBY_1000-500', #1000-500mb thickness
    'UGRD_TGL_10', # zonal wind component at 10 m
    'VGRD_TGL_10' # meridional wind component at 10 m
]

SCHEDULES = {
    0: '20 5 * * *',
    12: '20 17 * * *',
}

TIMESTEPS = list([i for i in range(0, 241, 3)])

BASE_URL = "http://dd.weather.gc.ca/model_gem_global/25km/grib2/lat_lon/"


def model_dir(base_dir, year, month, day, cycle):
    return '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/' % (base_dir, cycle, year, month, day)

def download_grib(data_dir, year, month, day, cycle, variable):
    model_data_dir = model_dir(data_dir, year, month, day, cycle)
    output_path = '%s/%s' % (model_data_dir, variable)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    datestr = '%04d%02d%02d' % (year, month, day)

    for i in TIMESTEPS:
        if i == 0 and variable == 'APCP_SFC_0':
            continue
        remote_filename = "CMC_glb_%s_latlon.24x.24_%s%02d_P%03d.grib2" % (variable, datestr, cycle, i)
        local_filename = "CMC_glb_%s_latlon.24x.24_%02d_P%03d.grib2" % (variable, cycle, i)
        url = "%s/%02d/%03d/%s" % (BASE_URL, cycle, i, remote_filename)
        filepath = "%s/%s" % (output_path, local_filename)

        # If file exists locally, do not download it again
        if not os.path.isfile(filepath):
            logging.info("Downloading %s to %s" % (url, filepath))
            download_file(url, filepath)
        else:
            logging.info("Skipping %s" % remote_filename)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['fabiosato@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 60,
    'retry_delay': timedelta(minutes=1),
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
    dag_id = 'RETRIEVE_GMC_GPDS_%02dZ' % cycle
    dag_description = 'Download CMC/GMC GPDS %02dZ forecasts' % cycle
    schedule = SCHEDULES[cycle]

    logging.info("Creating DAG for CMC/GMC GPDS %02dZ scheduled at '%s'" % (cycle, schedule))

    dag = DAG(dag_id, description=dag_description, default_args=default_args, start_date=datetime(2019,1,10,0,0), schedule_interval=schedule, catchup=False)
    dags[dag_id] = dag
    operators = {}

    for v in VARIABLES:
        #logging.info("Adding %s" % v)
        operator = PythonOperator(
            task_id='download_gmc_gpds_%s_%02dZ' % (v, cycle), 
            python_callable=download_grib, 
            op_args=['/data', year, month, day, cycle, v], dag=dag)
        operators[v] = operator

    # Link operators sequentially
    logging.info("Linking operators")
    keys = list(operators.keys())
    for i in range(1, len(keys)):
        operators[keys[i-1]] >> operators[keys[i]]

    plot_1000_500mb_thickness_task = PythonOperator(
        task_id='plot_gmc_1000_500mb_thickness_%02dZ' % (cycle), 
        python_callable=plot_gmc_1000_500mb_thickness, 
        op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], 
        dag=dag)

    operators['PRMSL_MSL_0'] >> plot_1000_500mb_thickness_task
    operators['HGT_ISBY_1000-500'] >> plot_1000_500mb_thickness_task

    plot_mslp_gh500mb_task = PythonOperator(
        task_id='plot_gmc_mslp_gh500mb_%02dZ' % (cycle),
        python_callable=plot_gmc_mslp_gh500mb,
        op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS],
        dag=dag
    )

    operators['PRMSL_MSL_0'] >> plot_mslp_gh500mb_task
    operators['HGT_ISBL_500'] >> plot_mslp_gh500mb_task

    plot_t2m_task = PythonOperator(
        task_id='plot_gmc_t2m_%02dZ' % (cycle),
        python_callable=plot_gmc_t2m,
        op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS],
        dag=dag
    )

    operators['TMP_TGL_2'] >> plot_t2m_task


    plot_rh2m_task = PythonOperator(
        task_id='plot_gmc_rh2m_%02dZ' % (cycle),
        python_callable=plot_gmc_rh2m,
        op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS],
        dag=dag
    )
    operators['RH_TGL_2'] >> plot_rh2m_task

    plot_precipitation_task = PythonOperator(
        task_id='plot_gmc_precipitation_%02dZ' % (cycle),
        python_callable=plot_gmc_precipitation,
        op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS],
        dag=dag
    )
    operators['APCP_SFC_0'] >> plot_precipitation_task

    # plot_wind10m_task = PythonOperator(
    #     task_id='plot_gmc_wind10m_%02dZ' % (cycle),
    #     python_callable=plot_gmc_wind10m,
    #     op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS],
    #     dag=dag
    # )
    # operators['UGRD_TGL_10'] >> plot_wind10m_task
    # operators['VGRD_TGL_10'] >> plot_wind10m_task

    evict_task = PythonOperator(task_id='evict_gmc_%02d' % cycle, python_callable=delete_old_folders, op_args=['/data/NWP_GMC_GPDS/%02d' % cycle, 1], dag=dag)
    operators[keys[len(keys)-1]] >> evict_task

# Export DAGS so Airflow can use them
for d in dags.keys():
    globals()[d] = dags[d]