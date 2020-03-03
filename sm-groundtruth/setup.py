import boto3
import jsonlines
from os import listdir
from os.path import isfile, join

bucketName = 'huberttest'
bucketPath = 'sm-groundtruth'

outputJSON = []

for f in listdir('images'):
    outputJSON.append({'source-ref': f})

#print(outputJSON)

with jsonlines.open('manifest.json', 'w') as outfile:
    outfile.write_all(outputJSON)
