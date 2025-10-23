#!/bin/bash

# Environment Variables Setup Script
# Run this script to set up all required environment variables

echo "🔧 Setting up Environment Variables for Adventist Health Registration System"
echo "========================================================================"
echo ""

echo "You need to set up these environment variables in Vercel:"
echo ""
echo "1. SPREADSHEET_ID"
echo "   - Get this from your Google Sheet URL"
echo "   - Format: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit"
echo ""
echo "2. GOOGLE_SERVICE_ACCOUNT"
echo "   - This is the full JSON content from your service account file"
echo "   - Copy the entire JSON as a single line string"
echo ""
echo "3. ADMIN_API_KEY"
echo "   - Generate a secure random string"
echo "   - Example: $(openssl rand -hex 32)"
echo ""

echo "Setting up environment variables..."
echo ""

# Set SPREADSHEET_ID
echo "Setting SPREADSHEET_ID..."
echo "Enter your Google Sheet ID (from the URL):"
read -p "SPREADSHEET_ID: " SPREADSHEET_ID
vercel env add SPREADSHEET_ID production <<< "$SPREADSHEET_ID"

echo ""
echo "Setting GOOGLE_SERVICE_ACCOUNT..."
echo "Paste your service account JSON (the entire content as one line):"
read -p "GOOGLE_SERVICE_ACCOUNT: " GOOGLE_SERVICE_ACCOUNT
vercel env add GOOGLE_SERVICE_ACCOUNT production <<< "$GOOGLE_SERVICE_ACCOUNT"

echo ""
echo "Setting ADMIN_API_KEY..."
ADMIN_KEY=$(openssl rand -hex 32)
echo "Generated admin key: $ADMIN_KEY"
vercel env add ADMIN_API_KEY production <<< "$ADMIN_KEY"

echo ""
echo "✅ Environment variables set successfully!"
echo ""
echo "Your admin key is: $ADMIN_KEY"
echo "Save this key - you'll need it to access the admin panel!"
echo ""
echo "Now you can deploy with: vercel --prod --yes"
