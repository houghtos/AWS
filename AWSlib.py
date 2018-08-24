import os, sys
from subprocess import check_output
import threading
import hashlib 
import subprocess 
import json 

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

#Object that obtains MD5 hash values for local and S3 file.
#Neither SHA1 or SHA2 are supported by AWS S3 metadata 
class MD5parse:
    def __init__(self, bucket, s3_path, local_path):
        self.bucket = bucket
        self.s3_path = s3_path
        self.local_path = local_path

    def localMD5(self):
        localmd5 = os.popen('md5sum {}'.format(self.local_path)).read()
        md5_split = localmd5.split('  ')
        local_hash = md5_split[0]
        return(local_hash)

    def awsMD5(self):
        object_head = os.popen('aws s3api list-objects --bucket {} --prefix {}'.format(self.bucket,self.s3_path)).read()
        #print(object_head)
        aws_md5 = json.loads(object_head)
        aws_md5 = aws_md5["Contents"]
        aws_md5 = aws_md5[0]
        aws_md5 = aws_md5['ETag']
        aws_md5 = str(aws_md5.replace('"',''))
        return(aws_md5)

