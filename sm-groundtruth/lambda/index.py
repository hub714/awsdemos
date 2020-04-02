from __future__ import print_function
import boto3
import logging
import json
import cfnresponse
import traceback
# from cfnresponse import send
from datetime import datetime
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(event['ResourceProperties'])

    logger.debug('Event: {}'.format(event))
    logger.debug('Context: {}'.format(context))
    responseData = {}

    s3Client = boto3.client('s3')
    smClient = boto3.client('sagemaker')

    # Define some variables for creating folders and such
    now = datetime.now()
    timePrefix = now.strftime("%d-%m-%Y-%H-%M-%S")

    # To parameterize later based off event
    # First, pull in parameters from CloudFormation event

    # Arn for work team created in core template
    assignedWorkTeam = event['ResourceProperties']['WorkTeamArn']

    # Arn for sagemaker execution role
    smExecutionRole = event['ResourceProperties']['SageMakerExecutionRole']

    # Attribute name for labelling
    labelAttributeName = event['ResourceProperties']['LabelAttributeName']
    s3ManifestURI = event['ResourceProperties']['S3ManifestURI']

    # Get S3 bucket that we will be storing data. This determines output as well as looks for some manifest info
    LabelCategoryConfigS3Bucket = event['ResourceProperties']['LabelingS3Bucket']
    LabelCategoryConfigFileName = 'LabelCategoryConfig.json'
    LabelCategoryConfigLocalPath = '/tmp'
    LabelCategoryConfigS3Path = 'sm-groundtruth'
    LabelJobName = 'LabelingJob-'+timePrefix
    LabelJobTitle = LabelJobName

    LabelJobOutputPath = 's3://'+LabelCategoryConfigS3Bucket+'/'+LabelCategoryConfigS3Path+'/output/'
    LabelJobUiTemplatePath = LabelJobOutputPath+'cfn-testing/annotation-tool/template.liquid'

    # Immediately respond on Delete
    if event['RequestType'] == 'Delete':
        try:
            cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            logger.error(e, exc_info=True)
            responseData = {'Error': str(e)}
            cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')

    if event['RequestType'] == 'Update':
        try:
            cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            logger.error(e, exc_info=True)
            responseData = {'Error': str(e)}
            cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')

    if event['RequestType'] == 'Create':
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

            response = smClient.create_labeling_job(
                LabelingJobName=LabelJobName,
                LabelAttributeName=labelAttributeName,
                InputConfig={
                    'DataSource': {
                        'S3DataSource': {
                            'ManifestS3Uri': s3ManifestURI
                        }
                    }
                },
                OutputConfig={
                    'S3OutputPath': LabelJobOutputPath
                    # 'KmsKeyId': 'string'
                },
                RoleArn=smExecutionRole,
                LabelCategoryConfigS3Uri='s3://'+LabelCategoryConfigS3Bucket+'/'+LabelCategoryConfigS3Path+'/'+LabelCategoryConfigFileName,
                HumanTaskConfig={
                    'WorkteamArn': assignedWorkTeam,
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
            responseData = {'Success': 'Role added to instance.'}
            cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            logger.error(e, exc_info=True)
            responseData = {'Error': str(e)}
            cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')