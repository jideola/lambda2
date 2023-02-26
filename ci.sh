#!/bin/bash

# Get current date and time
when=$(date +%y%m%d%H%M%S)
echo -e "new time is $when"
# Set new output path

echo "variable \"output_path\" { default = \"cloudwatch_lambda-$when.zip\" }" > input.tf
echo "variable \"function_name\" { default = \"cw_to_slack-$when\" }" >> input.tf
