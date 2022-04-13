
# SOS Client Python Project

NAME
====

  ./sos-client.py 

The SOS python client. You must use python version 2.7.X or later.
This program is not compatible with Python 3.X versions.

VERSION
=======

This documentation is intended to describe the 0.0.1 version or higher of the SOS python client.

SYNOPSIS
========

The purpose of this client is to provide a description of the products and allow user to subset and download data of an SOS server.


CONFIGURATION FILE
==================

The program parameters are contained in an ini file. This file is located in the following directory:

   - on Unix platforms: $HOME/sos-client/sos-client-python.ini
   - on Windows platforms: %USERPROFILE%\sos-client/sos-client-python.ini
   
If you do not provide this configuration file, you will have to specify configuration items directly in command line arguments. Please also be aware that any command line given option will OVERWRITE options in configuration file.

The expected structure of file for a cas-protected SOS service is:

	[Main]
	user=john
	pwd=secret
	log_level=10
	auth_mode=cas
	server=http://visi-oceanotronw-tomcat:8080/oceanotron/SOS/default
	offering_id=CORIOLIS-RECOPESCA
	date_min=2017-12-27T12:28:01.000
	date_max=2017-12-28T12:28:01.000
	latitude_min=16.10438
	latitude_max=62.3397
	longitude_min=-61.55259
	longitude_max=7.16829
	observed_property=sea_water_temperature
	out_dir=./out_dir
	out_name=test.nc
	procedure=CORIOLIS-RECOPESCA__EXRE0231
	socket_timeout=60.0
	
The expected structure for a not cas-protected SOS service :

	[Main]
	log_level=10
	auth_mode=none
	server=http://visi-oceanotronw-tomcat:8080/oceanotron/SOS/default
	offering_id=CORIOLIS-RECOPESCA
	date_min=2017-12-27T12:28:01.000
	date_max=2017-12-28T12:28:01.000
	latitude_min=16.10438
	latitude_max=62.3397
	longitude_min=-61.55259
	longitude_max=7.16829
	observed_property=sea_water_temperature
	out_dir=./out_dir
	out_name=test.nc
	procedure=CORIOLIS-RECOPESCA__EXRE0231
	socket_timeout=60.0
	
BUILD
============
From the root folder runs the Maven command:
mvn clean install -Dmaven.test.skip=true

[...]
[INFO] BUILD SUCCESS
[...]

This creates two archives in the target folder:

	 sos-client-python-$version-$buildTimestamp-src.tar.gz: Archive containing all the source code
	 sos-client-python-$version-$buildTimestamp-bin.tar.gz: Archive ready to be installed


INSTALLATION
============

Deploy the archive "ready to be installed" in the directory of your choice. Create a configuration file (see "CONFIGURATION FILE") to inform the user and password to use to connect to the CAS server.
If there is no authentification (auth=none), make sure to delete "user" and "pwd" lines in your configuration file (if any).

Installing Python modules which are not provided in the standard installation of Python. The list of modules to be installed is described in section "REQUIRED MODULES".


USAGE
=====

Usage: ./sos-client.py -h

Usage: sos-client.py [options]

	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -q, --quiet           prevent any output in stdout
	  --verbose             print information in stdout
	  --noisy               print more information (traces) in stdout
	  -u USER, --user=USER  the user name (string)
	  -p PWD, --pwd=PWD     the user password (string)
	  --auth-mode=AUTH_MODE
	                        the authentication mode: 'none' (for no
	                        authentication) or 'cas' (for Central Authentication
	                        Service) [default: cas]
	  -s SERVER, --server=SERVER
	                        the sos server to use (url)
	  -d OFFERING_ID, --offering-id=OFFERING_ID
	                        The offering (dataset) to subset and download (string)
	  -b OBSERVED_PROPERTY, --observed-property=OBSERVED_PROPERTY
	                        The observed property (string)
	  -r PROCEDURE, --procedure=PROCEDURE
	                        The procedure id requested (string)
	  -t DATE_MIN, --date-min=DATE_MIN
	                        The min date (string following format YYYY-MM-
	                        DDTHH:MM:SS.sssZ)
	  -T DATE_MAX, --date-max=DATE_MAX
	                        The max date (string following format YYYY-MM-
	                        DDTHH:MM:SS.sssZ)
	  -y LATITUDE_MIN, --latitude-min=LATITUDE_MIN
	                        The min latitude (float in the interval [-90 ; 90])
	  -Y LATITUDE_MAX, --latitude-max=LATITUDE_MAX
	                        The max latitude (float in the interval [-90 ; 90])
	  -x LONGITUDE_MIN, --longitude-min=LONGITUDE_MIN
	                        The min longitude (float in the interval [-180 ; 180])
	  -X LONGITUDE_MAX, --longitude-max=LONGITUDE_MAX
	                        The max longitude (float in the interval [-180 ; 180])
	  -S, --sync-mode       Only for download requests, sets the download mode to
	                        synchronous
	  -D, --describeSensor  Discover list of procedures provided by a dataset.
	                        Output is in XML format
	  --capabilities        Discover the capabilities (offering, observed
	                        properties, procedure) provided by the service
	  -o OUT_DIR, --out-dir=OUT_DIR
	                        The output dir where result (download file) is written
	                        (string). If it starts with 'console', behaviour is
	                        the same as with --console-mode.
	  -f OUT_NAME, --out-name=OUT_NAME
	                        The output file name (string)
	  --socket-timeout=SOCKET_TIMEOUT
	                        Set a timeout on blocking socket operations (float
	                        expressing seconds)
	  --user-agent=USER_AGENT
	                        Set the identification string (user-agent) for HTTP
	                        requests. By default this value is 'Python-urllib/x.x'
	                        (where x.x is the version of the python interpreter)
	  --outputWritten=OUTPUTWRITTEN
	                        Optional parameter used to set the format of the file
	                        returned by the download request: netcdf, json or xml.
	                        If not set, netcdf is used.
	  --console-mode        Optional parameter used to display result on stdout,
	                        either URL path to download extraction file, or the
	                        XML content of getCapabilities or describeSensor
	                        requests (not recommended for netcdf download).

USAGE EXAMPLES
================
==DOWNLOAD==
This command writes the extraction result data in file: /data/test.nc

	./sos_client.py --verbose --auth-mode=none -s {SOS_SERVER_URL} -d CORIOLIS-RECOPESCA -b sea_water_temperature -t 2017-12-27T12:28:01.000+01:00 -T 2017-12-28T12:28:01.000+01:00 -y 16.10438 -Y 62.3397 -x -61.55259 -X 7.16829 -o /data -f test.nc

The HTTP(s) URL is displayed on stdout. This URL is a direct link to the file which is available for download.

	./sos_client.py --verbose --auth-mode=none -s {SOS_SERVER_URL} -d CORIOLIS-RECOPESCA -b sea_water_temperature -t 2017-12-27T12:28:01.000+01:00 -T 2017-12-28T12:28:01.000+01:00 -y 16.10438 -Y 62.3397 -x -61.55259 -X 7.16829 -o console

==GETCAPABILITIES==
Download and save the xml file which contains metadata about the service, including offerings and parameters.

	./sos_client.py --verbose --auth-mode=none -s {SOS_SERVER_URL} --capabilities -o /data -f capabilities.xml

==DESCRIBESENSOR==
Download and save the xml file which contains the list of procedures associated to an offering.

	./sos_client.py --verbose --auth-mode=none -s {SOS_SERVER_URL} -d CORIOLIS-RECOPESCA --describeSensor -o /data -f describesensor.xml

REQUIRED MODULES
================

No module required.


BUGS AND QUESTIONS
==================

Please refer to the documentation for information on submitting bug reports or questions to the author.


AUTHOR
======

IFREMER

http://wwz.ifremer.fr/

