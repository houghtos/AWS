# S3 MD5/File Uploader for python3

Uploads single file or all files in a specified directory S3 along with a calculated MD5sum.  

Required packes:

1. boto3
2. hashlib
3. io
4. threading

## To run:

...
  
###### See argparse help for more information on each of the four arguments in AWS_Main.py.

## Action arguments:
1. su - Use for single upload
2. fu - Use to upload folder (folder upload.)
3. configure - use to configure "uploaderConfig.json", a file that will contain the AWS key, secret key, and region.

## Example Usage:
  #Configure and write uploaderConfig.json
  
  $ python AWS_Main.py configure
  
  #Upload MD5sum file and fileToUpload.txt
  
  $ python AWS_Main.py su mybucket S3Prefix/ /home/users/sean/fileToUpload.txt
  
  #Upload MD5sum files and all files in /home/users/sean/
  
  $ python AWS_Main.py fu mybucket S3Prefix/ /home/users/sean/
