import { google } from 'googleapis';
import { readFileSync } from 'fs';

const SPREADSHEET_ID = '1WJwkXMFzvFLL5I_b9ETC2SFXgnM1Y6EywPT_qfh9M6s';

// Load service account from file
const serviceAccount = JSON.parse(readFileSync('/Users/pranjaldubey/Downloads/adventist-476010-008951d91aac.json', 'utf8'));

async function setupSheets() {
  try {
    const auth = new google.auth.GoogleAuth({
      credentials: serviceAccount,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const sheets = google.sheets({ version: 'v4', auth });
    
    // Rename Sheet1 to Registrations
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      requestBody: {
        requests: [{
          updateSheetProperties: {
            properties: {
              sheetId: 0,
              title: 'Registrations'
            },
            fields: 'title'
          }
        }]
      }
    });

    console.log('✅ Renamed Sheet1 to Registrations');

    // Add headers to the Registrations sheet
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: 'Registrations!A1:K1',
      valueInputOption: 'RAW',
      requestBody: {
        values: [[
          'id',
          'name', 
          'email',
          'hospital',
          'role',
          'specialty',
          'bio',
          'submitted_at',
          'status',
          'status_updated_at',
          'notes'
        ]]
      }
    });

    console.log('✅ Added headers to Registrations sheet');

    // Add one example approved row
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: 'Registrations!A2:K2',
      valueInputOption: 'RAW',
      requestBody: {
        values: [[
          'example-001',
          'Dr. John Smith',
          'john.smith@example.com',
          'Adventist Health Center',
          'Doctor',
          'Cardiology',
          'Experienced cardiologist with 10+ years of practice.',
          '2024-01-15T10:30:00Z',
          'approved',
          '2024-01-15T11:00:00Z',
          'Approved by admin'
        ]]
      }
    });

    console.log('✅ Added example approved row');

    // Create AdminLogs sheet
    await sheets.spreadsheets.batchUpdate({
      spreadsheetId: SPREADSHEET_ID,
      requestBody: {
        requests: [{
          addSheet: {
            properties: {
              title: 'AdminLogs'
            }
          }
        }]
      }
    });

    console.log('✅ Created AdminLogs sheet');

    // Add headers to AdminLogs sheet
    await sheets.spreadsheets.values.update({
      spreadsheetId: SPREADSHEET_ID,
      range: 'AdminLogs!A1:E1',
      valueInputOption: 'RAW',
      requestBody: {
        values: [[
          'timestamp',
          'action',
          'email',
          'old_status',
          'new_status'
        ]]
      }
    });

    console.log('✅ Added headers to AdminLogs sheet');

    console.log('🎉 Google Sheets setup completed successfully!');

  } catch (error) {
    console.error('❌ Error setting up sheets:', error.message);
  }
}

setupSheets();
