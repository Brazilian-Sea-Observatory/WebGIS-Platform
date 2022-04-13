#!/bin/bash
pyversion="python3"
pyscript="/home/maretec/mercator/mercator_routine_products/downloadProducts.py"
outputdir="/home/geoserver/geoserver_data"
messagedir="/home/maretec/mercator/mercator_routine_products/logs"
errologdir="/home/maretec"
echo "download_surface_height_forecast_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} surface_height_forecast_daily ${outputdir} > ${messagedir}/download_surface_height_forecast_daily.log 2> ${errologdir}/errors_mercator_download_surface_height_forecast_daily.log;
echo "download_temperature_forecast_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} temperature_forecast_daily ${outputdir} > ${messagedir}/download_temperature_forecast_daily.log 2> ${errologdir}/errors_mercator_download_temperature_forecast_daily.log;
echo "download_salinity_forecast_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} salinity_forecast_daily ${outputdir} > ${messagedir}/download_salinity_forecast_daily.log 2> ${errologdir}/errors_mercator_download_salinity_forecast_daily.log;
echo "download_vector_speed_forecast_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} vector_speed_forecast_daily ${outputdir} > ${messagedir}/download_vector_speed_forecast_daily.log 2> ${errologdir}/errors_mercator_download_vector_speed_forecast_daily.log;
echo "download_oxygen_concentration " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} oxygen_concentration ${outputdir} > ${messagedir}/download_oxygen_concentration.log 2> ${errologdir}/errors_mercator_download_oxygen_concentration.log;
echo "download_nitrate_concentration " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} nitrate_concentration ${outputdir} > ${messagedir}/download_nitrate_concentration.log 2> ${errologdir}/errors_mercator_download_nitrate_concentration.log;
echo "download_phosphate_concentration " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} phosphate_concentration ${outputdir} > ${messagedir}/download_phosphate_concentration.log 2> ${errologdir}/errors_mercator_download_phosphate_concentration.log;
echo "download_silicate_concentration " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} silicate_concentration ${outputdir} > ${messagedir}/download_silicate_concentration.log 2> ${errologdir}/errors_mercator_download_silicate_concentration.log;
echo "download_chlorophyll_concentration " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} chlorophyll_concentration ${outputdir} > ${messagedir}/download_chlorophyll_concentration.log 2> ${errologdir}/errors_mercator_download_chlorophyll_concentration.log;
echo "download_temperature_observation_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} temperature_observation_daily ${outputdir} > ${messagedir}/download_temperature_observation_daily.log 2> ${errologdir}/errors_mercator_download_temperature_observation_daily.log;
echo "download_chlorophyll_observation_daily " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} chlorophyll_observation_daily ${outputdir} > ${messagedir}/download_chlorophyll_observation_daily.log 2> ${errologdir}/errors_mercator_download_chlorophyll_observation_daily.log;
echo "download_mass_concentration_of_suspended_matter_in_sea_water " && date '+%A %d/%m/%Y %T' &&
${pyversion} ${pyscript} mass_concentration_of_suspended_matter_in_sea_water ${outputdir} > ${messagedir}/download_mass_concentration_of_suspended_matter_in_sea_water.log 2> ${errologdir}/errors_mercator_download_mass_concentration_of_suspended_matter_in_sea_water.log;

