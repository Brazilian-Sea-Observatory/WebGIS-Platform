import cartopy.crs as ccrs
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import os

from areas import AOIS
from plotting import coastline, borders, states_provinces, plot_map
from plotting import plot_temperature, plot_humidity, plot_precipitation, plot_wind, plot_gh, plot_mslp

def plot_ecmwf_mslp_gh500mb(cycle, t, data_dir, images_dir):
    ds_mslp = cfgrib.open_dataset('%s/NWP_ECMWF_WMO/%02d/latest/msl/msl_%03dZ_global_0p5deg_grib2.bin' % (data_dir, cycle, t))
    ds_gh = cfgrib.open_dataset('%s/NWP_ECMWF_WMO/%02d/latest/gh_500/gh_500_%03dZ_global_0p5deg_grib2.bin' % (data_dir, cycle, t))

    forecast_time = ds_mslp.time.values
    valid_time = ds_mslp.valid_time.values

    for area in AOIS.keys():
        main_step = AOIS[area]['pressure_main_step']
        secondary_step = AOIS[area]['pressure_secondary_step']

        llon = AOIS[area]['llon']
        ulon = AOIS[area]['ulon']
        llat = AOIS[area]['llat']
        ulat = AOIS[area]['ulat']

        ds_mslp_area = ds_mslp.where((ds_mslp.longitude >= llon) & (ds_mslp.longitude <= ulon) & (ds_mslp.latitude >= llat) & (ds_mslp.latitude <= ulat), drop=True)
        ds_gh_area = ds_gh.where((ds_gh.longitude >= llon) & (ds_gh.longitude <= ulon) & (ds_gh.latitude >= llat) & (ds_gh.latitude <= ulat), drop=True)

        lons = ds_mslp_area.longitude.values
        lats = ds_mslp_area.latitude.values

        mslp_values = ds_mslp_area.msl.values / 100
        gh_values = ds_gh_area.gh.values / 10

        fig = plt.figure(figsize=(10,10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.set_xlim(llon, ulon)
        ax.set_ylim(llat, ulat)

        plot_gh(ax, lons, lats, gh_values)
        plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
        plot_map(ax, area, coastline, borders, states_provinces)

        forecast_ts = pd.to_datetime(str(forecast_time))
        forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

        valid_ts = pd.to_datetime(str(valid_time)) 
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

        plt.title('ECMWF %02dZ - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

        output_folder = '%s/NWP_ECMWF_WMO/%02d/%s/%s/mslp_gh500' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        filepath = '%s/ecmwf-mslp-gh500-%03d.png' % (output_folder, t)
        plt.savefig(filepath)
        plt.close()

    ds_mslp.close()
    ds_gh.close()

def plot_ecmwf_t850mb(cycle, t, data_dir, images_dir):
    """
    Generate figures for air temperature at 850mb from ECMWF
    """
    ds_tmp = cfgrib.open_dataset('%s/NWP_ECMWF_WMO/%02d/latest/t_850/t_850_%03dZ_global_0p5deg_grib2.bin' % (data_dir, cycle, t))

    forecast_time = ds_tmp.time.values
    valid_time = ds_tmp.valid_time.values

    for area in AOIS.keys():
        llon = AOIS[area]['llon']
        ulon = AOIS[area]['ulon']
        llat = AOIS[area]['llat']
        ulat = AOIS[area]['ulat']

        ds_tmp_area = ds_tmp.where((ds_tmp.longitude >= llon) & (ds_tmp.longitude <= ulon) & (ds_tmp.latitude >= llat) & (ds_tmp.latitude <= ulat), drop=True)

        lons = ds_tmp_area.longitude.values
        lats = ds_tmp_area.latitude.values

        values = ds_tmp_area.t.values - 273.15

        fig = plt.figure(figsize=(10,10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        contour_step = AOIS[area]['t2m_contour_step']
        plot_temperature(ax, lons, lats, values, contour_step)
        plot_map(ax, area, coastline, borders, states_provinces)

        forecast_ts = pd.to_datetime(str(forecast_time))
        forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

        valid_ts = pd.to_datetime(str(valid_time)) 
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

        plt.title('ECMWF %02dZ - AIR TEMPERATURE 850mb\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

        output_folder = '%s/NWP_ECMWF_WMO/%02d/%s/%s/t850' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        filepath = '%s/ecmwf-t850-%03d.png' % (output_folder, t)
        plt.savefig(filepath)
        plt.close()

    ds_tmp.close()

def plot_ecmwf_wind850mb(cycle, t, data_dir, images_dir):
    """
    Generate figures for wind at 850mb
    """
    ds_u = cfgrib.open_dataset('%s/NWP_ECMWF_WMO/%02d/latest/u_850/u_850_%03dZ_global_0p5deg_grib2.bin' % (data_dir, cycle, t))
    ds_v = cfgrib.open_dataset('%s/NWP_ECMWF_WMO/%02d/latest/v_850/v_850_%03dZ_global_0p5deg_grib2.bin' % (data_dir, cycle, t))

    for area in AOIS.keys():
        llon = AOIS[area]['llon']
        ulon = AOIS[area]['ulon']
        llat = AOIS[area]['llat']
        ulat = AOIS[area]['ulat']

        ds_u_area = ds_u.where((ds_u.longitude >= llon) & (ds_u.longitude <= ulon) & (ds_u.latitude >= llat) & (ds_u.latitude <= ulat), drop=True)
        ds_v_area = ds_v.where((ds_v.longitude >= llon) & (ds_v.longitude <= ulon) & (ds_v.latitude >= llat) & (ds_v.latitude <= ulat), drop=True)

        lons = ds_u_area.longitude.values
        lats = ds_v_area.latitude.values

        u_values = ds_u_area.u.values
        v_values = ds_v_area.v.values

        resampling_factor = AOIS[area]['wind_resampling_factor']

        forecast_time = ds_u.time.values
        valid_time = ds_u.valid_time.values

        fig = plt.figure(figsize=(10,10))
        ax = plt.axes(projection=ccrs.PlateCarree())

        plot_wind(ax, lons, lats, u_values, v_values, resampling_factor)
        plot_map(ax, area, coastline, borders, states_provinces)

        forecast_ts = pd.to_datetime(str(forecast_time))
        forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

        valid_ts = pd.to_datetime(str(valid_time)) 
        valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

        plt.title('ECMWF %02dZ - WIND 850mb\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

        output_folder = '%s/NWP_ECMWF_WMO/%02d/%s/%s/wind850' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        filepath = '%s/ecmwf-wind_850-%03d.png' % (output_folder, t)
        plt.savefig(filepath)
        plt.close()

    ds_u.close()
    ds_v.close()