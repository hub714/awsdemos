#!/bin/bash

# aws cloudformation create-stack --stack-name "groundtruth-test" --region us-east-1 --template-body file://core.yml

aws cloudformation create-stack --stack-name "groundtruth-test" --region us-west-2 --template-body file://core.yml
