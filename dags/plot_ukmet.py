import cartopy.crs as ccrs
import cfgrib
import pandas as pd
import logging
import matplotlib.pyplot as plt
import os
import xarray as xr

from areas import AOIS
from datetime import timedelta
from plotting import coastline, borders, states_provinces, plot_map
from plotting import plot_gh, plot_mslp 

def plot_ukmet(data_dir, images_dir, year, month, day, cycle):
    ds_ukmet = cfgrib.open_dataset(
        '%s/NWP_UKMET/%02d/%04d%02d%02d/nrukmet.t%02dz.ukm25.grib2' % 
        (data_dir, cycle, year, month, day, cycle))
    
    timesteps = (ds_ukmet.step.values / (60*60*1E9)).tolist()

    for step in timesteps:
        idx = timesteps.index(step)
        valid_time = (ds_ukmet.time + ds_ukmet.step[idx]).values
        valid_ts = pd.to_datetime(valid_time)
            
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
        forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_ukmet_area = ds_ukmet.where(
                (ds_ukmet.longitude >= llon - 2.) & 
                (ds_ukmet.longitude <= ulon + 2.) & 
                (ds_ukmet.latitude >= llat - 2.) & 
                (ds_ukmet.latitude <= ulat + 2.), drop=True)

            lons = ds_ukmet_area.longitude.values
            lats = ds_ukmet_area.latitude.values

            idx = timesteps.index(step)
            
            mslp_values = ds_ukmet_area.prmsl[idx].values / 100
            gh_values = ds_ukmet_area.gh[idx].values / 10

            main_step = AOIS[area]['pressure_main_step']
            secondary_step = AOIS[area]['pressure_secondary_step']

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            plot_gh(ax, lons, lats, gh_values)
            plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            plt.title('UKMET %02dZ - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_UKMET/%02d/%04d%02d%02d/%s/mslp_gh500' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/ukmet-mslp-gh500-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_ukmet.close()