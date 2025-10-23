#!/bin/bash

# Adventist Health Registration System - Test Script
# This script tests all API endpoints to verify the system is working correctly

# Configuration
BASE_URL="https://your-domain.vercel.app"  # Replace with your actual Vercel domain
ADMIN_KEY="your-admin-key"  # Replace with your actual admin key

echo "🧪 Testing Adventist Health Registration System"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local expected_status="$2"
    local curl_command="$3"
    
    echo -n "Testing $test_name... "
    
    # Run the curl command and capture the response
    response=$(eval "$curl_command" 2>/dev/null)
    status_code=$(eval "$curl_command" -w "%{http_code}" -o /dev/null -s 2>/dev/null)
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected: $expected_status, Got: $status_code)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "Response: $response"
    fi
    echo ""
}

# Test 1: Registration - Success
run_test "Registration (Success)" "201" \
"curl -X POST $BASE_URL/api/register \
  -H 'Content-Type: application/json' \
  -d '{
    \"name\": \"Dr. Test User\",
    \"email\": \"test@example.com\",
    \"hospital\": \"Test Hospital\",
    \"role\": \"Doctor\",
    \"specialty\": \"General Medicine\",
    \"bio\": \"Test bio for verification\"
  }'"

# Test 2: Registration - Duplicate Email
run_test "Registration (Duplicate Email)" "409" \
"curl -X POST $BASE_URL/api/register \
  -H 'Content-Type: application/json' \
  -d '{
    \"name\": \"Dr. Test User\",
    \"email\": \"test@example.com\",
    \"hospital\": \"Another Hospital\",
    \"role\": \"Doctor\"
  }'"

# Test 3: Registration - Validation Error
run_test "Registration (Validation Error)" "400" \
"curl -X POST $BASE_URL/api/register \
  -H 'Content-Type: application/json' \
  -d '{
    \"name\": \"\",
    \"email\": \"invalid-email\",
    \"hospital\": \"\",
    \"role\": \"\"
  }'"

# Test 4: Get Approved
run_test "Get Approved" "200" \
"curl -s $BASE_URL/api/getApproved"

# Test 5: Get Pending - No Admin Key
run_test "Get Pending (No Admin Key)" "401" \
"curl -s $BASE_URL/api/getPending"

# Test 6: Get Pending - With Admin Key
run_test "Get Pending (With Admin Key)" "200" \
"curl -s $BASE_URL/api/getPending \
  -H 'x-admin-key: $ADMIN_KEY'"

# Test 7: Update Status - No Admin Key
run_test "Update Status (No Admin Key)" "401" \
"curl -X POST $BASE_URL/api/updateStatus \
  -H 'Content-Type: application/json' \
  -d '{
    \"email\": \"test@example.com\",
    \"status\": \"approved\"
  }'"

# Test 8: Update Status - With Admin Key
run_test "Update Status (With Admin Key)" "200" \
"curl -X POST $BASE_URL/api/updateStatus \
  -H 'Content-Type: application/json' \
  -H 'x-admin-key: $ADMIN_KEY' \
  -d '{
    \"email\": \"test@example.com\",
    \"status\": \"approved\",
    \"notes\": \"Approved for testing\"
  }'"

# Test 9: Get Approved - After Approval
run_test "Get Approved (After Approval)" "200" \
"curl -s $BASE_URL/api/getApproved"

# Test 10: Update Status - Not Found
run_test "Update Status (Not Found)" "404" \
"curl -X POST $BASE_URL/api/updateStatus \
  -H 'Content-Type: application/json' \
  -H 'x-admin-key: $ADMIN_KEY' \
  -d '{
    \"email\": \"nonexistent@example.com\",
    \"status\": \"approved\"
  }'"

# Summary
echo "=============================================="
echo "Test Results Summary:"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Your system is working correctly.${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please check the configuration and try again.${NC}"
    echo ""
    echo "Common issues:"
    echo "1. Update BASE_URL with your actual Vercel domain"
    echo "2. Update ADMIN_KEY with your actual admin key"
    echo "3. Ensure environment variables are set correctly"
    echo "4. Verify Google Sheets API is working"
    exit 1
fi
