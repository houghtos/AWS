# !! This is out of date!  ETAG no longer captures MD5 sum for files larger than 10MB!  Will update.

# AWS-Python-API

Command line Python boto3 API tool comparing and logging MD5 hash sums on your local directory with S3 files. Allows three functions: 
1. Upload from local directory to S3 and compare MD5 values of the two files. 
2. Download from S3 to local directory and compare MD5 values of the two files.
3. Check MD5sum on file on your local drive with MD5sum of S3 object.  

Written in python 3

Required python libraries: boto3, hashlib, argparse, and json.  

## To run:

  1. Both python files should be in the same directory.

  2. Set variable "filename" in AWS_Main.py (line 11) to where the log output will write or append to.  Will create new text file for output on first run (if file doesn't exist) and append values if the files does exist.

  3. In AWSlib.py under class 'MD5parse' and function 'localMD5' (line 35) you will need to set your OS system's MD5sum command.  Here it is set as default "md5sum" for the Windows Subsystem for Linux (WSL).  For mac file systems this is "md5".  You will need to ensure this is set as correct command for your OS.

  4. In AWS_Main.py, ensure the correct AWS keys and region for accessing your S3 are entered for the boto3 client (lines 72-76).  

Usage:

  $ python AWS_Main.py [action] [local filepath] [S3 bucket] [S3 prefix]
  
###### See argparse help for more information on each of the four arguments in AWS_Main.py.

## Action arguments:
1. download
2. upload
3. check
