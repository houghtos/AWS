# AWS-Python-API

AWS Python SDK boto3 tool for uploading and downloading objects to S3.  Uses python3.

The AWS CLI is a python program that is written using Boto3 and provides a unified interface to all AWS service APIs.  This tool allows easy integration with other software and for customization on the AWS SDK level for S3 interaction.

Required libraries: boto3 and argparse.  

## To run:

In AWS_Main.py, ensure the correct AWS keys and region for accessing your S3 are entered for the boto3 client (lines 72-76).  

Usage:

  $ python AWS_Main.py [action] [local filepath] [S3 bucket] [S3 prefix]
  
###### See argparse help for more information on each of the four arguments in AWS_Main.py.

## Action arguments:
1. download
2. upload
