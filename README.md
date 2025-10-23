# Adventist Health India - Registration System

A production-ready, serverless registration system built with Vercel Functions and Google Sheets API. Healthcare professionals can register, and admins can approve/reject registrations through a simple interface.

## 🚀 Quick Start

This system can be deployed and tested within 20 minutes following these steps:

### 1. Prerequisites

- Node.js 18+ installed
- Vercel CLI installed (`npm i -g vercel`)
- Google account for Sheets API
- Git repository (optional, for version control)

### 2. Google Sheets Setup

#### Create the Spreadsheet

1. **Create a new Google Sheet** with the exact structure below:

**Sheet Name: `Registrations`**
```
| id | name | email | hospital | role | specialty | bio | submitted_at | status | status_updated_at | notes |
|----|------|-------|----------|------|-----------|-----|--------------|--------|-------------------|-------|
| uuid-123 | Dr. John Smith | john@hospital.com | City Hospital | Doctor | Cardiology | Experienced cardiologist... | 2024-01-15T10:30:00Z | approved | 2024-01-16T09:15:00Z | Approved after review |
```

**Sheet Name: `AdminLogs`**
```
| log_id | action | target_id | admin_key_used | timestamp | notes |
|--------|--------|-----------|----------------|-----------|-------|
| log-uuid-456 | update_status | uuid-123 | admin_key_used | 2024-01-16T09:15:00Z | Approved after review |
```

#### Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Google Sheets API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Fill in details:
   - Name: `adventist-health-sheets`
   - Description: `Service account for Adventist Health registration system`
6. Click **Create and Continue**
7. Skip role assignment (click **Continue**)
8. Click **Done**
9. Click on the created service account
10. Go to **Keys** tab → **Add Key** → **Create New Key** → **JSON**
11. Download the JSON file (keep it secure!)

#### Share the Spreadsheet

1. Open your Google Sheet
2. Click **Share** button
3. Add the service account email (found in the JSON file as `client_email`)
4. Give **Editor** permissions
5. Click **Send**

### 3. Environment Variables

Set these environment variables in Vercel:

```bash
# Required
SPREADSHEET_ID="your-spreadsheet-id-from-url"
GOOGLE_SERVICE_ACCOUNT='{"type":"service_account","project_id":"..."}' # Full JSON as string
ADMIN_API_KEY="your-secure-random-admin-key"

# Optional
VERCEL_ENV="production"
```

#### How to Set Environment Variables in Vercel:

1. **Via CLI:**
   ```bash
   vercel env add SPREADSHEET_ID
   vercel env add GOOGLE_SERVICE_ACCOUNT
   vercel env add ADMIN_API_KEY
   ```

2. **Via Dashboard:**
   - Go to your project in Vercel dashboard
   - Settings → Environment Variables
   - Add each variable

#### Important Notes:

- **SPREADSHEET_ID**: Extract from your Google Sheet URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
- **GOOGLE_SERVICE_ACCOUNT**: Paste the entire JSON content as a single-line string
- **ADMIN_API_KEY**: Generate a secure random string (e.g., `openssl rand -hex 32`)

### 4. Deploy to Vercel

```bash
# Install dependencies
npm install

# Deploy to Vercel
vercel

# Follow the prompts:
# - Link to existing project? N
# - Project name: adventist-health-registration
# - Directory: ./
# - Override settings? N
```

### 5. Test the Deployment

After deployment, test each endpoint:

```bash
# Test registration
curl -X POST https://your-domain.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Test User",
    "email": "test@example.com",
    "hospital": "Test Hospital",
    "role": "Doctor",
    "specialty": "General Medicine",
    "bio": "Test bio for verification"
  }'

# Test get approved (should return empty initially)
curl https://your-domain.vercel.app/api/getApproved

# Test get pending (requires admin key)
curl https://your-domain.vercel.app/api/getPending \
  -H "x-admin-key: your-admin-key"

# Test update status
curl -X POST https://your-domain.vercel.app/api/updateStatus \
  -H "Content-Type: application/json" \
  -H "x-admin-key: your-admin-key" \
  -d '{
    "email": "test@example.com",
    "status": "approved",
    "notes": "Approved for testing"
  }'
```

## 📁 Project Structure

```
├── api/
│   ├── register.js          # POST /api/register
│   ├── getApproved.js       # GET /api/getApproved
│   ├── getPending.js        # GET /api/getPending
│   ├── updateStatus.js      # POST /api/updateStatus
│   └── utils/
│       └── sheets.js        # Google Sheets utilities
├── register.html            # Registration form
├── directory.html           # Public directory
├── admin.html               # Admin panel
├── package.json             # Dependencies
├── vercel.json              # Vercel configuration
└── README.md                # This file
```

## 🔧 API Endpoints

### POST /api/register

Register a new healthcare professional.

**Request Body:**
```json
{
  "name": "string (required)",
  "email": "string (required)",
  "hospital": "string (required)",
  "role": "string (required)",
  "specialty": "string (optional)",
  "bio": "string (optional)"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-123",
    "name": "Dr. John Smith",
    "email": "john@hospital.com",
    "hospital": "City Hospital",
    "role": "Doctor",
    "specialty": "Cardiology",
    "bio": "Experienced cardiologist...",
    "submitted_at": "2024-01-15T10:30:00Z",
    "status": "pending",
    "status_updated_at": "",
    "notes": ""
  },
  "message": "Registration submitted successfully"
}
```

**Error Responses:**
- `400` - Validation failed
- `409` - Duplicate email
- `500` - Server error

### GET /api/getApproved

Get all approved professionals with pagination.

**Query Parameters:**
- `limit` (optional): Number of results (1-100, default: 50)
- `offset` (optional): Starting position (default: 0)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid-123",
      "name": "Dr. John Smith",
      "email": "john@hospital.com",
      "hospital": "City Hospital",
      "role": "Doctor",
      "specialty": "Cardiology",
      "bio": "Experienced cardiologist...",
      "submitted_at": "2024-01-15T10:30:00Z",
      "status": "approved",
      "status_updated_at": "2024-01-16T09:15:00Z",
      "notes": "Approved after review"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "hasMore": false
  }
}
```

### GET /api/getPending

Get all pending registrations (admin only).

**Headers:**
- `x-admin-key`: Your admin API key

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid-456",
      "name": "Dr. Jane Doe",
      "email": "jane@clinic.com",
      "hospital": "Community Clinic",
      "role": "Nurse",
      "specialty": "Pediatrics",
      "bio": "Pediatric nurse with 5 years experience...",
      "submitted_at": "2024-01-15T14:20:00Z",
      "status": "pending",
      "status_updated_at": "",
      "notes": ""
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "hasMore": false
  }
}
```

**Error Responses:**
- `401` - Invalid admin key
- `500` - Server error

### POST /api/updateStatus

Update registration status (admin only).

**Headers:**
- `x-admin-key`: Your admin API key

**Request Body:**
```json
{
  "id": "string (optional)",
  "email": "string (optional)",
  "status": "approved|rejected",
  "notes": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-456",
    "name": "Dr. Jane Doe",
    "email": "jane@clinic.com",
    "hospital": "Community Clinic",
    "role": "Nurse",
    "specialty": "Pediatrics",
    "bio": "Pediatric nurse with 5 years experience...",
    "submitted_at": "2024-01-15T14:20:00Z",
    "status": "approved",
    "status_updated_at": "2024-01-16T10:45:00Z",
    "notes": "Approved after verification"
  },
  "message": "Registration approved successfully"
}
```

**Error Responses:**
- `400` - Invalid request
- `401` - Invalid admin key
- `404` - Registration not found
- `500` - Server error

## 🧪 Testing Guide

### Complete Test Matrix

Run these tests in order to verify all functionality:

#### 1. Registration Tests

```bash
# Test successful registration
curl -X POST https://your-domain.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Alice Johnson",
    "email": "alice@test.com",
    "hospital": "Test Medical Center",
    "role": "Doctor",
    "specialty": "Internal Medicine",
    "bio": "Board-certified internal medicine physician"
  }'

# Expected: 201 Created with registration data

# Test duplicate email
curl -X POST https://your-domain.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Alice Johnson",
    "email": "alice@test.com",
    "hospital": "Another Hospital",
    "role": "Doctor"
  }'

# Expected: 409 Conflict with duplicate email error

# Test validation errors
curl -X POST https://your-domain.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "",
    "email": "invalid-email",
    "hospital": "",
    "role": ""
  }'

# Expected: 400 Bad Request with validation errors
```

#### 2. Get Approved Tests

```bash
# Test get approved (initially empty)
curl https://your-domain.vercel.app/api/getApproved

# Expected: 200 OK with empty data array

# Test pagination
curl "https://your-domain.vercel.app/api/getApproved?limit=10&offset=0"

# Expected: 200 OK with pagination info
```

#### 3. Admin Tests

```bash
# Test get pending without admin key
curl https://your-domain.vercel.app/api/getPending

# Expected: 401 Unauthorized

# Test get pending with invalid admin key
curl https://your-domain.vercel.app/api/getPending \
  -H "x-admin-key: invalid-key"

# Expected: 401 Unauthorized

# Test get pending with valid admin key
curl https://your-domain.vercel.app/api/getPending \
  -H "x-admin-key: your-actual-admin-key"

# Expected: 200 OK with pending registrations

# Test update status without admin key
curl -X POST https://your-domain.vercel.app/api/updateStatus \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@test.com",
    "status": "approved"
  }'

# Expected: 401 Unauthorized

# Test update status with valid admin key
curl -X POST https://your-domain.vercel.app/api/updateStatus \
  -H "Content-Type: application/json" \
  -H "x-admin-key: your-actual-admin-key" \
  -d '{
    "email": "alice@test.com",
    "status": "approved",
    "notes": "Approved after verification"
  }'

# Expected: 200 OK with updated registration

# Test get approved after approval
curl https://your-domain.vercel.app/api/getApproved

# Expected: 200 OK with the approved registration
```

### Frontend Testing

1. **Registration Form**: Visit `/register.html` and submit a test registration
2. **Directory**: Visit `/directory.html` to see approved professionals
3. **Admin Panel**: Visit `/admin.html` and test the approval workflow

## 🔒 Security Considerations

### Current Security Measures

- **Admin Key Protection**: Admin endpoints require valid `x-admin-key` header
- **Input Validation**: All inputs are validated server-side
- **CORS Headers**: Properly configured for frontend requests
- **Error Handling**: No sensitive information leaked in error messages

### Recommended Additional Security

For production use, consider:

1. **Rate Limiting**: Implement per-IP rate limiting on registration endpoint
2. **Input Sanitization**: Additional sanitization for bio fields
3. **Audit Logging**: Enhanced logging for all admin actions
4. **HTTPS Only**: Ensure all requests use HTTPS
5. **Admin Key Rotation**: Regular rotation of admin API keys

## 🚨 Troubleshooting

### Common Issues

#### 1. Google Sheets API Errors

**Error**: `403 Forbidden` or `Authentication failed`

**Solutions**:
- Verify service account JSON is correctly formatted
- Ensure spreadsheet is shared with service account email
- Check that Google Sheets API is enabled in Google Cloud Console
- Verify `GOOGLE_SERVICE_ACCOUNT` environment variable is set correctly

#### 2. Spreadsheet Not Found

**Error**: `404 Not Found` when accessing spreadsheet

**Solutions**:
- Verify `SPREADSHEET_ID` is correct (extract from URL)
- Ensure spreadsheet exists and is accessible
- Check that service account has Editor permissions

#### 3. Rate Limiting

**Error**: `429 Too Many Requests`

**Solutions**:
- Google Sheets API has quotas (100 requests per 100 seconds per user)
- Implement exponential backoff in your application
- Consider caching approved registrations

#### 4. Environment Variables

**Error**: `Service configuration error`

**Solutions**:
- Verify all required environment variables are set in Vercel
- Check that `GOOGLE_SERVICE_ACCOUNT` is a valid JSON string
- Ensure `ADMIN_API_KEY` is set and matches what you're using

#### 5. CORS Issues

**Error**: CORS errors in browser console

**Solutions**:
- Verify CORS headers are set correctly in API functions
- Check that frontend is served from the same domain
- Test with `curl` to isolate CORS vs API issues

### Debug Mode

Enable debug logging by setting `VERCEL_ENV=development` and checking Vercel function logs:

```bash
vercel logs --follow
```

### Performance Optimization

1. **Caching**: Approved registrations are cached for 60 seconds
2. **Pagination**: Use pagination to limit response sizes
3. **Batch Operations**: Consider batching multiple updates if needed

## 📊 Monitoring and Analytics

### Key Metrics to Monitor

1. **Registration Volume**: Track daily/weekly registration counts
2. **Approval Rate**: Monitor approval vs rejection ratios
3. **Response Times**: Monitor API response times
4. **Error Rates**: Track 4xx and 5xx error rates

### Vercel Analytics

Enable Vercel Analytics for detailed performance monitoring:

```bash
vercel analytics
```

## 🔄 Maintenance

### Regular Tasks

1. **Review Pending Registrations**: Check admin panel regularly
2. **Monitor Error Logs**: Review Vercel function logs weekly
3. **Update Dependencies**: Keep npm packages updated
4. **Backup Data**: Export Google Sheet data periodically

### Scaling Considerations

- **Google Sheets Limits**: 10M cells per spreadsheet
- **API Quotas**: 100 requests per 100 seconds per user
- **Vercel Limits**: 100GB bandwidth, 1000 serverless function invocations per month (hobby plan)

For high-volume usage, consider migrating to a proper database.

## 📞 Support

For issues or questions:

1. Check this README's troubleshooting section
2. Review Vercel function logs
3. Test with curl commands to isolate issues
4. Verify Google Sheets API quotas and permissions

## 📄 License

This project is part of the Adventist Health India system. All rights reserved.

---

**Deployment Checklist:**
- [ ] Google Sheet created with correct structure
- [ ] Service account created and JSON downloaded
- [ ] Spreadsheet shared with service account
- [ ] Environment variables set in Vercel
- [ ] Project deployed to Vercel
- [ ] All API endpoints tested with curl
- [ ] Frontend pages tested
- [ ] Admin panel tested with approval workflow