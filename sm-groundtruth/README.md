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
- Web
- SAML 2.0

Check CFN Outputs
- get SSODomain and AudienceURL
- Put those into SSO URL, Audience URI
- Name ID Format: EmailAddress

Attribute statements:
- Name: http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
Value: user.email

Next

Internal

Copy link of Identity Provider Metadata

### Update CallbackURL in Cognito
- Do describe on workteam

### Update CFN
- Update OktaMetadataURL with above link
- Update labeling endpoint in cfn
- aws cloudformation deploy --template-file cfn/core-updated.yml --stack-name groundtruth-demo-core --parameter-overrides "LabelingEndpoint=https://z182d0xam0.labeling.us-west-2.sagemaker.aws" "OktaMetadataURL=https://dev-642335.okta.com/app/exk57wzajs2Jst0oh4x6/sso/saml/metadata"

### Create Bookmark
- Look @ the Bookmark URL in outputs and copy/paste

Add people to both bookmark and app

### Create GT Job
- upload lambda for CFN custom resource
- pip install -r lambda/requirements.txt --target lambda/packages
- cd lambda/packages && zip -r9 ../../createjob-lambda.zip . && cd .. && zip -r9 ../createjob-lambda.zip . -x "*packages*" && cd .. && aws s3 cp createjob-lambda.zip s3://huberttest-pdx/createjob-lambda.zip && aws cloudformation deploy --template-file cfn/createjob-cfn.yml --stack-name groundtruth-demo-job-5 --capabilities CAPABILITY_IAM

## Reset Instructions
1. ./reset.sh
2. Delete CFN stack


## Todo:
- Create lambda for auto-add to group
- Update lambda to use cfn params

## Misc notes...
Disable cognito user pool auth <-- enabling this will allow logout to work
remove /saml2/idpresponse
add just the sm domain to the cognito callback url section
add bookmark for ^

CFN steps
- create Cognito User Pool
- Create workteam
- create labeling job
