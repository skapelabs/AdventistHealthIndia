/**
 * Registration API endpoint
 * Handles POST requests to register new healthcare professionals
 * 
 * POST /api/register
 * Body: { name, email, hospital, role, specialty?, bio? }
 * 
 * Returns: 201 Created with registration data or error response
 */

import { 
  initializeSheetsAPI, 
  getAllRegistrations, 
  appendRegistration, 
  findExistingRegistration, 
  validateRegistrationData 
} from './utils/sheets.js';

export default async function handler(req, res) {
  // Set CORS headers for frontend requests
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

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
    // Parse and validate request body
    const registrationData = req.body;
    
    if (!registrationData || typeof registrationData !== 'object') {
      return res.status(400).json({
        error: 'Invalid request body',
        code: 'INVALID_BODY'
      });
    }

    // Validate required fields
    const validation = validateRegistrationData(registrationData);
    if (!validation.isValid) {
      return res.status(400).json({
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        details: validation.errors
      });
    }

    // Initialize Google Sheets API
    const sheets = initializeSheetsAPI();
    
    // Get existing registrations to check for duplicates
    const existingRegistrations = await getAllRegistrations(sheets);
    
    // Check for duplicate email
    const existingRegistration = findExistingRegistration(
      existingRegistrations, 
      registrationData.email
    );

    if (existingRegistration) {
      // Handle duplicate email based on current status
      if (existingRegistration.status === 'pending' || existingRegistration.status === 'approved') {
        return res.status(409).json({
          error: 'Email already registered',
          code: 'DUPLICATE_EMAIL',
          details: {
            status: existingRegistration.status,
            message: `This email is already registered with status: ${existingRegistration.status}`
          }
        });
      }
      
      // If status is 'rejected', allow re-registration
      // We'll append a new row to preserve history
      console.log(`Allowing re-registration for previously rejected email: ${registrationData.email}`);
    }

    // Append new registration
    const newRegistration = await appendRegistration(sheets, registrationData);

    // Return success response
    return res.status(201).json({
      success: true,
      data: newRegistration,
      message: 'Registration submitted successfully'
    });

  } catch (error) {
    console.error('Registration error:', error);
    
    // Handle specific Google Sheets errors
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
