# Smart GST Calculator with Authentication

A comprehensive GST calculation tool with user authentication, multi-item support, and professional invoice generation.

## Features

### 🔐 Authentication System
- **User Registration**: Sign up with email, name, and phone number
- **Secure Login**: Password-protected access
- **Profile Management**: Update personal information
- **Session Management**: Automatic logout and session handling

### 🧮 GST Calculator
- **Multi-Item Support**: Add multiple products with quantities
- **AI-Assisted Classification**: Automatic GST rate detection
- **Real-time Calculation**: Instant GST and total calculations
- **Fraud Detection**: Verify billed amounts against calculated totals

### 📄 Professional Invoices
- **PDF Generation**: Create professional invoices
- **Itemized Bills**: Detailed breakdown of all items
- **Company Branding**: Customizable invoice templates

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`

## Usage

### First Time Setup
1. **Sign Up**: Create an account with your email, name, and phone number
2. **Login**: Use your credentials to access the calculator

### Using the Calculator
1. **Add Items**: Click "Add Another Item" to add multiple products
2. **Enter Details**: Fill in product name, quantity, and unit price
3. **Calculate**: Click "Calculate" to see GST breakdown
4. **Generate Invoice**: Download a professional PDF invoice

### Profile Management
- Click "Profile" to update your information
- Click "Logout" to end your session

## Database

The application uses SQLite database (`database/users.db`) to store user information securely with hashed passwords.

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection
- Input validation
- Email verification

## API Endpoints

- `GET /` - Main calculator (requires login)
- `GET/POST /login` - User login
- `GET/POST /signup` - User registration
- `GET/POST /profile` - User profile management
- `POST /logout` - User logout
- `POST /calculate` - GST calculation
- `POST /api/check_fraud` - Fraud detection
- `POST /api/generate_invoice` - PDF invoice generation
- `GET /history` - Calculation history

## Technologies Used

- **Backend**: Flask, Flask-Login, Flask-WTF
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Werkzeug security

## File Structure

```
SmartGST/
├── app.py                 # Main Flask application
├── models.py             # User model and database functions
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── index.html        # Main calculator page
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   └── profile.html      # User profile page
├── static/               # CSS and static files
├── backend/              # Business logic
├── database/             # SQLite database files
└── output pictures/      # Generated files
```