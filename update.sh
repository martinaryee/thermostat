#!/bin/bash

export AWS_ACCESS_KEY_ID=AKIAJ6OL6GHIOAX3OTJA
export AWS_SECRET_ACCESS_KEY=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

/usr/bin/python log_sensor_values.py
Rscript report.R
aws s3 cp temperature.svg s3://home-342 

