from __future__ import print_function
import boto3
import logging
import json
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3Client = boto3.client('s3')
smClient = boto3.client('sagemaker')

def lambda_handler(event, context):
    logger.debug('Event: {}'.format(event))
    logger.debug('Context: {}'.format(context))
    responseData = {}

    # Define some variables for creating folders and such
    now = datetime.now()
    timePrefix = now.strftime("%d-%m-%Y-%H-%M-%S")

    LabelCategoryConfigFileName = 'LabelCategoryConfig.json'
    LabelCategoryConfigLocalPath = '/tmp'
    LabelCategoryConfigS3Bucket = 'huberttest-pdx'
    LabelCategoryConfigS3Path = 'sm-groundtruth'
    LabelJobName = 'LabelingJob-'+timePrefix
    LabelJobTitle = LabelJobName

    LabelJobOutputPath = 's3://'+LabelCategoryConfigS3Bucket+'/'+LabelCategoryConfigS3Path+'/output/'
    # LabelJobUiTemplatePath = LabelJobOutputPath+LabelJobName+'/annotation-tool/template.liquid'
    LabelJobUiTemplatePath = LabelJobOutputPath+'cfn-testing/annotation-tool/template.liquid'


    localFile = open(LabelCategoryConfigLocalPath+'/'+LabelCategoryConfigFileName, "w")
    localFile.write('''
        {
            "document-version": "2018-11-28",
            "labels": [
                {
                    "label": "Tennis!"
                },
                {
                    "label": "Not Tennis!"
                },
                {
                    "label": "A boat"
                }
            ]
        }'''
    )

    localFile.close()

    try:
        response = s3Client.upload_file(LabelCategoryConfigLocalPath+'/'+LabelCategoryConfigFileName, LabelCategoryConfigS3Bucket, LabelCategoryConfigS3Path+"/"+LabelCategoryConfigFileName)
    except ClientError as e:
        logging.error(e)

    #
    # f=open("/tmp/LabelCategoryConfig.json", "r")
    # print(f.read())

    response = smClient.create_labeling_job(
        LabelingJobName=LabelJobName,
        LabelAttributeName='TennisOrNot',
        InputConfig={
            'DataSource': {
                'S3DataSource': {
                    'ManifestS3Uri': 's3://huberttest-pdx/sm-groundtruth/manifest.json'
                }
            }
        },
        OutputConfig={
            'S3OutputPath': LabelJobOutputPath
            # 'KmsKeyId': 'string'
        },
        RoleArn='arn:aws:iam::521243010531:role/service-role/AmazonSageMaker-ExecutionRole-20200303T135454',
        LabelCategoryConfigS3Uri='s3://'+LabelCategoryConfigS3Bucket+'/'+LabelCategoryConfigS3Path+'/'+LabelCategoryConfigFileName,
        HumanTaskConfig={
            'WorkteamArn': 'arn:aws:sagemaker:us-west-2:521243010531:workteam/private-crowd/SageMakerDefaultWorkTeam-dOunDRSoTSKd',
            'UiConfig': {
                'UiTemplateS3Uri': LabelJobUiTemplatePath
            },
            'PreHumanTaskLambdaArn': 'arn:aws:lambda:us-west-2:081040173940:function:PRE-ImageMultiClass',
            # 'TaskKeywords': [
            #     'string',
            # ],
            'TaskTitle': LabelJobTitle,
            'TaskDescription': 'Some Cool Description',
            'NumberOfHumanWorkersPerDataObject': 1,
            'TaskTimeLimitInSeconds': 600,
            # 'TaskAvailabilityLifetimeInSeconds': 123,
            # 'MaxConcurrentTaskCount': 123,
            'AnnotationConsolidationConfig': {
                'AnnotationConsolidationLambdaArn': 'arn:aws:lambda:us-west-2:081040173940:function:ACS-ImageMultiClass'
            }
        },
        LabelingJobAlgorithmsConfig={
            'LabelingJobAlgorithmSpecificationArn': 'arn:aws:sagemaker:us-west-2:027400017018:labeling-job-algorithm-specification/image-classification',
            # 'InitialActiveLearningModelArn': 'string',
            # 'LabelingJobResourceConfig': {
            #     'VolumeKmsKeyId': 'string'
            # }
        }
    )
    print(response)
