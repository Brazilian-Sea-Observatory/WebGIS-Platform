import cartopy.crs as ccrs
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import os

from areas import AOIS
from plotting import coastline, borders, states_provinces, plot_map
from plotting import plot_temperature, plot_humidity, plot_precipitation, plot_wind, plot_1000_500mb_thickness
from plotting import plot_gh, plot_mslp

def plot_gefs_t2m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for air temperature at 2m from GFS
    """
    ds_tmp = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/TMP/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_tmp.longitude.values
    lats = ds_tmp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    values = ds_tmp.t2m.values - 273.15
    forecast_time = ds_tmp.time.values
    valid_time = ds_tmp.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    contour_step = AOIS[area]['t2m_contour_step']
    plot_temperature(ax, lons, lats, values, contour_step)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GEFS %02dZ - AIR TEMPERATURE\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GEFS_0p5/%02d/%s/%s/t2m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gefs-t2m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()
    ds_tmp.close()

def plot_gefs_rh2m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for relative humidity at 2m from GFS
    """
    ds_rh = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/RH/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_rh.longitude.values
    lats = ds_rh.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    values = ds_rh.r2.values
    forecast_time = ds_rh.time.values
    valid_time = ds_rh.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    contour_step = AOIS[area]['rh2m_contour_step']
    plot_humidity(ax, lons, lats, values, contour_step)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GEFS %02dZ - RELATIVE HUMIDITY\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GEFS_0p5/%02d/%s/%s/rh2m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gefs-rh2m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()


def plot_gefs_precipitation(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for total precipitation at surface from GFS
    """
    ds_tp = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/APCP/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_tp.longitude.values
    lats = ds_tp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    values = ds_tp.tp.values

    #if (t-1) % 6 == 0 or t == 1 or t >= 120:
    #     values = ds_tp.tp.values
    # else:
    #     ds_tp_previous = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/APCP/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t-1))
    #     values = ds_tp.tp.values - ds_tp_previous.tp.values
    #     ds_tp_previous.close()
    
    forecast_time = ds_tp.time.values
    valid_time = ds_tp.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    vmin = AOIS[area]['prec_min']
    vmax = AOIS[area]['prec_max']
    plot_precipitation(ax, lons, lats, values, vmin, vmax)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GEFS %02dZ - TOTAL PRECIPITATION\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GEFS_0p5/%02d/%s/%s/prec' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gefs-prec-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_tp.close()

def plot_gefs_wind10m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for wind at 10m
    """
    ds_ugrd = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/UGRD/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))
    ds_vgrd = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/VGRD/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_ugrd.longitude.values
    lats = ds_vgrd.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    u_values = ds_ugrd.u10.values
    v_values = ds_vgrd.v10.values

    resampling_factor = AOIS[area]['wind_resampling_factor']

    forecast_time = ds_ugrd.time.values
    valid_time = ds_ugrd.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    plot_wind(ax, lons, lats, u_values, v_values, resampling_factor)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GEFS %02dZ - WIND\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GEFS_0p5/%02d/%s/%s/wind10m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gefs-wind_10m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_ugrd.close()
    ds_vgrd.close()

def plot_gefs_mslp_gh500mb(area, cycle, t, data_dir, images_dir):
    ds_mslp = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/PRMSL/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))
    ds_gh = cfgrib.open_dataset('%s/NWP_GEFS_0p5/%02d/%s/latest/HGT/geavg.t%02dz.pgrb2a.0p50.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_mslp.longitude.values
    lats = ds_mslp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    mslp_values = ds_mslp.prmsl.values / 100
    gh_values = ds_gh.gh.values / 10

    main_step = AOIS[area]['pressure_main_step']
    secondary_step = AOIS[area]['pressure_secondary_step']

    forecast_time = ds_mslp.time.values
    valid_time = ds_mslp.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    plot_gh(ax, lons, lats, gh_values)
    plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GEFS %02dZ - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GEFS_0p5/%02d/%s/%s/mslp_gh500' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gefs-mslp-gh500-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_mslp.close()
    ds_gh.close()