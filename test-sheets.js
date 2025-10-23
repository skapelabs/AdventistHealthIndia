import { google } from 'googleapis';
import { readFileSync } from 'fs';

const SPREADSHEET_ID = '1WJwkXMFzvFLL5I_b9ETC2SFXgnM1Y6EywPT_qfh9M6s';

// Load service account from file
const serviceAccount = JSON.parse(readFileSync('/Users/pranjaldubey/Downloads/adventist-476010-008951d91aac.json', 'utf8'));

async function testSheets() {
  try {
    const auth = new google.auth.GoogleAuth({
      credentials: serviceAccount,
      scopes: ['https://www.googleapis.com/auth/spreadsheets']
    });

    const sheets = google.sheets({ version: 'v4', auth });
    
    // Get spreadsheet metadata
    const response = await sheets.spreadsheets.get({
      spreadsheetId: SPREADSHEET_ID
    });

    console.log('Spreadsheet title:', response.data.properties.title);
    console.log('Available sheets:');
    response.data.sheets.forEach(sheet => {
      console.log(`- ${sheet.properties.title} (ID: ${sheet.properties.sheetId})`);
    });

  } catch (error) {
    console.error('Error:', error.message);
  }
}

testSheets();
