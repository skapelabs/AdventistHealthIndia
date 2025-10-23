/**
 * Update Registration Status API endpoint
 * Allows admins to approve or reject registrations
 * Protected by ADMIN_API_KEY header
 * 
 * POST /api/updateStatus
 * Headers: x-admin-key: <ADMIN_API_KEY>
 * Body: { id?, email?, status: "approved"|"rejected", notes? }
 * 
 * Returns: 200 OK with updated registration data
 */

import { 
  initializeSheetsAPI, 
  updateRegistrationStatus 
} from './utils/sheets.js';

export default async function handler(req, res) {
  // Set CORS headers for frontend requests
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, x-admin-key');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'Method not allowed',
      code: 'METHOD_NOT_ALLOWED'
    });
  }

  try {
    // Check admin authentication
    const adminKey = req.headers['x-admin-key'];
    const expectedAdminKey = process.env.ADMIN_API_KEY;

    if (!expectedAdminKey) {
      console.warn('ADMIN_API_KEY not configured - endpoint is unprotected');
    } else if (!adminKey || adminKey !== expectedAdminKey) {
      return res.status(401).json({
        error: 'Unauthorized',
        code: 'INVALID_ADMIN_KEY',
        details: 'Valid admin key required in x-admin-key header'
      });
    }

    // Parse and validate request body
    const updateData = req.body;
    
    if (!updateData || typeof updateData !== 'object') {
      return res.status(400).json({
        error: 'Invalid request body',
        code: 'INVALID_BODY'
      });
    }

    // Validate required fields
    const { id, email, status, notes } = updateData;

    if (!id && !email) {
      return res.status(400).json({
        error: 'Either id or email is required',
        code: 'MISSING_IDENTIFIER'
      });
    }

    if (!status || !['approved', 'rejected'].includes(status)) {
      return res.status(400).json({
        error: 'Invalid status',
        code: 'INVALID_STATUS',
        details: 'Status must be either "approved" or "rejected"'
      });
    }

    // Initialize Google Sheets API
    const sheets = initializeSheetsAPI();
    
    // Determine identifier (id takes precedence over email)
    const identifier = id || email;
    
    // Update registration status
    const updatedRegistration = await updateRegistrationStatus(
      sheets, 
      identifier, 
      status, 
      notes || ''
    );

    // Return success response
    return res.status(200).json({
      success: true,
      data: updatedRegistration,
      message: `Registration ${status} successfully`
    });

  } catch (error) {
    console.error('Update status error:', error);
    
    // Handle specific errors
    if (error.message === 'Registration not found') {
      return res.status(404).json({
        error: 'Registration not found',
        code: 'NOT_FOUND',
        details: 'No registration found with the provided identifier'
      });
    }
    
    if (error.message.includes('authentication')) {
      return res.status(500).json({
        error: 'Service configuration error',
        code: 'AUTH_ERROR'
      });
    }
    
    if (error.message.includes('quota') || error.message.includes('rate limit')) {
      return res.status(429).json({
        error: 'Service temporarily unavailable',
        code: 'RATE_LIMIT'
      });
    }

    // Generic error response
    return res.status(500).json({
      error: 'Internal server error',
      code: 'INTERNAL_ERROR'
    });
  }
}
