import json
import math
import os
import time
import pwd
import grp
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent


def get_datetime(tdelta):
    return (datetime(1950,1,1) + timedelta(hours=tdelta)).strftime('%Y-%m-%d %H:%M:%S')

def get_data(variable_data, time=0, depth=0):
    v=[]
    for lat in reversed(range(1, variable_data.data.shape[2], 12)):
        for lon in range(0, variable_data.data.shape[3], 12):
            value = variable_data.data[time, depth, lat, lon]
            v.append(value if not xr.ufuncs.isnan(value) else 0.)
    return v

def variable_to_json(file, variable_name, time, pnumber, model='global'):
    netcdf_data = xr.open_dataset(file)
    variable_data = netcdf_data[variable_name]
    json_data = {}
    json_data['header'] = {}
    json_data['header']['dx'] = 1.
    json_data['header']['dy'] = 1.
    if model == 'global':
        json_data['header']['la1'] = netcdf_data['latitude'].attrs['valid_max']
        json_data['header']['la2'] = netcdf_data['latitude'].attrs['valid_min']
        json_data['header']['lo1'] = netcdf_data['longitude'].attrs['valid_max']
        json_data['header']['lo2'] = netcdf_data['longitude'].attrs['valid_min']
        if (variable_name == 'uo'):
            json_data['header']['parameterNumberName'] = 'Eastward current'
        else:
            json_data['header']['parameterNumberName'] = 'Northward current'
    else:
        json_data['header']['la1'] = netcdf_data['lat'].attrs['valid_max']
        json_data['header']['la2'] = netcdf_data['lat'].attrs['valid_min']
        json_data['header']['lo1'] = netcdf_data['lon'].attrs['valid_max']
        json_data['header']['lo2'] = netcdf_data['lon'].attrs['valid_min']
        if (variable_name == 'u'):
            json_data['header']['parameterNumberName'] = 'Eastward current'
        else:
            json_data['header']['parameterNumberName'] = 'Northward current'
        
    json_data['header']['nx'] = 360
    json_data['header']['ny'] = 170
    json_data['header']['parameterCategory'] = 2
    json_data['header']['parameterNumber'] = pnumber
    json_data['header']['parameterUnit'] = 'm.s-1'
    json_data['header']['refTime'] = pd.to_datetime(time).strftime('%Y-%m-%d %H:%M:%S')

    json_data['data'] = get_data(variable_data)
    return json_data


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return round(float(obj), 2)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def netcdf_to_json(file, model='global'):
    data = xr.open_dataset(file)
    for time in data['time'].data:
        output = []
        output.append(variable_to_json(file, 'uo' if model == 'global' else 'u', time, 2, model))
        output.append(variable_to_json(file, 'vo' if model == 'global' else 'v', time, 3, model))
        if model == 'global':
            outfile = os.path.join(os.path.sep, o_dir, pd.to_datetime(time).strftime('%Y-%m-%d') + '.json')
        else:
            outfile = os.path.join(os.path.sep, o_dir, model, pd.to_datetime(time).strftime('%Y-%m-%d') + '.json')
        with open(outfile, 'w') as f:
            f.write(json.dumps(output, cls=MyEncoder))


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            if 'babitonga_hydrodinamic' in event.src_path:
                netcdf_to_json(event.src_path, model='babitonga')
            elif 'cep_hydrodinamic' in event.src_path:
                netcdf_to_json(event.src_path, model='cep')
            elif 'pr_sc_hydrodinamic' in event.src_path:
                netcdf_to_json(event.src_path, model='pr_sc')
            elif 'hydrodinamic' in event.src_path:
                netcdf_to_json(event.src_path, model='regional')
            else:
                netcdf_to_json(event.src_path)

if __name__ == '__main__':
    base = '/home'
    i_dir_gl = os.path.join(os.path.sep, base, 'geoserver-data/mercator_products/vector_speed_forecast_daily')
    i_dir_rg = os.path.join(os.path.sep, base, 'geoserver-data/mercator_products/last_regional_models')
    o_dir = os.path.join(os.path.sep, base, 'leaflet_velocity')

    i_file = os.path.join(os.path.sep, i_dir_gl, "vector_speed_forecast_daily_1.nc")
    netcdf_to_json(i_file)

    #event_handler = EventHandler()
    # observer = Observer()
    # observer.schedule(event_handler, i_dir_gl, recursive=True)
    for model in ['babitonga', 'cep', 'pr_sc']:
        i_file = os.path.join(os.path.sep, i_dir_rg, model + "_hydrodinamic/latest_hydro_model_1.nc")
        netcdf_to_json(i_file, model)

        # observer.schedule(event_handler, os.path.join(os.path.sep, i_dir_rg, model+'_hydrodinamic'), recursive=True)

    i_file = os.path.join(os.path.sep, i_dir_rg, "hydrodinamic/latest_hydro_model_1.nc")
    netcdf_to_json(i_file, model='regional')
    #observer.schedule(event_handler, os.path.join(os.path.sep, i_dir_rg, 'hydrodinamic'), recursive=True)

    #observer.start()
    #try:
    #    while True:
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    observer.stop()
    #observer.join()

