#!/bin/bash

# Read the service account JSON and set it as environment variable
SERVICE_ACCOUNT_JSON=$(cat /Users/pranjaldubey/Downloads/adventist-476010-008951d91aac.json)

# Set the environment variable
echo "$SERVICE_ACCOUNT_JSON" | vercel env add GOOGLE_SERVICE_ACCOUNT production
