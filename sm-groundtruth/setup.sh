#!/bin/bash

aws s3 rm --recursive s3://huberttest/sm-groundtruth

aws s3 sync ../sm-groundtruth s3://huberttest/sm-groundtruth --acl public-read
