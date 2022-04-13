
import sys
import os
import io
import errno

import xarray as xr
from importlib.machinery import SourceFileLoader


#Operational Params
# DIR_ORIGIN="/home/evx/ftp/files/Plataforma_SE" 

# DIR_DESTINY="/home/geoserver/geoserver_data/mercator_products"

# DIR_DESTINY_NAME="last_regional_models"


## Local Test Params

# DIR_ORIGIN="/opt/test_dir"

# DIR_DESTINY="/opt"

# DIR_DESTINY_NAME="last_regional_models"

# Inside dirs

 # /DIR_DESTINY_HYDRO_SURFACE="hydrodinamic"

# DIR_DESTINY_WP_SURFACE="water_properties"

## File Models

# FILE_HYDRODYNAMIC_SURFACE_NAME="Hydrodynamic_2_Surface.hdf5.nc"

# FILE_WATER_PROPERTIES_SURFACE_NAME="WaterProperties_2_Surface.hdf5.nc"

# NUMBER_OF_FILES_TO_MERGE = 5

## Actual Dir

##DirScript
DIR = os.path.dirname(os.path.realpath(__file__))

NUMBER_OF_SYMB_LINKS = '1' 

## TODO: Remove the intermediate files with Hour->00:00, the hour is repeated
#                Make the generate of files more modular, read of dictionary            

class routineGeneral():

        def __init__(self):


                ##VariablesTo Load
                #Read Product Param
                self.productParam = sys.argv[1]
                print('############################################# ' + self.productParam)             

                #Import External Dicitonary
                dictionaryLocate = DIR + '/' + 'dictionaryProductsRegionalModels.py'
                self.updateSymbolicLinksScript = DIR + '/' + 'updateSymbLinks.sh'


                dictionary = SourceFileLoader("variables_model", dictionaryLocate).load_module()
                self.dictionaryProduct = dictionary.variables_model[self.productParam]


                ##Load model dir informations
                self.dir_origin = self.dictionaryProduct['model_dirs']['dir_origin'] 
                self.dir_destiny = self.dictionaryProduct['model_dirs']['dir_destiny']
                self.dir_destiny_name = self.dictionaryProduct['model_dirs']['dir_destiny_name']


                ##Load model info
                self.dir_destiny_model = self.dictionaryProduct['model_info']['model_destiny_dir'] 
                self.file_model_name = self.dictionaryProduct['model_info']['file_name'] 
                self.prefix_file_name = self.dictionaryProduct['model_info']['prefix'] 
                self.number_of_files_to_merge= self.dictionaryProduct['model_info']['number_files_to_merge'] 


                ##Variable to share info of folders
                self.foldersFinded = []
                # self.files_of_hydronynamic = []
                # self.files_of_water_properties = []
                self.files_of_model = []
                self.destiny_name_file = ""


                ##Functions that will be called
                self.findDirOfModels()

                self.mergeModelFinded()

                self.mergeAndSaveFiles()

                self.updateSymbolicLinks()


        def findDirOfModels(self):
                # folders = []
                # r=root, d=directories, f = files
                
                for r, d ,f in os.walk(self.dir_origin):
                        for folder in sorted(d):
                                self.foldersFinded.append(os.path.join(r, folder))

                #print(folders)
                sizeVector = len(self.foldersFinded)
                print("Find " + str(sizeVector) + " directories on " + self.dir_origin)

        
                #Slice the last X files
                last_files = int(self.number_of_files_to_merge) * -1
                self.foldersFinded = self.foldersFinded[last_files - 3:]

                #Print dir finded
                for r in self.foldersFinded:
                        print(r)


                #Save the name files
                first_name_data = self.foldersFinded[0]
                first_name_data = first_name_data.replace(self.dir_origin + "/","")
                self.destiny_name_file = first_name_data[0:8]
                # print(first_name_data)

                last_index = len(self.foldersFinded)
                last_name_data = self.foldersFinded[last_index -1]
                last_name_data = last_name_data.replace(self.dir_origin + "/","")
                self.destiny_name_file = self.destiny_name_file + "_" + last_name_data[9:]

                # print(last_name_data)
                

                print("\nCreated Destiny Name File: " + self.destiny_name_file)
                                
        def mergeModelFinded(self):

                #Check if files exists, and put in array of files that will be merge
                for d in self.foldersFinded:
                        model = d + "/" + self.file_model_name
                
                        if(os.path.isfile(model)):
                                self.files_of_model.append(model)


                print("\nFiles of Water Properties Files That Will Be Merge:\n", self.files_of_model)           
                # print("\n\nFiles of Hydronamic With Merge Files:\n", self.files_of_hydronynamic)


        def mergeAndSaveFiles(self):
                #Exemple of How to Merge Files
                
                #ncrcat -h /opt/mercator_model_products/20190519_20190520/WaterProperties_2_Surface.hdf5.nc 
                #/opt/mercator_model_products/20190520_20190521/WaterProperties_2_Surface.hdf5.nc 
                #/opt/mercator_model_products/20190520_20190521/WaterProperties_2_Surface.hdf5.nc total.nc

                destineFolder  = self.dir_destiny + "/" + self.dir_destiny_name
                if not (os.path.isdir(destineFolder)):
                        try:
                                print("Create destiny folder " + destineFolder)
                                os.mkdir(destineFolder)
                                os.mkdir(destineFolder + "/" + self.dir_destiny_model)
                                # os.mkdir(destineFolder + "/" + DIR_DESTINY_WP_SURFACE)
                        except:
                                print("Cant create destiny folder at " + destineFolder)

                savedir = self.dir_destiny + "/" + self.dir_destiny_name  

                #Save the WP_Model on File
                print("\n##########->WARNINGs")
                dataset_wp = xr.open_mfdataset(self.files_of_model)
                print("#################")

                file_name_save = savedir + "/"+ self.dir_destiny_model + "/" + self.destiny_name_file + "_" + self.file_model_name
                print("\nSave name of merge file: " + file_name_save)
                dataset_wp.to_netcdf(file_name_save)


                # #Save the Hydro_Model on File
                # print("\n##########->WARNINGs")
                # dataset_hydro = xr.open_mfdataset(self.files_of_hydronynamic)
                # print("#################")

                # file_name_save = savedir + "/" + DIR_DESTINY_WP_SURFACE + "/" + self.destiny_name_file + "_" + FILE_WATER_PROPERTIES_SURFACE_NAME
                # print("\nSave name of merge file: " + file_name_save)
                # dataset_hydro.to_netcdf(file_name_save)

        def updateSymbolicLinks(self):

                outputDirModel = self.dir_destiny + "/" + self.dir_destiny_name + "/" + self.dir_destiny_model

                # outputDirWP = self.dir_destiny + "/" + self.dir_destiny_name + "/" + DIR_DESTINY_WP_SURFACE

                ##${programDir}/AtualizaLinksSimbolicos.sh ${outputDir}/satelite_parana/ jpg jpeg satelite_parana 7 1
                scriptDirModel = self.updateSymbolicLinksScript + ' '  + outputDirModel + '/' + ' nc nc ' + self.prefix_file_name + ' '  +  NUMBER_OF_SYMB_LINKS + '  10' 
                # scriptDirWP = self.updateSymbolicLinksScript + ' '  + outputDirWP + '/' + ' nc nc ' +  'latest_wp_model'  +  ' ' + NUMBER_OF_SYMB_LINKS + '  10' 

                print('\n##Update Symbolic Links at \n' + scriptDirModel)       
                os.system(scriptDirModel)
                
        
                # print('\n##Update Symbolic Links DirWaterProperties \n' + scriptDirWP)        
                # os.system(scriptDirWP)
                

if __name__ == "__main__":
        classMain= routineGeneral()

