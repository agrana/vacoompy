# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 05:46:49 2017

@author: maint
"""

# -*- coding: utf-8 -*-
import os
from os.path import expanduser
import time
import shutil
import configparser
import ast
import logging

# Home and default folders
home = expanduser("~")
base = home + '/.vacoom/'
rules = base + 'rules.ini'
logfile = base + 'vacoom.log'

# Logging
logger = logging.getLogger('vacoom')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

#Configuration
Config = configparser.ConfigParser()
Config.read(rules)
rules = Config.sections()

# Results.
matched_files = []
matched_files_dict = {}
file_count = 0
scanned_files = 0

# start timer
start_time = time.time()
# Reading rules from configuration and starting to fill collections of files to act on.
for rule in rules:
    # if rule is disabled continue.
    if Config.get(rule, 'enabled') != '1':
        logger.info('not processing => %s , is not enabled', rule)
        continue
    directories=ast.literal_eval(Config.get(rule, 'directories'))
    extensions=ast.literal_eval(Config.get(rule, 'extensions'))
    for directory in directories:
        for root, dirs, files in os.walk(directory, topdown=True):
            for file in files:
                scanned_files += 1
                for ext in extensions:
                    # Exclude hidden unix files.
                    files = [f for f in files if not f[0] == '.']
                    dirs[:] = [d for d in dirs if not d[0] == '.']
                    if (file.endswith(ext)):
                        matched_files_dict[os.path.join(root, file)] = rule
end_time = time.time()
elapsed_time = end_time - start_time
file_count = len(matched_files)
logger.info('matched files %s scanned files %s', file_count, scanned_files)
logger.info('seconds to scan %s', elapsed_time)
# Actions
def copyf(f, dst):
    try:
        logger.info('copying %s to %s', f, dst)
        shutil.copyfile(f, dst)
    except shutil.SameFileError:
        logger.warning('%s and %s are the same file', f, dst)
    except Exception as e:
        logger.warning('an exception occurred: %s', e)
def movef(f, dst):
    try:
        logger.info('moving %s to %s', f, dst)
        shutil.move(f, dst)
    except shutil.SameFileError:
        logger.warning('%s and %s are the same file', f, dst)
    except Exception as e:
        logger.warning('an exception occurred: %s', e)
def delf(f):
    try:
        logger.info('deleting %s', f)
        os.remove(f)
    except Exception as e:
        logger.warning('an exception occurred: %s', e)
for k, v in matched_files_dict.items():
    if Config.get(v, 'destination') in k:
        print('Already in destination', k ,'in', Config.get(v, 'destination'))
        continue
    if Config.get(v, 'enabled') == '0':
        print('nothing')
        continue
    else:
        if Config.get(v, 'action') == 'delete':
            delf(k)
        elif Config.get(v, 'action') == 'move':
            movef(k, Config.get(v, 'destination'))
        elif Config.get(v, 'action') == 'copy':
            copyf(k, Config.get(v, 'destination'))
        else:
            logger.warning('bad action %s for rule %s', v, Config.get(v, 'action'))
