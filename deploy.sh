#!/bin/bash
# Install serverless plugins
npm install --save-dev serverless-python-requirements

# Deploy to AWS
serverless deploy --stage prod 