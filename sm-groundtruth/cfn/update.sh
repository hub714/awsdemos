#!/bin/bash

aws cloudformation update-stack --stack-name "groundtruth-test" --region us-west-2 --template-body file://core.yml
