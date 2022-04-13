#! /usr/bin/env python
# -*- coding: utf-8

#echo source activate moodsenv
#source activate moodsenv

from importlib.machinery import SourceFileLoader
import xarray as xr
import sys
import os
import urllib3 as urllib
import io
import json
import datetime, dateutil.tz
import time
import netCDF4 as nc
import numpy as np

##TODO Things
# 1- Create operational branch, with operational variables to put on Gitlab
# 2- Try to identify what is the most recent data available
# 3- Improove the names that will be saved the files

#PythonDDIR
#DIR_PYTHON = '/opt/anaconda3/bin/python'
DIR_PYTHON = 'python'

DIR_MOTU_CLIENT = 'motuclient-python'
DIR_SOS_CLIENT = 'sos-client-python'

##DirScript
DIR = os.path.dirname(os.path.realpath(__file__))

##OutputDir
OUTPUT_DIR = '/opt/mercator_products'
NUMBER_OF_SYMB_LINKS = '5'

#UserParams
#USER_COPERNICUS = 'fsato'
USER_COPERNICUS = 'hibanez'
#PWD_COPERNICUS = 'FabioCMEMS2018'
PWD_COPERNICUS = 'Bso_2022'


class routineGeneral():

        def __init__(self):

                #Print Dir of script 
                #print(DIR, '\n')

                #Read Product Param
                self.productParam = sys.argv[1]
                print('############################################# ' + self.productParam)

                #Import External Dicitonary
                dictionaryLocate = DIR + '/' + 'dictionaryProducts.py'
                self.updateSymbolicLinksScript = DIR + '/' + 'updateSymbLinks.sh'

                # self.generateImageScript = DIR + '/' + 'generateForecast.py'  
                # self.updateSymbolicLinksScript = DIR + '/' + 'AtualizaLinksSimbolicos.sh'

                dictionary = SourceFileLoader("variables", dictionaryLocate).load_module()
                self.dictionaryProducts = dictionary.variables

                # self.dictionaryProducts = dictionary.dictionaryForecast

                self.variablesDownload = self.dictionaryProducts[self.productParam]

                self.productID = self.variablesDownload['parameters']['product_id']
                self.serviceID = self.variablesDownload['parameters']['service_id']
                self.aditionalParams = self.variablesDownload['parameters']['aditional_params']
                self.variable = self.variablesDownload['parameters']['variable']

                ##Time variable
                self.intervalPeriod = int(self.variablesDownload['parameters']['interval_period'])
                self.unitTime = self.variablesDownload['parameters']['unit']
                self.time = self.variablesDownload['parameters']['time']

                ##Save parameters
                self.outputMatrixDir = sys.argv[2] + '/mercator_products'
                self.outputDir = self.outputMatrixDir  + '/' +  self.variablesDownload['file']['outputDir']

                date_name = datetime.datetime.now().strftime('%Y%m%d')
                self.outputName = date_name + '_1200_' + self.variablesDownload['file']['fileNameSufix']

                ##Parameters To Routine
                self.daysToDeleSymbLinks = self.dictionaryProducts[self.productParam]['file']['daysToDeleSymbLinks']

                self.generateAndUpdateProducts();

        def generateAndUpdateProducts(self):

                ##Check if the directory was created, if is not, create
                if not(self.createOutputDir()):
                        return

                ##Download Files
                if('insitu' in self.productParam):
                        self.downloadSelectedProductsSosClient()
                else:
                        self.downloadSelectedProductsMotuClient()

                ##Delete temp files that are created during the process
                # self.deleteTemporaryFiles()

                ##Update Symbolic Links (Are called in function of downloads) 
                # self.updateSymbolicLinks();


        def downloadSelectedProductsMotuClient(self):

                #python <PATH_TO_MOTUCLIENT_DIR>/motu-client.py --user <USERNAME> --pwd <PASSWORD> 
                #--motu http://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS 
                #--product-id global-analysis-forecast-phy-001-024 --longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90 

                #--date-min "2019-02-23 12:00:00" --date-max "2019-03-03 12:00:00" 
                #--depth-min 0.493 --depth-max 0.4942 --variable zos --out-dir <OUTPUT_DIR> --out-name <OUTPUT_FILENAME>

                self.calculateStartEndDate()

                self.tempOutputName = '.' + self.outputName

                programsLine = DIR_PYTHON + ' ' + DIR + '/' + DIR_MOTU_CLIENT + '/motuclient.py ' + '--user ' +  USER_COPERNICUS + ' --pwd ' + PWD_COPERNICUS
                variableLine = '--service-id ' + self.serviceID + ' --product-id ' + self.productID + ' --variable ' + self.variable
                dateLine = self.calculateStartEndDate()
                commonParametersLine = '--longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90 --motu http://nrt.cmems-du.eu/motu-web/Motu'
                downloadLine =  '--out-dir ' + self.outputDir  + ' --out-name ' + self.tempOutputName + '.nc'

                scriptExecute = programsLine + ' ' + variableLine + ' ' + dateLine + ' ' + self.aditionalParams + ' ' + commonParametersLine + ' ' + downloadLine

                print(scriptExecute + '\n\n')
                os.system(scriptExecute)

                self.calculateOffsetAndScale()

                self.updateSymbolicLinks()


        def     downloadSelectedProductsSosClient(self):

                ##Annotations

                #python <PATH_TO_SOSCLIENT_DIR>/sos_client.py --user=<USERNAME> --pwd=<PASSWORD> 
                #--quiet --server=http://nrt.cmems-du.eu/oceanotron/SOS/default


                #--offering-id=INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST 
                #--longitude-min=-179.99942 --longitude-max=179.98204 --latitude-min=-78.01 --latitude-max=81.991 
                #--date-min="2019-06-16T12:00:00.000Z" --date-max="2019-06-22T12:00:00.000Z" 
                #--observed-property=sea_water_temperature --out-dir=<OUTPUT_DIRECTORY> --out-name=<OUTPUT_FILENAME>

                #python3 /Users/lucashenning/Documents/Projetos/Mercator/mercator_routine_products/sos-client-python/src/python/sos_client.py --user=fsato --pwd=FabioCMEMS2018 
                # --quiet  --server=http://nrt.cmems-du.eu/oceanotron/SOS/default --offering-id=INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST --observed-property=sea_water_temperature 
                 # --date-min "2019-07-04 12:00" --date-max "2019-06-27 12:00"  --longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90 
                 # --out-dir /opt/mercator_products/temperature_insitu_daily --out-name 20190704_1200_temperature_insitu_daily.nc

                 #python3 /Users/lucashenning/Documents/Projetos/Mercator/mercator_routine_products/sos-client-python/src/python/sos_client.py --user=fsato --pwd=FabioCMEMS2018 --quiet --server=http://nrt.cmems-du.eu/oceanotron/SOS/default --offering-id=INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST  --longitude-min=-179.99942 --longitude-max=179.98204 --latitude-min=-78.01 --latitude-max=81.991  --date-min="2019-06-16T12:00:00.000Z" --date-max="2019-06-22T12:00:00.000Z"  --out-dir /opt/mercator_products/temperature_insitu_daily --out-name 20190704_1200_temperature_insitu_daily.nc

                self.calculateStartEndDate()

                programsLine = DIR_PYTHON + ' ' + DIR + '/' + DIR_SOS_CLIENT + '/src/python/sos_client.py ' + '--user=' +  USER_COPERNICUS + ' --pwd=' + PWD_COPERNICUS
                variableLine = '--quiet ' + ' --server=http://nrt.cmems-du.eu/oceanotron/SOS/default ' + '--offering-id=' + self.serviceID + ' --observed-property=' + self.variable + ' '
                # dateLine = self.calculateStartEndDate()
                dateLine = '--date-min "2019-07-04 12:00" --date-max "2019-06-27 12:00"'
                commonParametersLine = '--longitude-min -180 --longitude-max 179.9166717529297 --latitude-min -80 --latitude-max 90'
                downloadLine =  '--out-dir ' + self.outputDir  + ' --out-name ' + self.outputName + '.nc'
                scriptExecute = programsLine + ' ' + variableLine + ' ' + dateLine + ' ' + self.aditionalParams + ' ' + commonParametersLine + ' ' + downloadLine

                print(scriptExecute + '\n\n')
                os.system(scriptExecute)

                self.updateSymbolicLinks()


        def calculateOffsetAndScale(self):

                print("Applying offset and scal if was needed." + '\n')

                file_path = self.outputDir + '/' + self.tempOutputName + '.nc'
                final_path = self.outputDir + '/' + self.outputName + '.nc'

                #Read the temp file
                dataset = xr.open_dataset(file_path, mask_and_scale=True).load()

                coords = {}
                for dim in dataset.dims:
                    coords[dim] = dataset[dim]


                #TODO improve dictionaryProducts.py file to add vo and uo variables as vector in vector_speed_forecast_daily file to be generic
                if self.variablesDownload['file']['fileNameSufix'] != 'vector_speed_forecast_daily':
                    variable = dataset[self.variable].data
                    ds = xr.Dataset({self.variable: (dataset[self.variable].dims, variable, dataset[self.variable].attrs)}, coords=coords)

                else:
                    uo = dataset['uo'].data
                    vo = dataset['vo'].data

                    ds = xr.Dataset({'uo': (dataset['uo'].dims, uo, dataset['uo'].attrs), 'vo': (dataset['vo'].dims, vo, dataset['vo'].attrs), 'vm': (dataset['uo'].dims, np.sqrt((vo * vo) + (uo * uo)), dataset['uo'].attrs)}, coords=coords)

                for dim in dataset.dims:
                    ds[dim].attrs = dataset[dim].attrs

                ds.attrs = dataset.attrs

                ds.to_netcdf(final_path)

                #Delete the temp file
                print("Finish offset apply, delete temporary files, and save final" + '\n')
                path = 'rm ' + file_path
                os.system(path)

        def calculateStartEndDate(self):
                datetimeProduct = datetime.datetime.now()
                date_init = datetimeProduct

                #Calculate interval
                delta = datetime.timedelta(weeks=self.intervalPeriod)
                if(self.unitTime == 'week'):
                        delta = datetime.timedelta(weeks=self.intervalPeriod)
                elif(self.unitTime == 'days'):
                        delta = datetime.timedelta(days=self.intervalPeriod)

                #See if was backward or forward date
                date_final = datetimeProduct + delta
                if(self.time == 'forward'):
                        date_init = datetimeProduct - delta
                        date_final = datetimeProduct + delta
                else:
                        date_final = datetimeProduct - delta

                date_i = date_init.strftime('%Y-%m-%d 12:00')
                date_f = date_final.strftime('%Y-%m-%d 12:00')


                date_interval = '--date-min "' + date_i  + '" --date-max "' + date_f + '"'
                return date_interval


        def createOutputDir(self):
                # scriptDir = self.dictionaryProducts[self.productParam]['file']['outputDir'] 

                matrizDirectoryExists = os.path.isdir(self.outputMatrixDir)
                if not(matrizDirectoryExists):
                        # return directoryExists
                        print('\n\nCreate directory matriz in ' + self.outputMatrixDir)
                        os.mkdir(self.outputMatrixDir)


                directoryExists = os.path.isdir(self.outputDir)
                if not (directoryExists):
                        print('\nCreate new directory in ' + self.outputDir)
                        # createFolder = 'mkdir ' + scriptDir
                        os.mkdir(self.outputDir)

                return True;


        # def deleteTemporaryFiles(self):
        #       print('\n\nDelete temp files:\n')
        #       #Need to force, cause temporary files are crete with ROOT dir

        #       path = 'rm -rf ' + self.outputDir + '/.*'
        #       os.system(path)


        def updateSymbolicLinks(self):

                ##${programDir}/AtualizaLinksSimbolicos.sh ${outputDir}/satelite_parana/ jpg jpeg satelite_parana 7 1
                scriptDir = self.updateSymbolicLinksScript + ' '  + self.outputDir + '/' + ' nc nc ' + self.productParam + ' '  +  NUMBER_OF_SYMB_LINKS + ' ' + self.daysToDeleSymbLinks
                os.system(scriptDir)
                print('\n##Update Symbolic Links \n' + scriptDir)


if __name__ == "__main__":
        classMain= routineGeneral()

