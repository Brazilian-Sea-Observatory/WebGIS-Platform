import logging
import os
import re
import requests
import shutil
import tempfile

from datetime import date, datetime, timedelta
from typing import List
from urllib3.exceptions import HTTPError

def download_file(url, filepath):
    r = requests.get(url, timeout=10, stream=True)

    # store data in temporary file
    if r.status_code == 200:
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                tmpfile.write(chunk)
        
        tmpfile.close()
    
        # rename file after successfull download
        shutil.move(tmpfile.name, filepath)
    else:
        logging.error('Server returned status code %03d' % r.status_code)
        logging.error(r.text)
        r.raise_for_status()

def list_old_folders(start_dir: str, retention_days: int) -> List[str]:
    """
    List old folders

    Parameters:
        start_dir (str): base directory to scan for subdirectories
        retention_days (int): maximum number of days (age) that should be kept
    
    Returns:
        List[str]: a list of paths (folders) that were deleted
    """
    date_folder_pattern = re.compile(r'[0-9]{4}[0-9]{2}[0-9]{2}')

    current_date = datetime.utcnow().date().today()
    date_reference = current_date - timedelta(days=retention_days)
    
    old_folders: List[str] = []

    # List all subfolders under the model's data folder and extract dates from the path
    folders = [f for f in os.listdir('%s' % (start_dir)) if os.path.isdir('%s/%s' % (start_dir, f))]
    
    # check if folder match a date
    for f in folders:
        is_date = date_folder_pattern.match(f)
        if is_date:
            # extract date from folder name
            folder_date = datetime.strptime(f, '%Y%m%d').date()
            if folder_date < date_reference:
                old_folders.append('%s/%s' % (start_dir, f))
        else:
            old_folders = old_folders + list_old_folders('%s/%s' % (start_dir, f), retention_days)
            
    return old_folders

def delete_old_folders(start_dir: str, retention_days: int = 1) -> List[str]:
    """
    Deletes folders with date pattern that are expided

    Parameters:
        start_dir (str): base directory to scan for subdirectories
        retention_days (int): maximum number of days (age) that should be kept
    
    Returns:
        List[str]: a list of paths (folders) that were deleted
    """
    old_folders = list_old_folders(start_dir, retention_days)
    for f in old_folders:
        logging.info('Deleting folder: %s' % f)
        shutil.rmtree(f)
    return old_folders