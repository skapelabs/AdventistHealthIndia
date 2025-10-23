/**
 * Get Approved Registrations API endpoint
 * Returns all approved healthcare professionals with pagination support
 * 
 * GET /api/getApproved?limit=50&offset=0
 * 
 * Returns: 200 OK with approved registrations array
 */

import { 
  initializeSheetsAPI, 
  getAllRegistrations 
} from './utils/sheets.js';

export default async function handler(req, res) {
  // Set CORS headers for frontend requests
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({
      error: 'Method not allowed',
      code: 'METHOD_NOT_ALLOWED'
    });
  }

  try {
    // Parse pagination parameters
    const limit = parseInt(req.query.limit) || 50;
    const offset = parseInt(req.query.offset) || 0;

    // Validate pagination parameters
    if (limit < 1 || limit > 100) {
      return res.status(400).json({
        error: 'Invalid limit parameter',
        code: 'INVALID_LIMIT',
        details: 'Limit must be between 1 and 100'
      });
    }

    if (offset < 0) {
      return res.status(400).json({
        error: 'Invalid offset parameter',
        code: 'INVALID_OFFSET',
        details: 'Offset must be non-negative'
      });
    }

    // Initialize Google Sheets API
    const sheets = initializeSheetsAPI();
    
    // Get all registrations
    const allRegistrations = await getAllRegistrations(sheets);
    
    // Filter for approved registrations only
    const approvedRegistrations = allRegistrations.filter(reg => 
      reg.status === 'approved'
    );

    // Apply pagination
    const totalCount = approvedRegistrations.length;
    const paginatedResults = approvedRegistrations.slice(offset, offset + limit);

    // Set caching headers for better performance
    res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');

    // Return success response
    return res.status(200).json({
      success: true,
      data: paginatedResults,
      pagination: {
        total: totalCount,
        limit,
        offset,
        hasMore: offset + limit < totalCount
      }
    });

  } catch (error) {
    console.error('Get approved registrations error:', error);
    
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
