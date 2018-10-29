# AWS-Python-API

AWS Python boto3 API tool allowing for uploading and downloading files. 

Required libraries: boto3, argparse, and json.  

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
