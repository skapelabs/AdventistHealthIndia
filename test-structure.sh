#!/bin/bash

# Quick API Structure Test
# This script verifies that all API files are properly structured

echo "🔍 Testing API Structure..."
echo "=========================="

# Check if all required files exist
files=(
    "api/register.js"
    "api/getApproved.js" 
    "api/getPending.js"
    "api/updateStatus.js"
    "api/utils/sheets.js"
    "package.json"
    "vercel.json"
)

echo "Checking required files..."
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

echo ""
echo "Checking API file structure..."

# Check if API files export default functions
for api_file in api/*.js; do
    if grep -q "export default" "$api_file"; then
        echo "✅ $api_file has default export"
    else
        echo "❌ $api_file missing default export"
    fi
done

# Check if utils file exports functions
if grep -q "export function" api/utils/sheets.js; then
    echo "✅ utils/sheets.js exports functions"
else
    echo "❌ utils/sheets.js missing function exports"
fi

echo ""
echo "Checking package.json dependencies..."
if grep -q "googleapis" package.json && grep -q "uuid" package.json; then
    echo "✅ Required dependencies found"
else
    echo "❌ Missing required dependencies"
fi

echo ""
echo "Checking Vercel configuration..."
if grep -q "nodejs18.x" vercel.json; then
    echo "✅ Vercel runtime configured"
else
    echo "❌ Vercel runtime not configured"
fi

echo ""
echo "🎉 API structure test complete!"
echo ""
echo "Next steps:"
echo "1. Run: vercel login"
echo "2. Run: vercel --prod --yes"
echo "3. Test endpoints with curl commands"
echo "4. Verify Google Sheets integration"
