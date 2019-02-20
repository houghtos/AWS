# S3 MD5/File Uploader for python3

Uploads single file or all files in a specified directory S3 along with calculated MD5sums.  

Generates text file containing the MD5sum value for an object (e.g. file.bam.md5).  Subsequently uploads object and text file and then removes the MD5 text file from your local machine.  Subsequently annotates the uploaded object's metadata with the MD5sum value. 

## Required Python packages:

1. boto3
2. hashlib
3. io
4. threading
 
## Configure:
Before using, run the "configure" command before beginning uploads (see example usage).  This will prompt you for you AWS key/secret_key and region.

## Arguments:
1. **su** - Use for single file upload
2. **fu** - Use to upload all files in folder (folder upload.)
3. **configure** - use to configure "uploaderConfig.json", a file that will contain the AWS key, secret key, and region.

## Example Usage:
   
  Configure and write AWS credentials to uploaderConfig.json:
  
  `$ python S3Uploader.py configure`
  
  Upload MD5sum file and single file.  Example file in this case is "fileToUpload.txt"
  
  `$ python S3Uploader.py su mybucket S3Prefix/ /home/users/sean/fileToUpload.txt`
  
  Upload MD5sum files and all files in folder "/home/users/sean/"
  
  `$ python AS3Uploader.py fu mybucket S3Prefix/ /home/users/sean/`
