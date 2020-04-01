# Sagemaker GroundTruth Demo

## Instructions

### Upload demo tennis images + Create/upload manifest
1. Install virtualenv
- virtualenv groundtruth-demo
- source groundtruth-demo/bin/activate
2. Install pip requirements
- pip install -r requirements.txt
3. Run setup to upload images and manifest
- python setup.py

### Configure Cognito [TODO]
1. Launch CFN template for Cognito
- aws cloudformation deploy --template-file cfn/core.yml --stack-name groundtruth-demo-core
  - This will create a bare Cognito User Pool with no Oauth set up yet

### Configure Okta
Go to old console
create application

Check CFN Outputs
- get SSODomain and AudienceURL
- Put those into SSO URL, Audience URI

Attribute statements:
Name: http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
Value: user.email

Next

Internal

Copy link of Identity Provider Metadata

### Update CFN
- Update OktaMetadataURL with above link
- aws cloudformation deploy --template-file cfn/core-updated.yml --stack-name groundtruth-demo-core

### Create GT Job
- upload lambda for CFN custom resource
- pip install -r lambda/requirements.txt --target lambda
- cd lambda && zip -r9 ../createjob-lambda.zip . && cd ..
- aws s3 cp createjob-lambda.zip s3://huberttest-pdx/createjob-lambda.zip
- aws cloudformation deploy --template-file cfn/createjob-cfn.yml --stack-name groundtruth-demo-job-2 --capabilities CAPABILITY_IAM

### Update CallbackURL in Cognito
- Do describe on workteam

### Create Bookmark



## Reset Instructions
1. ./reset.sh
2. Delete CFN stack


## Misc notes...
Disable cognito user pool auth <-- enabling this will allow logout to work
remove /saml2/idpresponse
add just the sm domain to the cognito callback url section
add bookmark for ^

CFN steps
- create Cognito User Pool
- Create workteam
- create labeling job
