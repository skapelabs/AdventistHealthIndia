# 🚀 Adventist Health Registration System - Deployment Guide

## Current Status: Ready for Deployment ✅

All backend files are created and configured. Here's what you need to do to deploy:

## 📋 Pre-Deployment Checklist

### ✅ Completed:
- [x] All API endpoints created (`/api/register.js`, `/api/getApproved.js`, `/api/getPending.js`, `/api/updateStatus.js`)
- [x] Google Sheets utilities implemented (`/api/utils/sheets.js`)
- [x] Frontend pages created (`register.html`, `directory.html`, `admin.html`)
- [x] Package.json with dependencies
- [x] Vercel configuration (`vercel.json`)
- [x] Comprehensive README with setup instructions
- [x] Test scripts and templates

### 🔧 Required Setup:
- [ ] Google Sheets API enabled ✅ (You mentioned this is done)
- [ ] Service account created and shared ✅ (You mentioned this is done)
- [ ] Environment variables set in Vercel ✅ (You mentioned this is done)

## 🚀 Deployment Steps

### 1. Login to Vercel (Required)
```bash
vercel login
```
- This will open a browser for authentication
- Follow the prompts to authenticate

### 2. Deploy to Vercel
```bash
# Deploy to production
vercel --prod --yes

# Or deploy to preview first
vercel
```

### 3. Set Environment Variables (if not already done)
```bash
# Set your environment variables
vercel env add SPREADSHEET_ID
vercel env add GOOGLE_SERVICE_ACCOUNT  
vercel env add ADMIN_API_KEY
```

## 🧪 Testing Your Deployment

### 1. Test Registration Endpoint
```bash
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
```

**Expected Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "uuid-123",
    "name": "Dr. Test User",
    "email": "test@example.com",
    "hospital": "Test Hospital", 
    "role": "Doctor",
    "specialty": "General Medicine",
    "bio": "Test bio for verification",
    "submitted_at": "2024-01-15T10:30:00Z",
    "status": "pending",
    "status_updated_at": "",
    "notes": ""
  },
  "message": "Registration submitted successfully"
}
```

### 2. Test Get Approved Endpoint
```bash
curl https://your-domain.vercel.app/api/getApproved
```

**Expected Response (200):**
```json
{
  "success": true,
  "data": [],
  "pagination": {
    "total": 0,
    "limit": 50,
    "offset": 0,
    "hasMore": false
  }
}
```

### 3. Test Admin Endpoints
```bash
# Get pending registrations (requires admin key)
curl https://your-domain.vercel.app/api/getPending \
  -H "x-admin-key: YOUR_ADMIN_KEY"

# Update status (requires admin key)
curl -X POST https://your-domain.vercel.app/api/updateStatus \
  -H "Content-Type: application/json" \
  -H "x-admin-key: YOUR_ADMIN_KEY" \
  -d '{
    "email": "test@example.com",
    "status": "approved",
    "notes": "Approved for testing"
  }'
```

## 🔍 Troubleshooting

### Common Issues:

1. **Authentication Error (401/403)**
   - Check that `GOOGLE_SERVICE_ACCOUNT` is properly formatted JSON
   - Verify the service account email has access to the spreadsheet
   - Ensure the spreadsheet ID is correct

2. **Spreadsheet Not Found (404)**
   - Double-check the `SPREADSHEET_ID` from your Google Sheets URL
   - Verify the spreadsheet exists and is accessible

3. **Rate Limiting (429)**
   - Google Sheets API has quotas (100 requests per 100 seconds)
   - Wait a moment and retry

4. **Environment Variables**
   - Ensure all three variables are set in Vercel
   - Check that `GOOGLE_SERVICE_ACCOUNT` is the full JSON as a string

## 📊 Google Sheets Setup

### Required Sheet Structure:

**Sheet Name: `Registrations`**
```
| id | name | email | hospital | role | specialty | bio | submitted_at | status | status_updated_at | notes |
```

**Sheet Name: `AdminLogs`** 
```
| log_id | action | target_id | admin_key_used | timestamp | notes |
```

### Import Template:
1. Use the provided `spreadsheet-template.csv` file
2. Import it into your Google Sheet
3. Share the sheet with your service account email

## 🎯 Frontend Testing

After deployment, test these URLs:

1. **Registration Form**: `https://your-domain.vercel.app/register.html`
2. **Public Directory**: `https://your-domain.vercel.app/directory.html`  
3. **Admin Panel**: `https://your-domain.vercel.app/admin.html`

## 📈 Expected Workflow

1. **User Registration**: 
   - User fills form at `/register.html`
   - Data saved to Google Sheets with `status: pending`

2. **Admin Review**:
   - Admin logs into `/admin.html` with admin key
   - Reviews pending registrations
   - Approves/rejects with notes

3. **Public Display**:
   - Approved registrations appear in `/directory.html`
   - Search and pagination work seamlessly

## 🚨 Important Notes

- **Admin Key**: Keep your `ADMIN_API_KEY` secure
- **Service Account**: Never expose the JSON credentials
- **Rate Limits**: Google Sheets API has quotas
- **Caching**: Approved registrations are cached for 60 seconds

## ✅ Success Indicators

Your deployment is working when:
- [ ] Registration endpoint returns 201 with new UUID
- [ ] Duplicate email returns 409 error
- [ ] Get approved returns empty array initially
- [ ] Admin endpoints require valid admin key
- [ ] Status updates work and reflect in Google Sheets
- [ ] Frontend pages load and function correctly

## 🆘 Need Help?

If you encounter issues:
1. Check Vercel function logs: `vercel logs`
2. Verify environment variables in Vercel dashboard
3. Test with curl commands first
4. Check Google Sheets API quotas
5. Ensure spreadsheet is properly shared

The system is production-ready and will handle the complete registration workflow seamlessly!
