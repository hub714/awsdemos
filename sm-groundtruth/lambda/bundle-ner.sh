#!/bin/bash
cd createjob-ner/packages
zip -r9 ../../createjob-ner.zip .
cd ..
zip -r9 ../createjob-ner.zip . -x "*packages*"
cd ..
aws s3 cp createjob-ner.zip s3://huberttest-pdx/createjob-ner.zip
