import re
import datetime
import time
import glob, os, shutil
import subprocess

file_name = "run.bat"

input_file = "CMEMS_DOWNLOAD.dat"

#url="http://nrtcmems.mercator-ocean.fr/motu-web/Motu"
#product="GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS"
#dataset="global-analysis-forecast-phy-001-024"
#####################################################
def read_date():
	global initial_date
	global end_date
	global number_of_runs
	
	with open(input_file) as file:
		for line in file:
			if re.search("^START.+:", line):
				words = line.split()
				initial_date = datetime.datetime(int(words[2]),int(words[3]),int(words[4]),int(words[5]),int(words[6]),int(words[7]))
			elif re.search("^END.+:", line):
				words = line.split()
				end_date = datetime.datetime(int(words[2]),int(words[3]),int(words[4]),int(words[5]),int(words[6]),int(words[7]))
					
	interval = end_date - initial_date
	
	number_of_runs = interval.days
	
#####################################################
def read_keyword_value(keyword_name): 
	with open(input_file) as file:
		for line in file:
			if re.search("^"+keyword_name+".+: ", line):
				words = line.split()
				#value = int(words[2])
				value = words[2]
				return value
#####################################################
def download_file():

	#Take also the previous day for running Mohid
	#start_date = next_start_date - datetime.timedelta(days = 1)
	start_date = next_start_date

	os.system("python -m motuclient --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS --product-id global-analysis-forecast-phy-001-024 --longitude-min " +
	lon_min + " --longitude-max " + lon_max + " --latitude-min " + lat_min + " --latitude-max " + lat_max + " --date-min " + '"' + str(start_date.strftime("%Y-%m-%d"))+" 12:00:00"+'"'+ 
	" --date-max " + '"'+str(next_end_date.strftime("%Y-%m-%d"))+" 12:00:00"+'"'+ " --depth-min " + start_depth + " --depth-max " + end_depth + " --variable thetao --variable so --variable zos --variable uo --variable vo --out-dir " + 
	output_directory + " --out-name " + output_file_name + ".nc --user " + user + " --pwd " + password)
#####################################################
def next_date (run):
	global next_start_date
	global next_end_date
	global old_start_date
	global old_end_date
		
	next_start_date = initial_date + datetime.timedelta(days = run)
	next_end_date = initial_date + datetime.timedelta(days = run+1)

#####################################################
#Read main keywords 

keyword_name = ("your_user","your_password", "lon_min",
				"lon_max","lat_min","lat_max","start_depth","end_depth","your_output_directory","your_output_file_name")

number_of_keywords = len(keyword_name)

keyword_value = [0]*number_of_keywords
for n in range (0,number_of_keywords):
	keyword_value[n] = read_keyword_value(keyword_name[n])

user = keyword_value[0]
password = keyword_value[1]
lon_min = keyword_value[2]
lon_max = keyword_value[3]
lat_min = keyword_value[4]
lat_max = keyword_value[5]
start_depth = keyword_value[6]
end_depth = keyword_value[7]
output_directory = keyword_value[8]
output_file_name = keyword_value[9]

read_date()

######################################################

for run in range (0,number_of_runs):	
	
	#Update dates
	next_date (run)
	
	download_file()
	
	#output = subprocess.call([file_name])