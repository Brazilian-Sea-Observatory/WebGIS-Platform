import bz2
import functools
import glob
import logging
import os
import requests
import shutil
import subprocess
import tempfile

from datetime import date, datetime, timedelta
from typing import List

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from common import download_file, delete_old_folders
from areas import AOIS
from plot_icon import plot_icon_t2m, plot_icon_mslp_gh500mb, plot_icon_1000_500mb_thickness, plot_icon_precipitation, plot_icon_rh2m, plot_icon_wind10m

VARIABLES = {
    't_2m': None, # Surface temperature at 2m
    't': [850, ], # Temperature at pressure levels
    'pmsl': None, # Mean sea level pressure
    'tot_prec': None, # Accumulated precipitation
    'u_10m': None, # Zonal wind at 10m
    'v_10m': None, # Meridional wind at 10m
    'vmax_10m': None, # Max wind speed at 10m
    'fi': [500, 850, 1000], # Geopotential
    'relhum_2m': None, # Relative humidity at 2m
    'relhum': [850, 700, 500], # Relative humidity at pressure levels
    'h_snow': None # Snow depth
}

SCHEDULES = {
    0: '0 4 * * *',
    6: '30 9 * * *',
    12: '0 16 * * *',
    18: '30 21 * * *'
}

TIMESTEPS = list([i for i in range(0, 79)])

def download_grib(data_dir, year, month, day, cycle, variable, level=None):
    if cycle == 0 or cycle == 12:
        TIMESTEPS.extend([i for i in range(81, 181, 3)])
    else:
        TIMESTEPS.extend([i for i in range(81, 121, 3)])
   
    datestr = '%04d%02d%02d' % (year, month, day)
    logging.info(datestr)
    
    if level is not None:
        output_path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s_%03d' % (data_dir, cycle, datestr, variable, level)
    else:
        output_path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s' % (data_dir, cycle, datestr, variable)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    remote_folder = 'weather/nwp/icon/grib/%02d/%s' % (cycle, variable)

    for i in TIMESTEPS:
        if i == 0 and variable == 'vmax_10m':
            continue
        if level == None:
            remote_filename = 'icon_global_icosahedral_single-level_%s%02d_%03d_%s.grib2.bz2' % (datestr, cycle, i, variable.upper())
            filename = 'icon_global_icosahedral_single-level_%03d_%s.grib2.bz2' % (i, variable)
        else:
            remote_filename = 'icon_global_icosahedral_pressure-level_%s%02d_%03d_%03d_%s.grib2.bz2' % (datestr, cycle, i, level, variable.upper())
            filename = 'icon_global_icosahedral_pressure-level_%03d_%s_%03d.grib2.bz2' % (i, variable, level)

        url = "http://opendata.dwd.de/%s/%s" % (remote_folder, remote_filename)
        filepath = "%s/%s" % (output_path, filename)

        # If file exists locally, do not download it again
        if not os.path.isfile(filepath):
            logging.info("Downloading %s to %s" % (url, filepath))
            download_file(url, filepath)
        else:
            logging.info("Skipping %s" % filename)

def rename_folder(cycle, base_dir):
    # delete older folder and rename processing folder
    latest_path = '%s/NWP_ICON_GLOBAL_DWD/%02d/latest' % (base_dir, cycle)
    download_path = '%s/NWP_ICON_GLOBAL_DWD/%02d/downloading' % (base_dir, cycle)
    if os.path.exists(latest_path):
        logging.info("Deleting old data")
        shutil.rmtree(latest_path)
    logging.info("Renaming 'downloading' folder to 'latest'")
    os.rename(download_path, latest_path)


def decompress_gribs(data_dir, year, month, day, cycle, variable, level=None):
    """
    Decompress bzipped grib files for a cycle/variable folder
    """
    datestr = '%04d%02d%02d' % (year, month, day)
    if level is not None:
        path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s_%03d' % (data_dir, cycle, datestr, variable, level)
    else:
        path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s' % (data_dir, cycle, datestr, variable)
    # list grib2 bzipped files
    filepaths = glob.glob('%s/*.grib2.bz2' % path)
    
    for input_path in filepaths:
        output_path = input_path[:-4]
        logging.info('Decompressing %s' % input_path)
        with open(input_path, 'rb') as source, open(output_path, 'wb') as dest:
            dest.write(bz2.decompress(source.read()))
        os.remove(input_path)

def convert_gribs(data_dir, aux_dir, year, month, day, cycle, variable, level=None):
    """
    Convert grib2 files with triangular grids to a regular grid
    """
    datestr = '%04d%02d%02d' % (year, month, day)
    if level is not None:
        path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s_%03d' % (data_dir, cycle, datestr, variable, level)
    else:
        path = '%s/NWP_ICON_GLOBAL_DWD/%02d/%s/%s' % (data_dir, cycle, datestr, variable)
    # list grib2 decompressed files
    filepaths = glob.glob('%s/*.grib2' % path)
    
    for input_path in filepaths:
        output_path = '%s.nc' % (input_path[:-6])
        logging.info('Converting grid for %s' % input_path)
        remap_arg = 'remap,%s/target_grid_world_025.txt,%s/weights_icogl2world_025.nc' % (aux_dir, aux_dir)
        subprocess.run(['cdo', '-f', 'nc', remap_arg, input_path, output_path])

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

forecast_date = datetime.utcnow().date()

year = forecast_date.year
month = forecast_date.month
day = forecast_date.day

for cycle in SCHEDULES.keys():
    dag_id = 'RETRIEVE_ICON_GLOBAL_%02dZ' % cycle
    dag_description = 'Download ICON GLOBAL %02dZ forecasts retrieval' % cycle
    schedule = SCHEDULES[cycle]

    logging.info("Creating DAG for ICON %02dZ scheduled at '%s'" % (cycle, schedule))

    dag = DAG(dag_id, description=dag_description, default_args=default_args, start_date=datetime(2019,1,8,12,0), schedule_interval=schedule, catchup=False)
    dags[dag_id] = dag

    operators = {}
    regrids = {}
    for v in VARIABLES.keys():
        levels = VARIABLES[v]
        if levels == None:
            #logging.info("Adding %s" % v)
            operator = PythonOperator(task_id='download_icon_%s_%02dZ' % (v, cycle), python_callable=download_grib, op_args=['/data', year, month, day, cycle, v, None], dag=dag)
            operators[v] = operator

            decompress = PythonOperator(task_id='decompress_icon_%s_%02dZ' % (v, cycle), python_callable=decompress_gribs, op_args=['/data', year, month, day, cycle, v, None], dag=dag)
            decompress.set_upstream(operator)

            regrid = PythonOperator(task_id='regrid_icon_%s_%02dZ' % (v, cycle), python_callable=convert_gribs, op_args=['/data', '/aux', year, month, day, cycle, v, None], dag=dag)
            regrid.set_upstream(decompress)

            regrids[v] = regrid
        else:
            for l in levels:
                #logging.info("Adding %s at pressure level %d" % (v, l))
                operator = PythonOperator(task_id='download_icon_%s_%03d_%02dZ' % (v, l, cycle), python_callable=download_grib, op_args=['/data', year, month, day, cycle, v, l], dag=dag)
                operators['%s_%03d' % (v, l)] = operator
        
                decompress = PythonOperator(task_id='decompress_icon_%s_%03d_%02dZ' % (v, l, cycle), python_callable=decompress_gribs, op_args=['/data', year, month, day, cycle, v, l], dag=dag)
                decompress.set_upstream(operator)

                regrid = PythonOperator(task_id='regrid_icon_%s_%03d_%02dZ' % (v, l, cycle), python_callable=convert_gribs, op_args=['/data', '/aux', year, month, day, cycle, v, l], dag=dag)
                regrid.set_upstream(decompress)

                regrids['%s_%03d' % (v, l)] = regrid

    # Link operators sequentially
    logging.info("Linking operators")
    keys = list(operators.keys())
    for i in range(1, len(keys)):
        operators[keys[i-1]] >> operators[keys[i]]
    # for i in range(1, len(operators)):
    #    operators[i - 1].set_downstream(operators[i])

    plot_t2m_task = PythonOperator(task_id='plot_icon_t2m_%02dZ' % (cycle), python_callable=plot_icon_t2m, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['t_2m'] >> plot_t2m_task

    plot_mslp_gh500mb_task = PythonOperator(task_id='plot_icon_mslp_gh500mb_%02dZ' % (cycle), python_callable=plot_icon_mslp_gh500mb, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['pmsl'] >> plot_mslp_gh500mb_task
    regrids['fi_500'] >> plot_mslp_gh500mb_task

    plot_1000_500mb_thickness_task = PythonOperator(task_id='plot_icon_1000_500mb_thickness_%02dZ' % (cycle), python_callable=plot_icon_1000_500mb_thickness, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['pmsl'] >> plot_1000_500mb_thickness_task
    regrids['fi_500'] >> plot_1000_500mb_thickness_task
    regrids['fi_1000'] >> plot_1000_500mb_thickness_task

    plot_precipitation_task = PythonOperator(task_id='plot_icon_precipitation_%02dZ' % (cycle), python_callable=plot_icon_precipitation, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['tot_prec'] >> plot_precipitation_task

    plot_rh2m_task = PythonOperator(task_id='plot_icon_rh2_%02dZ' % cycle, python_callable=plot_icon_rh2m, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['relhum_2m'] >> plot_rh2m_task

    plot_wind_task = PythonOperator(task_id='plot_icon_wind_%02dZ' % cycle, python_callable=plot_icon_wind10m, op_args=['/data', '/images', year, month, day, cycle, TIMESTEPS], dag=dag)
    regrids['u_10m'] >> plot_wind_task
    regrids['v_10m'] >> plot_wind_task

    evict_task = PythonOperator(task_id='evict_icon_%02d' % cycle, python_callable=delete_old_folders, op_args=['/data/NWP_ICON_GLOBAL_DWD/%02d' % cycle, 1], dag=dag)

    #logging.info("Creating folder renaming task")
    #renaming_task = PythonOperator(task_id='icon_rename_folder_%02d' % cycle, python_callable=rename_folder, op_args=[cycle, '/data'], dag=dag)
    operators[keys[len(keys)-1]] >> evict_task

# Export DAGS so Airflow can use them
for d in dags.keys():
    globals()[d] = dags[d]