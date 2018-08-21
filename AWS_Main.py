import boto3
import boto3.s3.transfer
from boto3.s3.transfer import S3Transfer
import os, sys
import argparse
from AWSlib import ProgressPercentageUpload, MD5parse

#Routine to write MD5sum sum output as TSV to designated file.
#File location and name must be set below. 
def writeMD5(output):
    filename = "/home/user/person/md5sum_outputs.tsv" #<< Set file name manually for where outputs will be written.
    if os.path.exists(filename):
        append_write = 'a' 
    else:
        append_write = 'w' 

    f = open(filename,append_write)
    f.write(output + '\n')
    f.close()
    return()

#Uploads file to S3 bucket and then compares local and S3 MD5 hash values to ensure they match.  Results written to tsv.
def awsUpload(bucket, local_path, s3_path):
    transfer.upload_file(local_pathh, bucket , s3_path,  callback=ProgressPercentage(local_path))
    md5_obj = MD5parse(bucket, s3_path, local_path)
    local_hash = md5_obj.localMD5()
    aws_md5 = md5_obj.awsMD5()
    result = aws_md5 == str(local_hash)
    output = "Object Name: " + s3_path.split('/')[-1] + "\t" + "AWS MD5 Hash: " + aws_md5 + "\t" + "Local MD5 Hash: " + str(local_hash) + "\t" + "File upload" + "\t" + "Match is " + str(result)
    writeMD5(output)

    print("MD5sum match for: " + s3_path.split('/')[-1])
    print(output)
    print("Result is " + str(result))
    return(result)

#Checks if MD5 hash values match from S3 and local files.  
def checkMD5match(bucket, local_path, s3_path):
    md5_obj = MD5parse(bucket, s3_path, local_path)
    local_hash = md5_obj.localMD5()
    aws_md5 = md5_obj.awsMD5()
    result = aws_md5 == str(local_hash)
    output = "Object Name: " + s3_path.split('/')[-1] + "\t" + "AWS MD5 Hash: " + aws_md5 + "\t" + "Local MD5 Hash: " + str(local_hash) + "\t" + "MD5 match" + "\t" + "Match is " + str(result)
    writeMD5(output)

    print("MD5sum match for: " + s3_path.split('/')[-1])
    print(output)
    print("Result is " + str(result))
    return(result)

#Download file to local drive and then compares local and S3 MD5 hash values to ensure they match.  Results written to tsv.
def downloadObj(bucket, s3_path, local_path):
    try:
        transfer.download_file('{bucket}'.format(bucket=bucket),'{s3_path}'.format(s3_path=s3_path),local_path)  #Set your download path here.  Currently will attempt to save to C: drive.  Can also specify path in savename. 
        md5_obj = MD5parse(bucket, s3_path, local_path)
        local_hash = md5_obj.localMD5()
        aws_md5 = md5_obj.awsMD5()
        result = aws_md5 == str(local_hash)
        output = "Object Name: " + s3_path.split('/')[-1] + "\t" + "AWS MD5 Hash: " + aws_md5 + "\t" + "Local MD5 Hash: " + str(local_hash) + "\t" + "File upload" + "\t" + "Match is " + str(result)
        writeMD5(output)

        print("MD5sum match for: " + s3_path.split('/')[-1])
        print(output)
        print("Result is " + str(result))

    except NameError: 
        print("Name error on downloading.  Please specify correct path for object you are downloading and a proper name for saving")
        print("""Reminder: objects are saved to the directory the Python script is run from.  You cannot specify a directory such as 'home/user/download'.  This will invoke a name error.""")
    return(result)

if __name__ == "__main__":
    transfer = S3Transfer(boto3.client(
    's3',
    'us-east-1'#,
    #aws_access_key_id = 'yourKeyHere',
    #aws_secret_access_key = 'yourSecretKeyHere'
        )
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="What action you wish to perform. Options are 'download', 'upload', or 'check'. The check action looks if your local file md5 hash matches the S3 md5 hash",   type=str)
    parser.add_argument("local", help="The full local file address where you are downloading the file to, uploading the file from, or only checking the MD5sum against.  Please use frontslashes only between directories", type=str)
    parser.add_argument("bucket", help="The name of the S3 bucket you are interacting with.", type=str)
    parser.add_argument("s3_path", help="The S3 object prefix you are interacting with.  For uploads, you will need to include the file name as well,", type=str)
    args = parser.parse_args()

    if args.action == 'download':
        downloadObj(args.bucket, args.s3_path, args.local)
    elif args.action == 'upload':
        awsUpload(args.bucket, args.local, args.s3_path)
    elif args.action == 'check':
        checkMD5match(args.bucket, args.local, args.s3_path)
    else:
        print("Invalid action given: " + args.action)
        print("Only actions available are 'download', 'upload', or 'check'")  
