# Sagemaker GroundTruth Demo

## Instructions

The purpose of this demo is to show how one could initiate a flow from the Okta console and eventually get into Sagemaker GroundTruth.

### Upload demo tennis images + Create/upload manifest

This first section is only necessary if you do not already have images and a manifest file. Effectively, it will just take the images folder, upload them to a bucket, create a manifest file, and upload that as well. SM GroundTruth will use the manifest file to create the actual labeling job later on.

1. Set up Python 3.7 working environment with virtualenv
First of all, to keep your laptop clean, I used virtualenv. Install it using pip or anything else you might like and create the venv:
```
<<<<<<< HEAD
$ virtualenv groundtruth-demo
$ source groundtruth-demo/bin/activate
=======
- virtualenv groundtruth-demo
- source groundtruth-demo/bin/activate
>>>>>>> c94a9b820f9528fe86ee9db4e1c4730ed981d599
```

2. Install pip requirements
The setup.py script has a number of requirements: boto, jsonlines, etc. First, install the dependencies:
```
$ pip install -r requirements.txt
```

3. Run setup to upload images and manifest
The python file currently has hard coded values for an S3 bucket and the path in lines 8 and 9. Feel free to change these but note that you will also need to update the custom resource index.py later.
```
$ python setup.py
```

### Configure Cognito [TODO]
1. Launch CFN template for Cognito
- aws cloudformation deploy --template-file cfn/core.yml --stack-name groundtruth-demo-core --parameter-override "DefaultGroupName=English_default" --capabilities CAPABILITY_IAM
  - This will create a bare Cognito User Pool with no Oauth set up yet

### Configure Okta
Go to old console
create application
- Web
- SAML 2.0

- tick Do not display application icon to users
- Do not display application icon in the Okta Mobile app

Check CFN Outputs
- get SSODomain and AudienceURL
- Put those into SSO URL, Audience URI
- Name ID Format: EmailAddress

Attribute statements:
- Name: http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
Value: user.email

- Copy link of Identity Provider Metadata

### Get Labeling endpoint
- Go to [Sagemaker console - Labeling workforces](https://us-west-2.console.aws.amazon.com/sagemaker/groundtruth?region=us-west-2#/labeling-workforces)
  - Private workforce
  - Copy labeling portal sign-in url

### Update CFN
- Update OktaMetadataURL with above link
- Update labeling endpoint in cfn via parameter
- aws cloudformation deploy --template-file cfn/core-updated.yml --stack-name groundtruth-demo-core --parameter-overrides "LabelingEndpoint=https://z182d0xam0.labeling.us-west-2.sagemaker.aws" "OktaMetadataURL=https://dev-642335.okta.com/app/exk595x0hpOQf6Wgl4x6/sso/saml/metadata" "DefaultGroupName=English_default" --capabilities CAPABILITY_IAM

### Create Bookmark
- Look @ the Bookmark URL in outputs and copy/paste

Add people to both bookmark and app

### Create GT Job
- upload lambda for CFN custom resource
- pip install -r lambda/requirements.txt --target lambda/packages
- cd lambda/packages && zip -r9 ../../createjob-lambda.zip . && cd .. && zip -r9 ../createjob-lambda.zip . -x "*packages*" && cd .. && aws s3 cp createjob-lambda.zip s3://huberttest-pdx/createjob-lambda.zip
- aws cloudformation deploy --template-file cfn/createjob-cfn.yml --stack-name groundtruth-demo-job-6 --capabilities CAPABILITY_IAM

### Test Access
- Go to Okta in new incognito tab
- Click bookmark

<!-- ## Reset Instructions
1. ./reset.sh
2. Delete CFN stack -->

## Flow if you dont need Okta

- aws cloudformation deploy --template-file cfn/core.yml --stack-name groundtruth-demo-core --parameter-override "DefaultGroupName=English_default" --capabilities CAPABILITY_IAM

- aws cloudformation deploy --template-file cfn/core-nookta.yml --stack-name groundtruth-demo-core --parameter-overrides "LabelingEndpoint=https://z182d0xam0.labeling.us-west-2.sagemaker.aws" "DefaultGroupName=English_default" --capabilities CAPABILITY_IAM

aws cloudformation deploy --template-file cfn/createjob-cfn.yml --stack-name groundtruth-demo-job-6 --capabilities CAPABILITY_IAM



### ToDo:
Custom resource to modify Cognito User Pool after Lambda is created

## Misc notes...
Disable cognito user pool auth <-- enabling this will allow logout to work
remove /saml2/idpresponse
add just the sm domain to the cognito callback url section
add bookmark for ^

CFN steps
- create Cognito User Pool
- Create workteam
- create labeling job
