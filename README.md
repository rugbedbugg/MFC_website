# Cybersecurity Monitoring Website

A modern web application built with Flask that helps users monitor their cybersecurity status, check for data breaches, and manage their security profile. The application integrates with SpyCloud's API to provide real-time threat intelligence and breach notifications.

## Features

### 🔐 User Authentication
- Secure user registration and login
- Password hashing using SHA-256
- Session management
- Profile management with customizable user information

### 📊 Threat Dashboard
- Real-time threat monitoring using SpyCloud API
- Visual representation of security threats
- Severity-based threat categorization (High, Medium, Low)
- Timeline view of security incidents

### 🔍 Breach Checker
- Email breach checking functionality
- Historical breach data access
- Detailed breach information including:
  - Breach date
  - Affected services
  - Type of compromised data
  - Severity level

### 👤 User Profile
- Customizable user profiles
- Secure password updates
- Personal information management
- Email preferences configuration

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Security**: Werkzeug Security, Session Management
- **API Integration**: SpyCloud API
- **Environment Management**: python-dotenv

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MFC_website-2
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
SPYCLOUD_API_KEY=your_api_key_here
SPYCLOUD_API_ENDPOINT=https://api.spycloud.com/v1
SECRET_KEY=your_secret_key_here
```

5. Initialize the database:
```bash
python3 app.py
```

## Usage

1. Start the application:
```bash
python3 app.py
```

2. Access the website at: `http://127.0.0.1:5001`

3. Register a new account or login with existing credentials

4. Navigate through the features:
   - View your security status on the Threat Dashboard
   - Check for breaches using the Breach Checker
   - Update your profile information
   - Monitor real-time security alerts

## Security Features

- Password hashing using SHA-256
- Secure session management
- CSRF protection
- Input validation and sanitization
- Secure API key handling
- Error logging and monitoring
- Rate limiting on sensitive endpoints

## Project Structure

```
MFC_website-2/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables
├── instance/            
│   └── users.db         # SQLite database
├── static/
│   └── style.css        # CSS styles
├── templates/
│   ├── base.html        # Base template
│   ├── dashboard.html   # Dashboard template
│   ├── login.html       # Login template
│   ├── profile.html     # Profile template
│   └── signup.html      # Registration template
└── services/
    └── spycloud_service.py  # SpyCloud API integration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SpyCloud API for threat intelligence data
- Flask framework and its contributors
- SQLAlchemy team for the ORM
- All open-source packages used in this project

## Support

For support, please open an issue in the repository or contact the development team.

## Security

If you discover any security-related issues, please email security@example.com instead of using the issue tracker.

---
Built with ❤️ by Your Team Name 