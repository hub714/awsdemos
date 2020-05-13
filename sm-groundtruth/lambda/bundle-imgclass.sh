#!/bin/bash
cd createjob-imgclass/packages
zip -r9 ../../createjob-imgclass.zip .
cd ..
zip -r9 ../createjob-imgclass.zip . -x "*packages*"
cd ..
aws s3 cp createjob-imgclass.zip s3://huberttest-pdx/createjob-imgclass.zip
