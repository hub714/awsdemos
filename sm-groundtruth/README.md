# Sagemaker GroundTruth Demo

## Instructions

### Upload demo tennis images
1. Install virtualenv
2. virtualenv groundtruth-demo
3. source groundtruth-demo/bin/activate
4. pip install -r requirements.txt
5. python setup.py

### Configure GroundTruth
1. Launch CFN template
2.

## Reset Instructions
1. ./reset.sh
2. Delete CFN stack



Disable cognito user pool auth <-- enabling this will allow logout to work
remove /saml2/idpresponse
add just the sm domain to the cognito callback url section
add bookmark for ^

CFN steps
- create Cognito User Pool
- Create workteam
- create labeling job
