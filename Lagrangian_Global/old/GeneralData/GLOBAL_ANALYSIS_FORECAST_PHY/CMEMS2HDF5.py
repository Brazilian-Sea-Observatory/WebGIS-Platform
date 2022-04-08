import re
import datetime
import time
import glob, os, shutil
import subprocess

dirpath = os.getcwd()

input_file = "CMEMS2HDF5.dat"

download_dir = (dirpath+"/CMEMS_Download")
ConvertToHdf5_dir = (dirpath+"/ConvertToHdf5")

backup_path =  (dirpath+"/Backup")
#backup_path = (r"C:/Aplica/Lagrangian_Global/GeneralData/Solutions/CMEMS")
#####################################################
def read_date():
	global initial_date
	global end_date
	global number_of_runs
	
	forecast_mode = 0
	refday_to_start = 0
	number_of_runs = 0
	
	with open(input_file) as file:
		for line in file:
			if re.search("^FORECAST_MODE.+:", line):
				number = line.split()
				forecast_mode = int(number[2])
				
	if forecast_mode == 1:
		with open(input_file) as file:
			for line in file:
				if re.search("^REFDAY_TO_START.+:", line):
					number = line.split()
					refday_to_start = int(number[2])
				elif re.search("^NUMBER_OF_RUNS.+:", line):
					number = line.split()
					number_of_runs = int(number[2])
					
		initial_date = datetime.datetime.utcnow() + datetime.timedelta(days = refday_to_start)
		end_date = initial_date + datetime.timedelta(days = number_of_runs-1)
    						
	else:
		with open(input_file) as file:
			for line in file:
				if re.search("^START.+:", line):
					number = line.split()
					initial_date = datetime.datetime(int(number[2]),int(number[3]),int(number[4]),int(number[5]),int(number[6]),int(number[7]))
				elif re.search("^END.+:", line):
					number = line.split()
					end_date = datetime.datetime(int(number[2]),int(number[3]),int(number[4]),int(number[5]),int(number[6]),int(number[7]))
				
		interval = end_date - initial_date
		number_of_runs = interval.days	
#####################################################
def next_date (run):
	global next_start_date
	global next_end_date
		
	next_start_date = initial_date + datetime.timedelta(days = run)
	next_end_date = next_start_date + datetime.timedelta(days = 1)

#####################################################
def write_date(file_name):
		
	with open(file_name) as file:
		file_lines = file.readlines()
		
	number_of_lines = len(file_lines)
	
	for n in range(0,number_of_lines):
		line = file_lines[n]		
		if re.search("^START.+:", line):
			file_lines[n] = "START " + ": " + str(next_start_date.strftime("%Y %m %d %H %M %S")) + "/n"

		elif re.search("^END.+:", line):	
			file_lines[n] = "END " + ": " + str(next_end_date.strftime("%Y %m %d %H %M %S")) + "/n"
			
	with open(file_name,"w") as file:
		for n in range(0,number_of_lines) :
			file.write(file_lines[n])

#####################################################

read_date()

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	#Download
	os.chdir(download_dir)
	
	files = glob.glob("*.nc")
	for filename in files:
		os.remove(filename)
		
	file_name = "CMEMS_DOWNLOAD.DAT"
	write_date(file_name)	
	output = subprocess.call(["CMEMS_DOWNLOAD.bat"])
	
	nc_files = glob.iglob(os.path.join(download_dir,"*.nc"))
	for file in nc_files:
		shutil.copy(file, ConvertToHdf5_dir)
	
		
	#ConvertToHdf5
	os.chdir(ConvertToHdf5_dir)
	
	files = glob.glob("*.hdf*")
	for filename in files:
		os.remove(filename)
		
	output = subprocess.call(["ConvertToHdf5.bat"])
	
	#output_dir = backup_path+"//"+str(next_start_date.strftime("%Y"))+"//"+str(next_start_date.strftime("%m"))+"//"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d"))
	output_dir = backup_path+"//"+"//"+str(next_start_date.strftime("%Y%m%d")) + "_" + str(next_end_date.strftime("%Y%m%d"))
		
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	
	hdf_files = glob.iglob(os.path.join(ConvertToHdf5_dir,"*.hdf*"))
	for file in hdf_files:
		shutil.copy(file, output_dir)
	
	files = glob.glob("*.nc")
	for filename in files:
		os.remove(filename)
