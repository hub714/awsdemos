#!/bin/bash

aws s3 rm --recursive s3://huberttest/sm-groundtruth

#aws s3 sync images/ s3://huberttest/sm-groundtruth/images --acl public-read
