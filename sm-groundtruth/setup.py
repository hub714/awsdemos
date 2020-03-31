import boto3
import jsonlines
import sys
from os import listdir, walk
from os.path import isfile, join

# bucketName = 'huberttest'
bucketName = 'huberttest-pdx'
bucketPath = 'sm-groundtruth'
localPath = 'images'

outputJSON = []

s3client = boto3.client('s3')

#print(s3client.head_object(Bucket=bucketName, Key=bucketPath))

def doesPrefixExist(bucketName, s3Prefix):
    try:
        s3List = s3client.list_objects_v2(Bucket=bucketName, Prefix=s3Prefix)
        if(s3List['KeyCount'] > 0):
            return "The bucket path s3://"+bucketName+"/"+s3Prefix+" already exists. Clear it out first"
        else:
            return False
    except Exception as e:
        return e

def doesObjectExist(bucketName, s3key):
    try:
        s3client.head_object(Bucket=bucketName, Key=s3key)
        return True
    except:
        return False

def uploadObject(localObject, bucketName, s3key):
    try:
        s3client.upload_file(localObject, bucketName, s3key)
        #print(s3client.put_object_acl(ACL='public-read', Bucket=bucketName, Key=s3key))
        return True
    except Exception as e:
        return e

# Check if the bucket and prefix exist. If it does, exit.
prefixExists = doesPrefixExist(bucketName, bucketPath)

if(prefixExists):
    print("Error when checking if prefix exists: "+str(prefixExists))
    sys.exit()

# Upload the files and create manifest
# Lists the local directory (images by default), creates an outputJSON with the proper
# source-ref formatting, then uploads the object to S3
for f in listdir(localPath):
    outputJSON.append({'source-ref': "s3://"+bucketName+"/"+bucketPath+"/"+localPath+"/"+f})
    if(uploadObject(localPath+"/"+f, bucketName, bucketPath+"/"+localPath+"/"+f)):
        print("Uploaded "+f)
    else:
        print("There was an error uploading the file "+f)

# Print the actual manifest.json to local folder
with jsonlines.open('manifest.json', 'w') as outfile:
    outfile.write_all(outputJSON)

# Finally, upload the manifest file to S3
response = uploadObject('manifest.json', bucketName, bucketPath+"/manifest.json")

if (response):
    print("Manifest.json successfully uploaded to S3")
else:
    print("There was an error uploading the manifest.json to S3: "+response)
