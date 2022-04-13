#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python OGC/SOS client
#
# SOS web service request standard for SWE (Sensor Web Enablement) framework
#  
# 



import traceback
import platform
import sys
import os
import datetime
import logging.config
import configparser
import optparse


# The necessary required version of Python interpreter
REQUIRED_VERSION = (2,7)

# error code to use when exiting after exception catch
ERROR_CODE_EXIT=1

# the config file to load from 
CFG_FILE = '~/sos-client/sos-client-python.ini'
LOG_CFG_FILE = './etc/log.ini'

# project libraries path
LIBRARIES_PATH = os.path.join(os.path.dirname(__file__), './lib')

SECTION = 'Main'

# shared logger
log = None

# shared variables to download
_variables = []

# Manage imports of project libraries
if not os.path.exists(LIBRARIES_PATH):
    sys.stderr.write('\nERROR: can not find project libraries path: %s\n\n' % os.path.abspath(LIBRARIES_PATH))
    sys.exit(1) 
sys.path.append(LIBRARIES_PATH)  

# Import project libraries
import utils_log
import utils_messages
import sos_api

def get_client_version():
    """Return the version (as a string) of this client.
    
    The value is automatically set by the maven processing build, so don't 
    touch it unless you know what you are doing."""
    return sos_api.get_client_version()

def get_client_artefact():
    """Return the artifact identifier (as a string) of this client.
    
    The value is automatically set by the maven processing build, so don't 
    touch it unless you know what you are doing."""
    return sos_api.get_client_artefact()   
                                     
def load_options():
    """load options to handle"""

    _options = None
    
    # create option parser
    parser = optparse.OptionParser(version=get_client_artefact() + ' v' + get_client_version())
    
    # create config parser
    conf_parser = configparser.SafeConfigParser()
    conf_parser.read(os.path.expanduser(CFG_FILE))
                     
    # add available options
    parser.add_option( '--quiet', '-q',
                       help = "prevent any output in stdout",
                       action = 'store_const',
                       const = logging.WARN,
                       dest='log_level')

    parser.add_option( '--verbose',
                       help = "print information in stdout",
                       action='store_const',
                       const = logging.DEBUG,
                       dest='log_level')
 
    parser.add_option( '--noisy',
                       help = "print more information (traces) in stdout",
                       action='store_const',
                       const = utils_log.TRACE_LEVEL,
                       dest='log_level')
                       
    parser.add_option( '--user', '-u',
                       type = 'string',
                       help = "the user name (string)")

    parser.add_option( '--pwd', '-p',
                       type = 'string',
                       help = "the user password (string)")
                       
    parser.add_option( '--auth-mode',
                       default = sos_api.AUTHENTICATION_MODE_CAS,
                       type = 'string',
                       help = "the authentication mode: '" + sos_api.AUTHENTICATION_MODE_NONE  +
                              "' (for no authentication) or '"+sos_api.AUTHENTICATION_MODE_CAS +
                              "' (for Central Authentication Service) [default: %default]")
                       
    parser.add_option( '--server', '-s',
                       help = "the sos server to use (url)")
                              
    parser.add_option( '--offering-id', '-d',
                       help = "The offering (dataset) to subset and download (string)")
    
    parser.add_option( '--observed-property', '-b',
                       help = "The observed property (string)")
    
    parser.add_option( '--procedure', '-r',
                       help = "The procedure id requested ex:'INS-CORIOLIS-GLO-NRT-OBS_PROFILE_LATEST__1901118' (string)."+
                       "To discover procedures for an offering, run a '--describeSensor' request")

    parser.add_option( '--date-min', '-t',
                       help = "The min date (string following format YYYY-MM-DDTHH:MM:SS.sssZ)")

    parser.add_option( '--date-max', '-T',
                       help = "The max date (string following format YYYY-MM-DDTHH:MM:SS.sssZ)")
               
    parser.add_option( '--latitude-min', '-y',
                       type = 'float',
                       help = "The min latitude (float in the interval [-90 ; 90])")

    parser.add_option( '--latitude-max', '-Y',
                       type = 'float',
                       help = "The max latitude (float in the interval [-90 ; 90])")
               
    parser.add_option( '--longitude-min', '-x',
                       type = 'float',    
                       help = "The min longitude (float in the interval [-180 ; 180])")

    parser.add_option( '--longitude-max', '-X',
                       type = 'float',    
                       help = "The max longitude (float in the interval [-180 ; 180])")
                       
    parser.add_option( '--sync-mode', '-S',
                       help = "Only for download requests, sets the download mode to synchronous",
                       action='store_true',
             dest='sync')
                      
    parser.add_option( '--describeSensor', '-D',
                       help = "Discover list of procedures provided by a dataset. Output is in XML format",
                       action='store_true',
             dest='describeSensor') 

    parser.add_option( '--capabilities', 
                       help = "Discover the capabilities (offering, observed properties, procedure) provided by the service",
                       action='store_true',
                       dest='getCapabilities')      
    
    parser.add_option( '--out-dir', '-o',
                       help = "The output dir where result (download file) is written (string). If it starts with 'console', behaviour is the same as with --console-mode. ",
                       default=".")
               
    parser.add_option( '--out-name', '-f',
                       help = "The output file name (string)",
                       default="data.nc")
                                              
    parser.add_option( '--socket-timeout',
                       type = 'float',
                       help = "Set a timeout on blocking socket operations (float expressing seconds)")     
                                    
    parser.add_option( '--user-agent',
                       help = "Set the identification string (user-agent) for HTTP requests. By default this value is 'Python-urllib/x.x' (where x.x is the version of the python interpreter)")
                                              
    parser.add_option( '--outputWritten',
                       help = "Optional parameter used to set the format of the file returned by the download request: netcdf, json or xml. If not set, netcdf is used.",                      
                       default="netcdf")
    
    parser.add_option( '--console-mode',
                       help = "Optional parameter used to display result on stdout, either URL path to download extraction file, or the XML content of getCapabilities or describeSensor requests (not recommended for netcdf download).",
                       action='store_true',
                       dest='console_mode')                      
    
    
    # set default values by picking from the configuration file
    default_values = {}
    default_variables = []
    for option in parser.option_list:        
        if (option.dest != None) and conf_parser.has_option(SECTION, option.dest):
            if option.dest == "variable":
                default_variables.append(conf_parser.get(SECTION, option.dest))
                default_values[option.dest] = default_variables
            else:    
                default_values[option.dest] = conf_parser.get(SECTION, option.dest)
    
    parser.set_defaults( **default_values )
                      
    return parser.parse_args()
    
def option_callback_variable(option, opt, value, parser):
    global _variables
    _variables.append(value)
    setattr(parser.values, option.dest, _variables)
    
def check_version():
    """Utilitary function that checks the required version of the python interpreter
    is available. Raise an exception if not."""
    
    global REQUIRED_VERSION
    cur_version = sys.version_info
    if (cur_version[0] > REQUIRED_VERSION[0] or
        cur_version[0] == REQUIRED_VERSION[0] and
        cur_version[1] >= REQUIRED_VERSION[1]):   
        return
    else:
        raise Exception( "This tool uses python 2.7 or greater. You version is %s. " % str(cur_version) )
    
#===============================================================================
# The Main function
#===============================================================================
if __name__ == '__main__':
    check_version()
    start_time = datetime.datetime.now()
    
    # first initialize the logger
    logging.addLevelName(utils_log.TRACE_LEVEL, 'TRACE')
    logging.config.fileConfig(  os.path.join(os.path.dirname(__file__),LOG_CFG_FILE) )
    log = logging.getLogger("sos-client-python")
        
    logging.getLogger().setLevel(logging.INFO)
    
    try:
        # we prepare options we want
        (_options, args) = load_options()    

        if _options.log_level != None:
            logging.getLogger().setLevel(int(_options.log_level))
                   
        sos_api.execute_request(_options)       
    except Exception as e:
        log.error( "Execution failed: %s", e )
        if hasattr(e, 'reason'):
            log.info( ' . reason: %s', e.reason )
        if hasattr(e, 'code'):
            log.info( ' . code  %s: ', e.code )
        if hasattr(e, 'read'):
            log.log( utils_log.TRACE_LEVEL, ' . detail:\n%s', e.read() )
        
        log.debug( '-'*60 )
        log.debug( "Stack trace exception is detailed herafter:" )
        exc_type, exc_value, exc_tb = sys.exc_info()
        x = traceback.format_exception(exc_type, exc_value, exc_tb)
        for stack in x:
            log.debug( ' . %s', stack.replace('\n', '') )
        log.debug( '-'*60 )
        log.log( utils_log.TRACE_LEVEL, 'System info is provided hereafter:' )
        system, node, release, version, machine, processor = platform.uname()
        log.log( utils_log.TRACE_LEVEL, ' . system   : %s', system )
        log.log( utils_log.TRACE_LEVEL, ' . node     : %s', node )
        log.log( utils_log.TRACE_LEVEL, ' . release  : %s', release )
        log.log( utils_log.TRACE_LEVEL, ' . version  : %s', version ) 
        log.log( utils_log.TRACE_LEVEL, ' . machine  : %s', machine )
        log.log( utils_log.TRACE_LEVEL, ' . processor: %s', processor )
        log.log( utils_log.TRACE_LEVEL, ' . python   : %s', sys.version )
        log.log( utils_log.TRACE_LEVEL, ' . client   : %s', get_client_version() )
        log.log( utils_log.TRACE_LEVEL, '-'*60 )

        sys.exit(ERROR_CODE_EXIT)

    finally:
        log.debug( "Elapsed time : %s", str(datetime.datetime.now() - start_time) )

