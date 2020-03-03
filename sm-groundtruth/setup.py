import boto3
import jsonlines
import sys
from os import listdir, walk
from os.path import isfile, join

bucketName = 'huberttest'
bucketPath = 'sm-groundtruth'
localPath = 'images'

outputJSON = []

s3client = boto3.client('s3')

#print(s3client.head_object(Bucket=bucketName, Key=bucketPath))

def doesPrefixExist(bucketName, s3Prefix):
    try:
        s3List = s3client.list_objects_v2(Bucket=bucketName, Prefix=s3Prefix)
        if(s3List['KeyCount'] > 0):
            return True
        else:
            return False
    except:
        return True

def doesObjectExist(bucketName, s3key):
    try:
        s3client.head_object(Bucket=bucketName, Key=s3key)
        return True
    except:
        return False

def uploadObject(localObject, bucketName, s3key):
    try:
        s3client.upload_file(localObject, bucketName, s3key)
        return True
    except Exception as e:
        return e

if(doesPrefixExist(bucketName, bucketPath)):
    print("The bucket path s3://"+bucketName+"/"+bucketPath+" already exists. Clear it out first")
    sys.exit()

for f in listdir(localPath):
    outputJSON.append({'source-ref': "s3://"+bucketName+"/"+bucketPath+"/images/"+f})
    #s3client.upload_file(localPath+"/"+f, bucketName, bucketPath+"/images/"+f))
    if(uploadObject(localPath+"/"+f, bucketName, bucketPath+"/images/"+f)):
        print("Uploaded "+f)

#print(outputJSON)

with jsonlines.open('manifest.json', 'w') as outfile:
    outfile.write_all(outputJSON)
#
# for root, dirs, files in walk(localPath):
#     #print("hi")
#     print(files)

# def upload_images():
#     try:
