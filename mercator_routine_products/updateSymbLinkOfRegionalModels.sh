#!/bin/bash

echo "Date/Time on Machine " 
date '+%A %W %Y %X'

# programDir="/home/geoserver/mercator_routine_products" Não existia na maretecVM
programDir="/home/maretec/mercator/mercator_routine_products"

# outputDir="/home/maretec/mercator/geoserver_data"
outputDir="/home/geoserver/geoserver_data"

# pythonExecutable="/opt/anaconda3/bin/python"
pythonExecutable="python3"
array_model=(
        platform_se_hydro_surface
        platform_se_wp_surface
        pr_sc_wp_surface
        pr_sc_hydro_surface
        cep_wp_surface
        cep_hydro_surface
        babitonga_wp_surface
        babitonga_hydro_surface
        # temperature_observation_daily
        # chlorophyll_observation_daily
) 


for item in ${!array_model[*]}
do
        printf "%d\n" $item
        executeScript= ${pythonExecutable} ${programDir}/mergeRegionalModelData.py  ${array_model[$item]} 
        # ${outputDir}
        printf "   %s\n" ${executeScript}
done
    # executeScript= ${pythonExecutable} ${programDir}/updateRegionalModelSymbLinks.py 
printf "   %s\n" ${executeScript}
