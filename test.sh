#!/bin/bash

if [[ $# != 1 ]]; then
  echo "Usage $0 <mail_type>"
  exit 1
fi

MAIL_TYPE=$1

source .env.local
envsubst <  "${MAIL_TYPE}_event.json" > "${MAIL_TYPE}.json"
python3 lambda_function.py "${MAIL_TYPE}"
