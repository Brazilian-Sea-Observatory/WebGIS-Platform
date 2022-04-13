#!/bin/sh
 
#echo source activate moodsenv
#source activate moodsenv

#programDir="/opt/scripts/mercator_scripts"
#programDir="$(cd "$(dirname "$0")" && pwd)"
#programDir="/Users/lucashenning/Documents/Projetos/Mercator/mercator_routine_products"
echo "Date/Time on Machine " 
date '+%A %W %Y %X'

programDir="/home/geoserver/mercator_routine_products"

# outputDir="/home/maretec/mercator/geoserver_data"
outputDir="/home/geoserver/geoserver_data"

# pythonExecutable="/opt/anaconda3/bin/python"
pythonExecutable="python3"

#########################################CREATE PHYSICAL VARIABLES


function physical(){
    array_phy=(surface_height_forecast_daily
        temperature_forecast_daily
        salinity_forecast_daily
        vector_speed_forecast_daily) 


    echo "\nPhysical Variables"
    #echo "\nArray size: ${#array_phy[*]\n\n}"

    for item in ${!array_phy[*]}
    do
        printf "%d\n" $item
        executeScript= ${pythonExecutable} ${programDir}/downloadProducts.py  ${array_phy[$item]} ${outputDir}
        printf "   %s\n" ${executeScript}
    done
}


#########################################EXECUTE BIOQUIMICAL VARIABLES
function bioquimical(){
    array_bio=(oxygen_concentration
    nitrate_concentration 
    phosphate_concentration
    silicate_concentration
    chlorophyll_concentration
    ) 


    echo "\nBioquimical Variables"
    #echo "\nArray size: ${#array_bio[*]\n\n}"

    for item in ${!array_bio[*]}
    do
        printf "%d\n" $item
        executeScript= ${pythonExecutable} ${programDir}/downloadProducts.py  ${array_bio[$item]} ${outputDir}
        printf "   %s\n" ${executeScript}
    done


}

#########################################EXECUTE INSITU VARIABLE
function observationAndInsitu(){
    array_observation=(
        # salinity_insitu_daily
        # temperature_insitu_daily
        temperature_observation_daily
        chlorophyll_observation_daily
    	mass_concentration_of_suspended_matter_in_sea_water
    ) 

    echo "\Observation and Insitu Variables"
    #echo "\nArray size: ${#array_bio[*]\n\n}"

    for item in ${!array_observation[*]}
    do
        printf "%d\n" $item
        executeScript= ${pythonExecutable} ${programDir}/downloadProducts.py  ${array_observation[$item]} ${outputDir}
        printf "   %s\n" ${executeScript}
    done

}


#########################################UPDATE REGIONAL MODELS
function updateSymbLinkOfRegionalModels(){
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
}


#########################################EXECUTE TO RELOAD CATALOGS
function reloadCatalogGeoserver(){

    #curlExecuteReset="curl -u admin:WsZdjHAjY9so -v -XPOST http://geoserver:8080/geoserver/rest/reset"
    #${curlExecuteReset}

    #curlExecuteReload="curl -u admin:WsZdjHAjY9so -v -XPOST http://geoserver:8080/geoserver/rest/reload"
    #${curlExecute}
    
    updateStores=${pythonExecutable} ${programDir}/gs_store.py
    printf "   %s\n" ${updateStores}

}


############### General
updateSymbLinkOfRegionalModels
observationAndInsitu
bioquimical
physical
reloadCatalogGeoserver


