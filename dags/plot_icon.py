import cartopy.crs as ccrs
import pandas as pd
import logging
import matplotlib.pyplot as plt
import os
import xarray as xr

from areas import AOIS
from datetime import timedelta
from plotting import coastline, borders, states_provinces, plot_map
from plotting import plot_temperature, plot_humidity, plot_precipitation, plot_wind, plot_gh, plot_mslp, plot_1000_500mb_thickness

def plot_icon_1000_500mb_thickness(data_dir, images_dir, year, month, day, cycle, timesteps):
    for step in timesteps:
        ds_mslp = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/pmsl/icon_global_icosahedral_single-level_%03d_pmsl.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        ds_gh500 = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/fi_500/icon_global_icosahedral_pressure-level_%03d_fi_500.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        ds_gh1000 = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/fi_1000/icon_global_icosahedral_pressure-level_%03d_fi_1000.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_mslp_area = ds_mslp.where((ds_mslp.lon >= llon) & (ds_mslp.lon <= ulon) & (ds_mslp.lat >= llat) & (ds_mslp.lat <= ulat), drop=True)
            ds_gh500_area = ds_gh500.where((ds_gh500.lon >= llon) & (ds_gh500.lon <= ulon) & (ds_gh500.lat >= llat) & (ds_gh500.lat <= ulat), drop=True)
            ds_gh1000_area = ds_gh1000.where((ds_gh1000.lon >= llon) & (ds_gh1000.lon <= ulon) & (ds_gh1000.lat >= llat) & (ds_gh1000.lat <= ulat), drop=True)

            lons = ds_mslp_area.lon.values
            lats = ds_mslp_area.lat.values
            
            mslp_values = ds_mslp_area.prmsl[0,:,:].values / 100
            gh_values = (ds_gh500_area.z[0,0,:,:].values - ds_gh1000_area.z[0,0,:,:].values)/100

            main_step = AOIS[area]['pressure_main_step']
            secondary_step = AOIS[area]['pressure_secondary_step']

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
            plot_1000_500mb_thickness(ax, lons, lats, gh_values)
            plot_map(ax, area, coastline, borders, states_provinces)

            valid_time = ds_mslp.time.values[0]
            valid_ts = pd.to_datetime(valid_time)
            
            valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
            forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

            plt.title('ICON %02dZ - PRMSL x 1000 - 500mb THICKNESS\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/1000_500mb_thickness' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-prsml-1000_500mb_thickness-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_mslp.close()
        ds_gh500.close()
        ds_gh1000.close()


def plot_icon_mslp_gh500mb(data_dir, images_dir, year, month, day, cycle, timesteps):
    for step in timesteps:
        ds_mslp = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/pmsl/icon_global_icosahedral_single-level_%03d_pmsl.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        ds_gh = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/fi_500/icon_global_icosahedral_pressure-level_%03d_fi_500.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')

        valid_time = ds_mslp.time.values[0]
        valid_ts = pd.to_datetime(valid_time)
            
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
        forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

        for area in AOIS.keys():
            main_step = AOIS[area]['pressure_main_step']
            secondary_step = AOIS[area]['pressure_secondary_step']

            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_mslp_area = ds_mslp.where((ds_mslp.lon >= llon) & (ds_mslp.lon <= ulon) & (ds_mslp.lat >= llat) & (ds_mslp.lat <= ulat), drop=True)
            ds_gh_area = ds_gh.where((ds_gh.lon >= llon) & (ds_gh.lon <= ulon) & (ds_gh.lat >= llat) & (ds_gh.lat <= ulat), drop=True)

            lons = ds_mslp_area.lon.values
            lats = ds_mslp_area.lat.values
            
            mslp_values = ds_mslp_area.prmsl[0,:,:].values / 100
            gh_values = ds_gh_area.z[0,0,:,:].values / 100

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            plot_gh(ax, lons, lats, gh_values)
            plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            plt.title('ICON DWD %02dZ - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/mslp_gh500' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-mslp-gh500-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_mslp.close()
        ds_gh.close()


def plot_icon_t2m(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for air temperature at 2m for ICON
    """
    for step in timesteps:
        ds_tmp = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/t_2m/icon_global_icosahedral_single-level_%03d_t_2m.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_tmp_area = ds_tmp.where((ds_tmp.lon >= llon) & (ds_tmp.lon <= ulon) & (ds_tmp.lat >= llat) & (ds_tmp.lat <= ulat))

            lons = ds_tmp_area.lon.values
            lats = ds_tmp_area.lat.values

            values = ds_tmp_area['2t'][0,0,:,:].values - 273.15
            valid_time = ds_tmp_area.time.values[0]

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            contour_step = AOIS[area]['t2m_contour_step']
            plot_temperature(ax, lons, lats, values, contour_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            valid_ts = pd.to_datetime(str(valid_time)) 
            valid_str = valid_ts.strftime('%Y-%m-%d %HZ')

            plt.title('ICON DWD - AIR TEMPERATURE 2m\nFORECAST TIME: %04d-%02d-%02d %02dZ - VALID TIME: %s - STEP: %03d' % (year, month, day, cycle, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/t2m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-t2m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_tmp.close()

def plot_icon_rh2m(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for relative humidity at 2m for ICON
    """
    for step in timesteps:
        ds_rh = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/relhum_2m/icon_global_icosahedral_single-level_%03d_relhum_2m.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        
        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_rh_area = ds_rh.where((ds_rh.lon >= llon) & (ds_rh.lon <= ulon) & (ds_rh.lat >= llat) & (ds_rh.lat <= ulat))

            lons = ds_rh_area.lon.values
            lats = ds_rh_area.lat.values

            valid_time = ds_rh_area.time.values[0]

            values = ds_rh_area['2r'][0,0,:,:].values

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            contour_step = AOIS[area]['rh2m_contour_step']
            plot_humidity(ax, lons, lats, values, contour_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

            valid_ts = pd.to_datetime(str(valid_time)) 
            valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

            plt.title('ICON %02dZ - RELATIVE HUMIDITY 2m\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/rh2m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-rh2m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_rh.close()

def plot_icon_precipitation(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for precipitation at surface for ICON
    """
    for step in timesteps:
        ds_tp = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/tot_prec/icon_global_icosahedral_single-level_%03d_tot_prec.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        
        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_tp_area = ds_tp.where((ds_tp.lon >= llon) & (ds_tp.lon <= ulon) & (ds_tp.lat >= llat) & (ds_tp.lat <= ulat))

            lons = ds_tp_area.lon.values
            lats = ds_tp_area.lat.values

            valid_time = ds_tp_area.time.values[0]

            values = ds_tp_area['tp'][0,:,:].values

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            vmin = AOIS[area]['prec_min']
            vmax = AOIS[area]['prec_max']
            plot_precipitation(ax, lons, lats, values, vmin, vmax)
            plot_map(ax, area, coastline, borders, states_provinces)

            forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

            valid_ts = pd.to_datetime(str(valid_time)) 
            valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

            plt.title('ICON %02dZ - TOTAL PRECIPITATION\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/prec' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-prec-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_tp.close()


def plot_icon_wind10m(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for wind at 10m for ICON
    """
    for step in timesteps:
        ds_u10 = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/u_10m/icon_global_icosahedral_single-level_%03d_u_10m.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        ds_v10 = xr.open_dataset('%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/v_10m/icon_global_icosahedral_single-level_%03d_v_10m.nc' % (data_dir, cycle, year, month, day, step), engine='netcdf4')
        
        valid_time = ds_u10.time.values[0]

        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_u10_area = ds_u10.where((ds_u10.lon >= llon) & (ds_u10.lon <= ulon) & (ds_u10.lat >= llat) & (ds_u10.lat <= ulat))
            ds_v10_area = ds_u10.where((ds_v10.lon >= llon) & (ds_v10.lon <= ulon) & (ds_v10.lat >= llat) & (ds_v10.lat <= ulat))

            lons = ds_u10_area.lon.values
            lats = ds_u10_area.lat.values

            u_values = ds_u10_area['10u'][0,0,:,:].values
            v_values = ds_v10_area['10u'][0,0,:,:].values

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            resampling_factor = AOIS[area]['wind_resampling_factor']
            plot_wind(ax, lons, lats, u_values, v_values, resampling_factor)
            plot_map(ax, area, coastline, borders, states_provinces)

            forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

            valid_ts = pd.to_datetime(str(valid_time)) 
            valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

            plt.title('ICON %02dZ - WIND AT 10m\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_ICON_GLOBAL_DWD/%02d/%04d%02d%02d/%s/wind_10m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/icon-wind_10m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_u10.close()
        ds_v10.close()

