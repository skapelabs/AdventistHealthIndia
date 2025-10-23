#!/usr/bin/env python3
"""
Adventist Health India Website
Startup script for development
"""

import os
import sys
from app import app, db

def main():
    """Main function to start the Flask application"""
    print("🏥 Starting Adventist Health India Website...")
    print("📍 Server will be available at: http://localhost:6990")
    print("🔧 Running in development mode")
    print("=" * 50)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Start the Flask development server
    app.run(
        host='0.0.0.0',
        port=6990,
        debug=True,
        use_reloader=True
    )

if __name__ == '__main__':
    main()
