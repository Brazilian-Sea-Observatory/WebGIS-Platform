#ProductsForecast
variables = {
	'surface_height_forecast_daily':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS',
			'product_id':'global-analysis-forecast-phy-001-024',
			'interval_period':'9',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'zos'
		},
		'file':{
			'outputDir':'surface_height_forecast_daily',
			'fileNameSufix':'surface_height_forecast_daily',
			'daysToDeleSymbLinks':'3'
		}
	},
	'temperature_forecast_daily':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS',
			'product_id':'global-analysis-forecast-phy-001-024',
			'interval_period':'9',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'thetao'
		},
		'file':{
			'outputDir':'temperature_forecast_daily',
			'fileNameSufix':'temperature_forecast_daily',
			'daysToDeleSymbLinks':'3'
		}
	},
	'salinity_forecast_daily':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS',
			'product_id':'global-analysis-forecast-phy-001-024',
			'interval_period':'9',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'so'
		},
		'file':{
			'outputDir':'salinity_forecast_daily',
			'fileNameSufix':'salinity_forecast_daily',
			'daysToDeleSymbLinks':'3'
		}
	},
	'vector_speed_forecast_daily':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS',
			'product_id':'global-analysis-forecast-phy-001-024',
			'interval_period':'9',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'uo --variable vo'
		},
		'file':{
			'outputDir':'vector_speed_forecast_daily',
			'fileNameSufix':'vector_speed_forecast_daily',
			'daysToDeleSymbLinks':'3'
		}
	},


	'oxygen_concentration':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS',
			'product_id':'global-analysis-forecast-bio-001-028-daily',
			'interval_period':'5',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'o2'
		},
		'file':{
			'outputDir':'oxygen_concentration',
			'fileNameSufix':'oxygen_concentration',
			'daysToDeleSymbLinks':'60'
		}
	},
	'nitrate_concentration':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS',
			'product_id':'global-analysis-forecast-bio-001-028-daily',
			'interval_period':'5',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'no3'
		},
		'file':{
			'outputDir':'nitrate_concentration',
			'fileNameSufix':'nitrate_concentration',
			'daysToDeleSymbLinks':'3'
		}
	},
	'phosphate_concentration':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS',
			'product_id':'global-analysis-forecast-bio-001-028-daily',
		    'interval_period':'5',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'po4'
		},
		'file':{
			'outputDir':'phosphate_concentration',
			'fileNameSufix':'phosphate_concentration',
			'daysToDeleSymbLinks':'3'
		}
	},
	'silicate_concentration':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS',
			'product_id':'global-analysis-forecast-bio-001-028-daily',
			'interval_period':'5',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'si'
		},
		'file':{
			'outputDir':'silicate_concentration',
			'fileNameSufix':'silicate_concentration',
			'daysToDeleSymbLinks':'3'
		}
	},
	'chlorophyll_concentration':{
		'parameters':{
			'service_id':'GLOBAL_ANALYSIS_FORECAST_BIO_001_028-TDS',
			'product_id':'global-analysis-forecast-bio-001-028-daily',
			'interval_period':'5',
			'unit':'days',
			'time':'forward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'chl'
		},
		'file':{
			'outputDir':'chlorophyll_concentration',
			'fileNameSufix':'chlorophyll_concentration',
			'daysToDeleSymbLinks':'3'
		}
	},
	'surface_height_observation_daily':{
		'parameters':{
			'service_id':'OCEANCOLOUR_GLO_OPTICS_L3_REP_OBSERVATIONS_009_086-TDS',
			'product_id':'dataset-oc-glo-opt-multi-l3-zsd_4km_daily-rep-v02',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'',
			'variable':'ZSD'
		},
		'file':{
			'outputDir':'surface_height_observation_daily',
			'fileNameSufix':'surface_height_observation_daily',
			'daysToDeleSymbLinks':'3'
		}
	},

# python -m motuclient --motu http://my.cmems-du.eu/motu-web/Motu 
# --service-id OCEANCOLOUR_GLO_OPTICS_L3_REP_OBSERVATIONS_009_086-TDS 
# --product-id dataset-oc-glo-opt-multi-l3-zsd_4km_daily-rep-v02 
# --longitude-min -179.9791717529297 --longitude-max 179.9791717529297 
# --latitude-min -89.97917175292969 --latitude-max 89.97916412353516 --date-min "2018-06-26 00:00:00" 
# --date-max "2018-06-30 00:00:00" --variable ZSD --out-dir <OUTPUT_DIRECTORY> 
# --out-name <OUTPUT_FILENAME> --user <USERNAME> --pwd <PASSWORD>

	'temperature_observation_daily':{
		'parameters':{
			'service_id':'SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001-TDS',
			'product_id':'METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'analysed_sst'
		},
		'file':{
			'outputDir':'temperature_observation_daily',
			'fileNameSufix':'temperature_observation_daily',
			'daysToDeleSymbLinks':'3'
		}
	},	
	'chlorophyll_observation_daily':{
		'parameters':{
			'service_id':'OCEANCOLOUR_GLO_CHL_L4_NRT_OBSERVATIONS_009_033-TDS',
			'product_id':'dataset-oc-glo-bio-multi-l4-chl_interpolated_4km_daily-rt',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'CHL'
		},
		'file':{
			'outputDir':'chlorophyll_observation_daily',
			'fileNameSufix':'chlorophyll_observation_daily',
			'daysToDeleSymbLinks':'3'
		}
	},
        'mass_concentration_of_suspended_matter_in_sea_water':{
		'parameters':{
			'service_id':'OCEANCOLOUR_GLO_OPTICS_L3_NRT_OBSERVATIONS_009_030-TDS',
			'product_id':'dataset-oc-glo-opt-multi-l3-spm_4km_daily-rt-v02',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'--depth-min 0.493 --depth-max 0.4942',
			'variable':'SPM'
		},
		'file':{
			'outputDir':'mass_concentration_of_suspended_matter_in_sea_water',
			'fileNameSufix':'mass_concentration_of_suspended_matter_in_sea_water',
			'daysToDeleSymbLinks':'3'
		}
	},
	'temperature_insitu_daily':{
		'parameters':{
			# 'service_id':'INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST',
			'service_id':'INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST',
			'product_id':'',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'',
			'variable':'sea_water_temperature'
		},
		'file':{
			'outputDir':'temperature_insitu_daily',
			'fileNameSufix':'temperature_insitu_daily',
			'daysToDeleSymbLinks':'3'
		}
	},
	'salinity_insitu_daily':{
		'parameters':{
			# 'service_id':'INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST',
			'service_id':'INS-CORIOLIS-GLO-NRT-OBS_POINTSERIES_LATEST',
			'product_id':'',
			'interval_period':'7',
			'unit':'days',
			'time':'backward',
			'aditional_params':'',
			'variable':'sea_water_temperature'
		},
		'file':{
			'outputDir':'salinity_insitu_daily',
			'fileNameSufix':'salinity_insitu_daily',
			'daysToDeleSymbLinks':'3'
		}
	},

}



# python <PATH_TO_SOSCLIENT_DIR>/sos_client.py --user=<USERNAME> --pwd=<PASSWORD> --quiet --server=http://nrt.cmems-du.eu/oceanotron/SOS/default --offering-id=INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST --longitude-min=-179.99942 --longitude-max=179.98204 --latitude-min=-78.01 --latitude-max=81.991 --date-min="2019-06-16T12:00:00.000Z" --date-max="2019-06-22T12:00:00.000Z" --observed-property=sea_water_temperature --out-dir=<OUTPUT_DIRECTORY> --out-name=<OUTPUT_FILENAME>






