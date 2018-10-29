import boto3.s3.transfer
from boto3.s3.transfer import S3Transfer
import argparse

# Class for tracking percent progress for uploads.  
# This class is given as argument to the S3 transfer upload function.
class ProgressPercentageUpload(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

#Uploads object to S3 bucket.
def awsUpload(bucket, local_path, s3_path):
    try:
        transfer.upload_file(
            local_path, 
            bucket , 
            s3_path,  
            callback=ProgressPercentage(local_path)
        )
    except:
        print("Error in uploading file.  Please ensure you credentials are correctly configured, the S3 bucket is valid, and the local file path is correct.")

#Download file to local drive.
def downloadObj(bucket, s3_path, local_path):
    try:
        transfer.download_file(
            '{bucket}'.format(bucket=bucket),
            '{s3_path}'.format(s3_path=s3_path),
            local_path
        )
    except NameError: 
        print("Name error on downloading.  Please specify correct path for object you are downloading and a proper name for saving")
        print("""Reminder: objects are saved to the directory the Python script is run from.  You cannot specify a directory such as 'home/user/download'.  This will invoke a name error.""")
    return(result)

if __name__ == "__main__":
    transfer = S3Transfer(
        boto3.client(
            's3',
            'us-west-1'#,
            #aws_access_key_id = 'yourKeyHere',
            #aws_secret_access_key = 'yourSecretKeyHere'
        )
    )
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "action", 
        help="What action you wish to perform. Options are 'download' or 'upload'.
        type=str
    )
    
    parser.add_argument(
        "local", 
        help="The full local file address where you are downloading the file to, uploading the file from, or only checking the MD5sum against.  Please use frontslashes only between directories",
        type=str
    )
    
    parser.add_argument(
        "bucket", 
        help="The name of the S3 bucket you are interacting with.", 
        type=str
    )
    
    parser.add_argument(
        "s3_path", 
        help="The S3 object prefix you are interacting with.  For uploads, you will need to include the file name as well,", 
        type=str
    )
    
    args = parser.parse_args()

    if args.action == 'download':
        downloadObj(
                    args.bucket, 
                    args.s3_path, 
                    args.local
                   )
        
    elif args.action == 'upload':
        awsUpload(
            args.bucket, 
            args.local, 
            args.s3_path
        )
        
    else:
        print("Invalid action given: " + args.action)
        print("Only actions available are 'download' or 'upload'")  
