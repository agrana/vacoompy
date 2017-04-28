#!/usr/bin/python

import argparse
import glob
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("folder", type=str, help="folder to process")
parser.add_argument("extension", type=str, help="extension of the files to process")
parser.add_argument("action", type=str, help="action to execute over the files matched")

# Arguments to variables is this really needed?
args = parser.parse_args()
fold = args.folder
ext = args.extension
action = args.action

# list containning files to process.
listoffiles = []

# Exiting if folder to process does not exists

if not os.path.exists(fold):
    print "folder does not exists quiting"
    sys.exit

for file in glob.glob(fold+"/"+"*."+ext):
    listoffiles.append(file)

print(listoffiles)
