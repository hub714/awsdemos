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
    print(event)
    print(event['ResourceProperties'])

    logger.debug('Event: {}'.format(event))
    logger.debug('Context: {}'.format(context))
    responseData = {}

    cfnClient = boto3.client('cloudformation')

    # CloudFormation custom resouces will send a RequestType of Delete, Update, or Create to Lambda. We need to figure out what it is and do something based on the specific request.
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
        try:
            response = cfnClient.describe_stacks(
                StackName=event['StackId']
            )
            tags = response['Stacks'][0]['Tags']

            for tag in tags:
                if 'provisioningPrincipalArn' in tag['Key']:
                    provisioningPrincipalArn = tag['Value']
                    provisioningPrincipal = provisioningPrincipalArn.split("/")[2]


            responseData = {'Success': 'Got provisioningPrincipal.', 'Username': provisioningPrincipal}
            cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            logger.error(e, exc_info=True)
            responseData = {'Error': str(e)}
            cfnresponse.send(event, context, cfnresponse.FAILED, responseData, 'CustomResourcePhysicalID')
