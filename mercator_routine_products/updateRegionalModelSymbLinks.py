
import sys
import os
import io
import errno


##Operational Params
# DIR_ORIGIN="/home/evx/ftp/files/Plataforma_SE/" 

# DIR_DESTINY="/home/geoserver/geoserver_data/mercator_products/regional_models"

# DIR_DESTINY_NAME="last_regional_models"


## Local Test Params

# DIR_ORIGIN="/opt/test_dir"

# DIR_DESTINY="/opt/test_dir"

# DIR_DESTINY_NAME="last_regional_models"

## File Models

# FILE_HYDRODYNAMIC_SURFACE_NAME="Hydrodynamic_2_Surface.hdf5.nc"

# FILE_WATER_PROPERTIES_SURFACE_NAME="WaterProperties_2_Surface.hdf5.nc"


class routineGeneral():

	def __init__(self):

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

		self.file_model_name = self.dictionaryProduct['model_info']['file_name'] 

		self.generateSymLinkFiles()


	def generateSymLinkFiles(self):
		folders = []
		# r=root, d=directories, f = files
		
		for r, d, f in os.walk(self.dir_origin):
			for folder in sorted(d):
				folders.append(os.path.join(r, folder))

		#print(folders)
		sizeVector = len(folders)

		destineFolder  = self.dir_destiny + "/" + self.dir_destiny_name 
		if(os.path.isdir(destineFolder)):
			os.remove(destineFolder)

		try:
			os.symlink(folders[sizeVector-1], destineFolder)
			print("Create destiny sucessful: " + destineFolder + " pointed to " + folders[sizeVector-1])
			
			file = destineFolder 	+ '/' + self.file_model_name
			# file_water = destineFolder 	+ '/' + FILE_WATER_PROPERTIES_SURFACE_NAME

			print("Models Found at " + file)  if(os.path.exists(file_hidro)) else print("Error Models Not Found.")
			# print("WaterProperties Model Found at " + file_water)  if(os.path.exists(file_water)) else print("Error: WaterProperties Not Found.")



		except OSError as e:
			os.remove(destineFolder)
			print("Error create destiny folder: " + destineFolder)
			print(e)



if __name__ == "__main__":
	classMain= routineGeneral()