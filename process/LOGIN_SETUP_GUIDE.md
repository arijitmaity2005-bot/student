# Event Management System - Login Setup Guide

## ✅ Changes Made

### 1. **Created `login/utils.py`**
   - `generate_otp()` - Generates random 6-digit OTP
   - `send_otp_email()` - Sends OTP to user's email
   - `create_otp_for_email()` - Creates and saves OTP record

### 2. **Updated `login/models.py`**
   - **New User Model**: Custom Django User based on AbstractUser
     - Email as unique identifier (instead of username)
     - `is_verified` field for email verification
   - **Updated Customer Model**: Linked to User via OneToOneField
     - Removed password field (now handled by User model)
     - Added phone and address fields
   - **Updated EmailOTP Model**: Added `is_used` field to track OTP usage

### 3. **Completely Rewrote `login/views.py`**
   - `login_view()` - Display login page
   - `login_user()` - Handle email/password login
   - `register_view()` - Display registration page
   - `register_user()` - Handle user registration with validation
   - `verify_otp()` - Handle OTP verification (5-minute expiry)
   - `resend_otp()` - Resend OTP to email
   - `home()` - Protected home view (requires login)
   - `logout_user()` - Handle logout

### 4. **Updated `login/urls.py`**
   Added all necessary URL patterns:
   ```
   '' → login_view
   'login/' → login_user
   'register/' → register_view
   'register/submit/' → register_user
   'verify-otp/' → verify_otp
   'resend-otp/' → resend_otp
   'logout/' → logout_user
   ```

### 5. **Created/Updated Templates**
   - **login.html**: Fixed to use email field instead of username
   - **register.html**: Complete registration form with validation
   - **verify_otp.html**: OTP verification with countdown timer

### 6. **Updated `login/admin.py`**
   - Registered User, Customer, and EmailOTP models
   - Custom admin interfaces for each model

### 7. **Updated `student/settings.py`**
   - Configured `AUTH_USER_MODEL = 'login.User'`
   - Added email backend configuration (console for development)
   - Added session configuration
   - Added login/logout redirect URLs

---

## 🚀 Setup Instructions

### Step 1: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Create Superuser (for admin)
```bash
python manage.py createsuperuser
```

### Step 3: Run Development Server
```bash
python manage.py runserver
```

### Step 4: Test the Application
- Go to: `http://localhost:8000/`
- Register: `http://localhost:8000/register/`
- Login: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`

---

## 📧 Email Configuration

### For Development (Default)
The project uses console email backend - emails will be printed to console.

### For Production (Gmail SMTP)
Update `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

---

## 🔐 Security Features Implemented

✅ Password hashing using Django's default hasher  
✅ CSRF token protection on all forms  
✅ OTP-based email verification (5-minute expiry)  
✅ Login required decorators on protected views  
✅ Email uniqueness validation  
✅ Password confirmation on registration  
✅ Minimum 8-character password requirement  
✅ Session-based authentication  
✅ HttpOnly cookies  

---

## ⚠️ Important Notes

1. **Never commit secrets**: The SECRET_KEY in settings.py should be moved to environment variables for production

2. **Create migrations**: Before running the server, run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Email Service**: During development, check the console for OTP emails. For production, configure SMTP settings.

4. **Static Files**: Make sure your front.jpeg exists in `static/` folder for the background image

5. **Database**: The project uses SQLite by default. For production, consider using PostgreSQL

---

## 📝 Database Schema

### User Table
- id, username, email (unique), password, first_name, last_name
- is_verified, is_active, is_staff, is_superuser
- date_joined, last_login

### Customer Table
- id, user_id (OneToOne), phone, address
- created_at, updated_at

### EmailOTP Table
- id, email, otp, is_used
- created_at

---

## 🧪 Test Flow

1. **Register**: Create new account with valid email
2. **OTP Verification**: Check console for OTP, enter it
3. **Login**: Use email and password to login
4. **Home**: Should see customer profile
5. **Logout**: Click logout link to logout

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "User matching query does not exist" | Make sure you've created users through registration |
| "OTP Expired" | OTP is valid for 5 minutes only |
| "Email already registered" | Use a different email address |
| Emails not sending | Check EMAIL_BACKEND setting, use console for testing |
| Static files not loading | Run `python manage.py collectstatic` |

---

## 📚 File Structure Summary

```
student/
├── login/
│   ├── models.py (✅ Updated - User, Customer, EmailOTP)
│   ├── views.py (✅ Updated - All login logic)
│   ├── urls.py (✅ Updated - All routes)
│   ├── admin.py (✅ Updated - Admin registration)
│   ├── utils.py (✅ NEW - OTP utilities)
│   └── migrations/ (will be generated)
├── templates/
│   ├── login.html (✅ Fixed - email field)
│   ├── register.html (✅ Updated)
│   └── verify_otp.html (✅ NEW)
├── student/
│   └── settings.py (✅ Updated - AUTH_USER_MODEL, email config)
└── db.sqlite3 (will be created by migrations)
```

---

Generated: 2024
For support: Check Django documentation and review code comments
