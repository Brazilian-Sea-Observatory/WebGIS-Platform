import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import cfgrib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import pandas as pd
import xarray as xr

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from areas import AOIS
from matplotlib.font_manager import FontProperties
from palettable.cartocolors.diverging import Temps_4
from palettable.colorbrewer.diverging import Spectral_7_r

borders = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_boundary_lines_land',
        scale='10m',
        facecolor='none')

coastline = cfeature.NaturalEarthFeature(
    category='physical',
    name='coastline',
    scale='10m',
    facecolor='none'
)

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none'
)

shp_fn = shpreader.natural_earth(resolution='10m', category='cultural', name='populated_places')
shp = shpreader.Reader(shp_fn)
cities = [{'longitude': r.attributes['LONGITUDE'],
           'latitude': r.attributes['LATITUDE'],
           'rank': r.attributes['LABELRANK'],
           'name': r.attributes['NAME']} for r in shp.records()]


shp_fn = shpreader.natural_earth(resolution='110m',
                                  category='cultural',
                                  name='admin_0_countries')
shp = shpreader.Reader(shp_fn)
countries = [{'longitude': r.geometry.representative_point().x, 
              'latitude': r.geometry.representative_point().y,
              'name': r.attributes['NAME']} for r in shp.records()]

class nf(float):
    def __repr__(self):
        str = '%.1f' % (self.__float__(),)
        if str[-1] == '0':
            return '%.0f' % self.__float__()
        else:
            return '%.1f' % self.__float__()

def plot_map(ax, area, coastline, borders, states_provinces):
    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    filtered_cities = [c for c in cities if
                      c['name'] in AOIS[area]['cities']]
    
    filtered_countries = [c for c in countries if
                          c['latitude'] > AOIS[area]['llat'] and
                          c['latitude'] < AOIS[area]['ulat'] and
                          c['longitude'] > AOIS[area]['llon'] and
                          c['longitude'] < AOIS[area]['ulon']]
    
    ax.add_feature(coastline, linewidth=1, edgecolor='gray')
    ax.add_feature(borders, linewidth=1, edgecolor='gray')
    ax.add_feature(states_provinces, linewidth=0.5, edgecolor='gray', linestyles=':')

    # Annotate cities
    x = [c['longitude'] for c in filtered_cities]
    y = [c['latitude'] for c in filtered_cities]
    names = [c['name'] for c in filtered_cities]

    ax.scatter(x,
               y,
               25,
               marker='o',
               edgecolors='none',
               color='black')
    
    for i, c in enumerate(names):
        ax.annotate(names[i],
                    (x[i], y[i]),
                    xytext=(0, 5),
                    textcoords='offset pixels',
                    color='black')
        
    # Annotate countries
    x = [c['longitude'] for c in filtered_countries]
    y = [c['latitude'] for c in filtered_countries]
    names = [c['name'] for c in filtered_countries]

    ax.scatter(x,
               y,
               25,
               marker='o',
               edgecolors='none',
               color='black')
    
    font_bold = FontProperties()
    font_bold.set_weight('bold')

    for i, c in enumerate(names):
        ax.annotate(names[i].upper(),
                    (x[i], y[i]),
                    xytext=(0, 5),
                    textcoords='offset pixels',
                    color='black',
                    fontproperties=font_bold
                   )
        
    # Add lat/lon decoration
    ax.set_xticks(np.linspace(llon, ulon, 5), crs=ccrs.PlateCarree())
    ax.set_yticks(np.linspace(llat, ulat, 5), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

def plot_mslp(ax, lons, lats, values, main_step, secondary_step, color='black'):
    """
    Plot Mean Sea Level Pressure as contours
    """
    CS = ax.contour(lons, lats, values, levels=range(800,1100,main_step), linewidths=2, colors=color)
    CS.levels = [nf(val) for val in CS.levels]
    ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=8)

    CS = ax.contour(lons, lats, values, levels=range(800,1100,secondary_step), linewidths=1, colors=color)
    CS.levels = [nf(val) for val in CS.levels]
    ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=8)

def plot_1000_500mb_thickness(ax, lons, lats, values):
    """
    Plot 1000-500mb thickness
    """
    CS = plt.contour(lons, lats, values, levels=range(450, 540, 5), colors='blue', linestyles='dashed', linewidths=1)
    CS.levels = [nf(val) for val in CS.levels]
    ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=8)

    CS = plt.contour(lons, lats, values, levels=[540], colors='red',  linewidths=2)
    CS.levels = [nf(val) for val in CS.levels]
    ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=8)

    CS = plt.contour(lons, lats, values, levels=range(545, 650, 5), colors='red',  linestyles='dashed', linewidths=1)
    CS.levels = [nf(val) for val in CS.levels]
    ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=8)

def plot_temperature(ax, lons, lats, values, contour_step):
    """
    Plot temperatures at 2m using contours
    """
    im = plt.contourf(lons, lats, values, levels=range(-20, 45), cmap = cm.get_cmap('rainbow'))
    cbar = plt.colorbar(im, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label("Air temperature (C)")

    CS = plt.contour(lons, lats, values, levels=range(-20, 45, contour_step), colors='white')
    ax.clabel(CS, CS.levels, inline=True, fmt='%d', fontsize=10)

def plot_humidity(ax, lons, lats, values, contour_step):
    """
    Plot relative humidity at 2m using contours
    """
    im = plt.contourf(lons, lats, values, levels=range(0, 100), cmap = cm.get_cmap('coolwarm_r'))
    cbar = plt.colorbar(im, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label("Relative humidity (%)")

    CS = plt.contour(lons, lats, values, levels=range(0, 50, contour_step), colors='white', linestyles='dashed')
    ax.clabel(CS, CS.levels, inline=True, fmt='%d', fontsize=10)

    CS = plt.contour(lons, lats, values, levels=range(50, 100, contour_step), colors='white')
    ax.clabel(CS, CS.levels, inline=True, fmt='%d', fontsize=10)

def plot_precipitation(ax, lons, lats, values, vmin, vmax):
    """
    Plot total precipitation at surface
    """
    cmap = Temps_4.mpl_colormap
    cmap.set_under('w')

    dx = (lons[1]-lons[0])/2.
    dy = (lats[1]-lats[0])/2.
    extent = [lons[0]-dx, lons[-1]+dx, lats[0]-dy, lats[-1]+dy]

    im=plt.imshow(values, extent=extent, vmin=vmin, vmax=vmax, cmap=cmap, interpolation='spline16')
    cbar = plt.colorbar(im, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label("Accumulated Precipitation at Surface (mm)")

def plot_wind(ax, lons, lats, u_values, v_values, resampling_factor):
    wind_speed = np.sqrt(u_values * u_values, v_values * v_values) * 3.6
    im = plt.contourf(lons, lats, wind_speed, levels = range(0, 80), cmap = Spectral_7_r.mpl_colormap)
    cbar = plt.colorbar(im, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label("Wind Speed at 10 m (km/h)")
    if resampling_factor > 1:
        lons = lons[::resampling_factor]
        lats = lats[::resampling_factor]
        u_values = u_values[::resampling_factor,::resampling_factor]
        v_values = v_values[::resampling_factor,::resampling_factor]
    ax.barbs(lons, lats, u_values, v_values, color='white')

def plot_gh(ax, lons, lats, values):
    im = plt.contourf(lons, lats, values, cmap=cm.rainbow, levels=range(480,600))
    cbar = plt.colorbar(im, orientation='horizontal', fraction=0.046, pad=0.04)
    cbar.set_label("Geopotencial Height (dm)")

def plot_gfs_1000_500mb_thickness(area, cycle, t, data_dir, images_dir):
    ds_mslp = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/PRMSL/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))
    ds_gh = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/HGT/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_mslp.longitude.values
    lats = ds_mslp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    mslp_values = ds_mslp.prmsl.values / 100
    gh_values = (ds_gh.gh[2].values - ds_gh.gh[0].values) / 10

    main_step = AOIS[area]['pressure_main_step']
    secondary_step = AOIS[area]['pressure_secondary_step']

    forecast_time = ds_mslp.time.values
    valid_time = ds_mslp.valid_time.values

    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    plot_mslp(ax, lons, lats, mslp_values, main_step, secondary_step)
    plot_1000_500mb_thickness(ax, ds_gh.longitude, ds_gh.latitude, gh_values)
    plot_map(ax, area, coastline, borders, states_provinces)

    forecast_ts = pd.to_datetime(str(forecast_time))
    forecast_str = forecast_ts.strftime('%Y-%m-%d %H:%M Z')

    valid_ts = pd.to_datetime(str(valid_time)) 
    valid_str = valid_ts.strftime('%Y-%m-%d %H:%M Z')

    plt.title('GFS 00Z - PRMSL x 1000 - 500mb THICKNESS\nFORECAST TIME: %s - VALID TIME: %s' % (forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/1000_500mb_thickness' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-prsml-1000_500mb_thickness-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_mslp.close()
    ds_gh.close()

def plot_gfs_mslp_gh500mb(area, cycle, t, data_dir, images_dir):
    ds_mslp = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/PRMSL/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))
    ds_gh = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/HGT/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_mslp.longitude.values
    lats = ds_mslp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    mslp_values = ds_mslp.prmsl.values / 100
    gh_values = ds_gh.gh[2].values / 10

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

    plt.title('GFS 00Z - PRMSL x GEOPOTENTIAL HEIGHT\nFORECAST TIME: %s - VALID TIME: %s' % (forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/mslp_gh500' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-mslp-gh500-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_mslp.close()
    ds_gh.close()


def plot_gfs_t2m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for air temperature at 2m from GFS
    """
    ds_tmp = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/TMP/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

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

    plt.title('GFS %02dZ - AIR TEMPERATURE 2m\nFORECAST TIME: %s - VALID TIME: %s' % (cycle, forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/t2m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-t2m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_tmp.close()


def plot_gfs_rh2m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for relative humidity at 2m from GFS
    """
    ds_rh = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/RH/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

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

    plt.title('GFS 00Z - RELATIVE HUMIDITY 2m\nFORECAST TIME: %s - VALID TIME: %s' % (forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/rh2m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-rh2m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()


def plot_gfs_precipitation(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for total precipitation at surface from GFS
    """
    ds_tp = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/APCP/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

    lons = ds_tp.longitude.values
    lats = ds_tp.latitude.values

    llon = AOIS[area]['llon']
    ulon = AOIS[area]['ulon']
    llat = AOIS[area]['llat']
    ulat = AOIS[area]['ulat']

    if (t-1) % 6 == 0 or t == 1 or t >= 120:
        values = ds_tp.tp.values
    else:
        ds_tp_previous = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/APCP/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t-1))
        values = ds_tp.tp.values - ds_tp_previous.tp.values
        ds_tp_previous.close()
    
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

    plt.title('GFS 00Z - TOTAL PRECIPITATION\nFORECAST TIME: %s - VALID TIME: %s' % (forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/prec' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-prec-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_tp.close()


def plot_gfs_wind10m(area, cycle, t, data_dir, images_dir):
    """
    Generate figures for wind at 10m
    """
    ds_ugrd = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/UGRD/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))
    ds_vgrd = cfgrib.open_dataset('%s/NWP_GFS_0p25_1hr/%02d/%s/latest/VGRD/gfs.t%02dz.pgrb2.0p25.f%03d' % (data_dir, cycle, area, cycle, t))

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

    plt.title('GFS 00Z - WIND\nFORECAST TIME: %s - VALID TIME: %s' % (forecast_str, valid_str))

    output_folder = '%s/NWP_GFS_0p25_1hr/%02d/%s/%s/wind10m' % (images_dir, cycle, area, forecast_ts.strftime('%Y%m%d'))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepath = '%s/gfs-wind_10m-%03d.png' % (output_folder, t)
    plt.savefig(filepath)
    plt.close()

    ds_ugrd.close()
    ds_vgrd.close()


def plot_gfs(cycle, area, data_dir, images_dir):
    TIMESTEPS = list([i for i in range(0, 121)])
    TIMESTEPS.extend([i for i in range(120, 241, 3)])
    TIMESTEPS.extend([i for i in range(240, 384, 12)])

    for t in TIMESTEPS:
        plot_gfs_mslp_gh500mb(area, cycle, t, data_dir, images_dir)
        plot_gfs_1000_500mb_thickness(area, cycle, t, data_dir, images_dir)
        plot_gfs_t2m(area, cycle, t, data_dir, images_dir)
        plot_gfs_rh2m(area, cycle, t, data_dir, images_dir)
        if t > 0:
            plot_gfs_precipitation(area, cycle, t, data_dir, images_dir)
        plot_gfs_wind10m(area, cycle, t, data_dir, images_dir)

