# AWS-Python-API

Python API scripts for comparing and logging MD5 hash sums on your local directory with S3 files. Allows for three functions: upload, download, or check file.  Upload/download will compare local with S3 file while logging both MD5 sums.  Check function used to compare local MD5 sum file values with those on S3.

Written in python 3
Requires libraries: boto3, hashlib, argparse, and json.  Other libraries should be native to python.

## To run:

  1. Both files must be in the same direcory to run.  The AWS_Main.py script will import classes from AWSlib.py

  2. Set variable "filename" in AWS_Main.py (line 11) to where the log output will write or append to.  Script will create the file on   first run (if filename doesn't exist) and append values once it is created.

  3. In AWSlib.py under class 'MD5parse' and function 'localMD5' (line 35) you will need to set your OS system's MD5sum command.  Here it is set as default "md5sum" for the Windows Subsystem for Linux (WSL).  For mac file systems this is "md5".  You will need to ensure this is set as correct command for your OS.

  4. In AWS_Main.py, ensure the correct AWS keys and region for accessing your S3 are entered for the boto3 client (lines 72-76).  

Usage:

  $ python AWS_Main.py [action] [local filepath] [S3 bucket] [S3 prefix]
  
###### See argparse help for more information on each of the four arguments in AWS_Main.py.

## Action arguments:
1. download
2. upload
3. check
