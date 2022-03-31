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
from plotting import plot_temperature, plot_humidity, plot_precipitation, plot_wind, plot_gh, plot_mslp, plot_1000_500mb_thickness

def plot_gmc_1000_500mb_thickness(data_dir, images_dir, year, month, day, cycle, timesteps):
    for step in timesteps:
        ds_mslp = cfgrib.open_dataset('%s/NWP_GMC_GPSS/%02d/%04d%02d%02d/PRMSL_MSL_0/CMC_glb_PRMSL_MSL_0_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        ds_gh = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/HGT_ISBL_500/CMC_glb_HGT_ISBL_500_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_mslp_area = ds_mslp.where(
                (ds_mslp.longitude >= llon) & 
                (ds_mslp.longitude <= ulon) & 
                (ds_mslp.latitude >= llat) & 
                (ds_mslp.latitude <= ulat), drop=True)

            ds_gh_area = ds_gh.where(
                (ds_gh.longitude >= llon) & 
                (ds_gh.longitude <= ulon) & 
                (ds_gh.latitude >= llat) & 
                (ds_gh.latitude <= ulat), drop=True)

            lons = ds_mslp_area.longitude.values
            lats = ds_mslp_area.latitude.values
            
            mslp_values = ds_mslp_area.prmsl.values / 100
            gh_values = ds_gh_area.thick.values / 10

            main_step = AOIS[area]['pressure_main_step']
            secondary_step = AOIS[area]['pressure_secondary_step']

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
            plot_1000_500mb_thickness(ax, lons, lats, gh_values)
            plot_map(ax, area, coastline, borders, states_provinces)

            valid_time = ds_mslp.time.values
            valid_ts = pd.to_datetime(valid_time)
            
            valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
            forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

            plt.title('GMC %02dZ - PRMSL x 1000 - 500mb THICKNESS\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/1000_500mb_thickness' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-prsml-1000_500mb_thickness-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_mslp.close()
        ds_gh.close()

def plot_gmc_mslp_gh500mb(data_dir, images_dir, year, month, day, cycle, timesteps):
    for step in timesteps:
        ds_mslp = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/PRMSL_MSL_0/CMC_glb_PRMSL_MSL_0_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        ds_gh = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/CMC_glb_PRMSL_MSL_0_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))

        valid_time = ds_mslp.time.values[0]
        valid_ts = pd.to_datetime(valid_time)
            
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
        forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_mslp_area = ds_mslp.where(
                (ds_mslp.longitude >= llon) & 
                (ds_mslp.longitude <= ulon) & 
                (ds_mslp.latitude >= llat) & 
                (ds_mslp.latitude <= ulat), drop=True)

            ds_gh_area = ds_gh.where(
                (ds_gh.longitude >= llon) & 
                (ds_gh.longitude <= ulon) & 
                (ds_gh.latitude >= llat) & 
                (ds_gh.latitude <= ulat), drop=True)

            lons = ds_mslp_area.longitude.values
            lats = ds_mslp_area.latitude.values
            
            mslp_values = ds_mslp_area.prmsl.values / 100
            gh_values = ds_gh_area.thick.values / 10

            main_step = AOIS[area]['pressure_main_step']
            secondary_step = AOIS[area]['pressure_secondary_step']

            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            plot_gh(ax, lons, lats, gh_values)
            plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            plt.title('GMC %02dZ - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/mslp_gh500' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-mslp-gh500-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_mslp.close()
        ds_gh.close()


def plot_gmc_t2m(data_dir, images_dir, year, month, day, cycle, timesteps):
    for step in timesteps:
        ds_t2m = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/TMP_TGL_2/CMC_glb_TMP_TGL_2_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))

        valid_time = ds_t2m.time.values
        valid_ts = pd.to_datetime(valid_time)
            
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')
        forecast_str = '%04d-%02d-%02d %02dZ' % (year, month, day, cycle)

        for area in AOIS.keys():
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_t2m_area = ds_t2m.where(
                (ds_t2m.longitude >= llon) & 
                (ds_t2m.longitude <= ulon) & 
                (ds_t2m.latitude >= llat) & 
                (ds_t2m.latitude <= ulat), drop=True)

            lons = ds_t2m_area.longitude.values
            lats = ds_t2m_area.latitude.values
            
            values = ds_t2m_area.t2m.values - 273.15
            fig = plt.figure(figsize=(10,10))
            ax = plt.axes(projection=ccrs.PlateCarree())

            ax.set_xlim(llon, ulon)
            ax.set_ylim(llat, ulat)

            contour_step = AOIS[area]['t2m_contour_step']
            plot_temperature(ax, lons, lats, values, contour_step)
            plot_map(ax, area, coastline, borders, states_provinces)

            plt.title('GMC %02dZ - AIR TEMPERATURE 2m\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/t2m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-t2m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)

        ds_t2m.close()

def plot_gmc_rh2m(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for relative humidity at 2m for GMC
    """
    for step in timesteps:
        ds_rh = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/RH_TGL_2/CMC_glb_RH_TGL_2_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        
        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_rh_area = ds_rh.where(
                (ds_rh.longitude >= llon) & 
                (ds_rh.longitude <= ulon) & 
                (ds_rh.latitude >= llat) & 
                (ds_rh.latitude <= ulat))

            lons = ds_rh_area.longitude.values
            lats = ds_rh_area.latitude.values

            valid_time = ds_rh_area.time.values

            values = ds_rh_area.r2.values

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

            plt.title('GMC %02dZ - RELATIVE HUMIDITY 2m\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/rh2m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-rh2m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_rh.close()

def plot_gmc_precipitation(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for precipitation at surface for GMC
    """
    for step in timesteps:
        ds_tp = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/APCP_SFC_0/CMC_glb_APCP_SFC_0_latlon_.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        
        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_tp_area = ds_tp.where(
                (ds_tp.longitude >= llon) & 
                (ds_tp.longitude <= ulon) & 
                (ds_tp.latitude >= llat) & 
                (ds_tp.latitude <= ulat))

            lons = ds_tp_area.longitude.values
            lats = ds_tp_area.latitude.values

            valid_time = ds_tp_area.time.values

            values = ds_tp_area['unknown'].values

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

            plt.title('GMC %02dZ - TOTAL PRECIPITATION\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/prec' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-prec-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_tp.close()

def plot_gmc_wind10m(data_dir, images_dir, year, month, day, cycle, timesteps):
    """
    Generate figures for wind at 10m for GMC
    """
    for step in timesteps:
        ds_u10 = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/UGRD_TGL_10/CMC_glb_UGRD_TGL_10_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        ds_v10 = cfgrib.open_dataset('%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/VGRD_TGL_10/CMC_glb_VGRD_TGL_10_latlon.24x.24_%02d_P%03d.grib2' % (data_dir, cycle, year, month, day, cycle, step))
        
        valid_time = ds_u10.time.values[0]

        for area in AOIS:
            llon = AOIS[area]['llon']
            ulon = AOIS[area]['ulon']
            llat = AOIS[area]['llat']
            ulat = AOIS[area]['ulat']

            ds_u10_area = ds_u10.where(
                (ds_u10.longitude >= llon) & 
                (ds_u10.longitude <= ulon) & 
                (ds_u10.latitude >= llat) & 
                (ds_u10.latitude <= ulat))
            ds_v10_area = ds_u10.where(
                (ds_v10.longitude >= llon) & 
                (ds_v10.longitude <= ulon) & 
                (ds_v10.latitude >= llat) & 
                (ds_v10.latitude <= ulat))

            lons = ds_u10_area.longitude.values
            lats = ds_u10_area.latgitude.values

            u_values = ds_u10_area.u10.values
            v_values = ds_v10_area.v10.values

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

            plt.title('GMC %02dZ - WIND AT 10m\nFORECAST TIME: %s - VALID TIME: %s - STEP: %03d' % (cycle, forecast_str, valid_str, step))

            output_folder = '%s/NWP_GMC_GPDS/%02d/%04d%02d%02d/%s/wind_10m' % (images_dir, cycle, year, month, day, area)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filepath = '%s/gmc-wind_10m-%03d.png' % (output_folder, step)
            plt.savefig(filepath)
            plt.close()

            logging.info('Generated %s' % filepath)
        
        ds_u10.close()
        ds_v10.close()

