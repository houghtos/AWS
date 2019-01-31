import boto3.s3.transfer
from boto3.s3.transfer import S3Transfer
import argparse
import hashlib
import os,sys
import json
import io
import threading

# Class for tracking percent progress for uploads.  
# This class is given as argument to the S3 transfer upload function.
class ProgressPercentage(object):
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



#Creates object that calculates MD5sum, writes it to the local directory wiht file name
#Takes local file location as input.  Outputs the local file location to the MD5sum.
class md5sum:
    def __init__(self, local):
        self.local = local
        self.fileInput = self.local.split('/')
        self.fileInput = self.fileInput[-1]
    
    #Obtains MD5sum of file and writes output
    def md5Calc(self):
        hash_md5 = hashlib.md5()
        with open(self.local, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        md5WriteDirectory = self.local + '.md5'
        md5Value = self.fileInput + ' ' + hash_md5.hexdigest()
        f = open(md5WriteDirectory, "w")
        f.write(md5Value)
        return (md5WriteDirectory)


#Function for uploading file to S3 using light weight boto3 client.
#Depends on ProgressPercentage object to output upload progress.
#Requires for you to run configure before using.
def awsUpload(bucket, local_path, s3_path):
    with open('uploaderConfig.json') as f:
        configVals = json.load(f)
        aws_key = configVals['access_key']
        aws_secret_key = configVals['aws_secret_key']
        region = configVals['region']
    client = boto3.client('s3', configVals['region'],
            aws_access_key_id = configVals['access_key'],
            aws_secret_access_key = configVals['aws_secret_key']
            )
    transfer = S3Transfer(client)

    transfer.upload_file(
        local_path, 
        bucket , 
        s3_path,  
        callback=ProgressPercentage(local_path)
    )

#Function to initialize arguments from argparse.
def processArguments():
    parser = argparse.ArgumentParser(description=r"Script calculates MD5sum for file and uploads it to designated AWS S3 location.")

    ### Create sub parser for each function menus
    subparsers = parser.add_subparsers(dest='options', help='choose script action')

    ### Call routine to uplaod single file.
    price_parser = subparsers.add_parser('su', help='Single File upload')
    price_parser.add_argument('-b', '--su_bucket', help='Bucket to which the single file should be uploaded')
    price_parser.add_argument('-p', '--su_prefix', help='Prefix which to upload the file to.')
    price_parser.add_argument('-l', '--su_local', help='Full local file path of the file you wish to upload.')

    ### Call routine to upload folder of files.
    price_parser = subparsers.add_parser('fu', help='Upload all files in folder')
    price_parser.add_argument('-b', '--fu_bucket', help='Bucket to which the single file should be uploaded')
    price_parser.add_argument('-p', '--fu_prefix', help='Prefix which to upload the file to.')
    price_parser.add_argument('-l', '--fu_local', help='Full local file path for the folder you wish to upload all files within.')

    price_parser = subparsers.add_parser('configure', help='Configure with AWS region and key credentials (if not already done through AWS CLI)')
    return (parser.parse_args())


if __name__ == "__main__":

    #Initiate arguments in main function.
    args = processArguments()

    #Configure AWS key, secret key, and region.
    if args.options.lower() == 'configure':

        jsonInput = {
                    'access_key': '',
                    'aws_secret_key': '',
                    'region': ''
                    }

        aws_key = input('AWS Access Key: ')
        aws_secret_key = input('AWS Secret Access Key: ')
        region = input('AWS region: ')

        jsonInput['access_key'] = aws_key
        jsonInput['aws_secret_key'] = aws_secret_key
        jsonInput['region'] = region

        #Implement try-catch block for checking unicode.
        #This ensures writing to a file is in in unicode :
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str
        #Write config.json file in unicode standard utf-8. 
        with io.open('uploaderConfig.json', 'w', encoding='utf8') as outfile:
            strOut = json.dumps(jsonInput,
                            indent=4, sort_keys=True,
                            separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(strOut))


    #Single upload argument.
    if args.options.lower() == 'su':
        
        md5 = md5sum(args.su_local) 
        md5Upload = md5.md5Calc()
        md5File = md5Upload.split('/')
        md5File = md5File[-1]


        awsUpload(
            args.su_bucket, 
            md5Upload, 
            args.su_prefix + md5File
        )
        
        os.remove(md5Upload)

        tempName = args.su_local
        tempName = tempName.split('/')
        tempName = tempName[-1]
        
        awsUpload(
            args.su_bucket, 
            args.su_local, 
            args.su_prefix + tempName
        )

    #Upload all files in folder.
    elif args.options.lower() == 'fu':
        fileList = os.listdir(args.fu_local)
        for j in fileList:
            try:
                tempPath = args.fu_local + j
                md5 = md5sum(tempPath) 
                md5Upload = md5.md5Calc()
                md5File = md5Upload.split('/')
                md5File = md5File[-1]
                awsUpload(args.fu_bucket, md5Upload, args.fu_prefix + md5File)
                os.remove(md5Upload)

                awsUpload(
                    args.fu_bucket, 
                    args.fu_local + j, 
                    args.fu_prefix + j
                )

            except:
                pass

    except:
        print("Invalid argument given.  Only accepts 'configure', 'su', and 'fu'")
