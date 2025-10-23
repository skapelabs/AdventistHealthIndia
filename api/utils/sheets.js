/**
 * Google Sheets API utility module
 * Handles authentication and common operations for the registration system
 */

import { google } from 'googleapis';
import { v4 as uuidv4 } from 'uuid';

/**
 * Initialize Google Sheets API client with service account credentials
 * @returns {google.sheets_v4.Sheets} Authenticated Sheets API client
 */
export function initializeSheetsAPI() {
  try {
    const serviceAccount = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT);
    
    const auth = new google.auth.GoogleAuth({
      credentials: serviceAccount,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    return google.sheets({ version: 'v4', auth });
  } catch (error) {
    console.error('Failed to initialize Google Sheets API:', error);
    throw new Error('Google Sheets authentication failed');
  }
}

/**
 * Get all rows from the Registrations sheet
 * @param {google.sheets_v4.Sheets} sheets - Authenticated Sheets client
 * @returns {Promise<Array>} Array of registration objects
 */
export async function getAllRegistrations(sheets) {
  const spreadsheetId = process.env.SPREADSHEET_ID;
  
  try {
    const response = await sheets.spreadsheets.values.get({
      spreadsheetId,
      range: 'Registrations!A:K', // All columns A through K
    });

    const rows = response.data.values || [];
    
    if (rows.length === 0) {
      return [];
    }

    // Skip header row and convert to objects
    const headers = rows[0];
    const dataRows = rows.slice(1);
    
    return dataRows.map(row => {
      const obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index] || '';
      });
      return obj;
    });
  } catch (error) {
    console.error('Error fetching registrations:', error);
    throw new Error('Failed to fetch registrations from Google Sheets');
  }
}

/**
 * Append a new registration to the sheet
 * @param {google.sheets_v4.Sheets} sheets - Authenticated Sheets client
 * @param {Object} registrationData - Registration data to append
 * @returns {Promise<Object>} The inserted registration with generated ID
 */
export async function appendRegistration(sheets, registrationData) {
  const spreadsheetId = process.env.SPREADSHEET_ID;
  const id = uuidv4();
  const now = new Date().toISOString();
  
  const rowData = [
    id,
    registrationData.name,
    registrationData.email.toLowerCase().trim(),
    registrationData.hospital,
    registrationData.role,
    registrationData.specialty || '',
    registrationData.bio || '',
    now, // submitted_at
    'pending', // status
    '', // status_updated_at (empty for new registrations)
    '' // notes
  ];

  try {
    await sheets.spreadsheets.values.append({
      spreadsheetId,
      range: 'Registrations!A:K',
      valueInputOption: 'RAW',
      insertDataOption: 'INSERT_ROWS',
      resource: {
        values: [rowData]
      }
    });

    return {
      id,
      name: registrationData.name,
      email: registrationData.email.toLowerCase().trim(),
      hospital: registrationData.hospital,
      role: registrationData.role,
      specialty: registrationData.specialty || '',
      bio: registrationData.bio || '',
      submitted_at: now,
      status: 'pending',
      status_updated_at: '',
      notes: ''
    };
  } catch (error) {
    console.error('Error appending registration:', error);
    throw new Error('Failed to save registration to Google Sheets');
  }
}

/**
 * Update registration status by ID or email
 * @param {google.sheets_v4.Sheets} sheets - Authenticated Sheets client
 * @param {string} identifier - Either ID or email
 * @param {string} status - New status (approved/rejected)
 * @param {string} notes - Optional admin notes
 * @returns {Promise<Object>} Updated registration object
 */
export async function updateRegistrationStatus(sheets, identifier, status, notes = '') {
  const spreadsheetId = process.env.SPREADSHEET_ID;
  const now = new Date().toISOString();
  
  try {
    // First, get all registrations to find the target row
    const registrations = await getAllRegistrations(sheets);
    const targetRegistration = registrations.find(reg => 
      reg.id === identifier || reg.email === identifier
    );

    if (!targetRegistration) {
      throw new Error('Registration not found');
    }

    // Find the row number (add 2 because: +1 for header, +1 for 0-based to 1-based)
    const rowIndex = registrations.findIndex(reg => 
      reg.id === identifier || reg.email === identifier
    ) + 2;

    // Update status and status_updated_at columns (columns I and J)
    await sheets.spreadsheets.values.update({
      spreadsheetId,
      range: `Registrations!I${rowIndex}:K${rowIndex}`,
      valueInputOption: 'RAW',
      resource: {
        values: [[status, now, notes]]
      }
    });

    // Log admin action
    await logAdminAction(sheets, 'update_status', targetRegistration.id, notes);

    return {
      ...targetRegistration,
      status,
      status_updated_at: now,
      notes
    };
  } catch (error) {
    console.error('Error updating registration status:', error);
    throw error;
  }
}

/**
 * Log admin actions to AdminLogs sheet
 * @param {google.sheets_v4.Sheets} sheets - Authenticated Sheets client
 * @param {string} action - Action performed
 * @param {string} targetId - Target registration ID
 * @param {string} notes - Additional notes
 */
export async function logAdminAction(sheets, action, targetId, notes = '') {
  const spreadsheetId = process.env.SPREADSHEET_ID;
  const logId = uuidv4();
  const now = new Date().toISOString();
  
  const logData = [
    logId,
    action,
    targetId,
    'admin_key_used', // We'll track that a key was used
    now,
    notes
  ];

  try {
    await sheets.spreadsheets.values.append({
      spreadsheetId,
      range: 'AdminLogs!A:F',
      valueInputOption: 'RAW',
      insertDataOption: 'INSERT_ROWS',
      resource: {
        values: [logData]
      }
    });
  } catch (error) {
    // Log error but don't fail the main operation
    console.error('Failed to log admin action:', error);
  }
}

/**
 * Check if email already exists in registrations
 * @param {Array} registrations - Array of registration objects
 * @param {string} email - Email to check
 * @returns {Object|null} Existing registration or null
 */
export function findExistingRegistration(registrations, email) {
  return registrations.find(reg => 
    reg.email.toLowerCase().trim() === email.toLowerCase().trim()
  );
}

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if valid
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate required fields for registration
 * @param {Object} data - Registration data
 * @returns {Object} Validation result
 */
export function validateRegistrationData(data) {
  const errors = [];

  if (!data.name || data.name.trim().length === 0) {
    errors.push('Name is required');
  }

  if (!data.email || data.email.trim().length === 0) {
    errors.push('Email is required');
  } else if (!isValidEmail(data.email)) {
    errors.push('Invalid email format');
  }

  if (!data.hospital || data.hospital.trim().length === 0) {
    errors.push('Hospital is required');
  }

  if (!data.role || data.role.trim().length === 0) {
    errors.push('Role is required');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
