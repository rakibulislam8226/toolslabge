# Email Verification System Documentation

## Overview

A clean, simplified email verification system that blocks unverified users from accessing the application. After registration, users must verify their email before they can access any protected routes.

## Key Features

- 🔐 **Secure verification tokens** using UUID4
- ⏰ **24-hour token expiration**
- 📧 **Professional email templates**
- 🚫 **Access control** - Unverified users cannot access protected routes
- 🎨 **Vue.js verification pages** with clean UX
- 🧹 **Automatic token cleanup**

## User Flow

1. **User registers** → Account created with `is_verified=False`
2. **Verification email sent** → Professional email with verification link
3. **Access blocked** → User cannot access dashboard until verified
4. **Email verification required page** → Shows verification status and resend option
5. **User clicks verification link** → Email verified, access granted
6. **Dashboard access** → User can now access all features

## API Endpoints

### Email Verification
**POST** `/api/v1/users/email/verify/`
```json
{
    "token": "12345678-1234-5678-9012-123456789012"
}
```

### Resend Verification Email  
**POST** `/api/v1/users/email/resend-verification/`
```json
{
    "email": "user@example.com"
}
```

### Check Verification Status
**GET** `/api/v1/users/email/status/{email}/`

## Frontend Routes

- `/verify-email/{token}` - Email verification page
- `/email-verification-required` - Shown to unverified users
- `/dashboard` - Only accessible to verified users

## Access Control

**Unverified users are automatically redirected to the email verification required page** when trying to access:
- Dashboard
- Projects
- Tasks  
- Organization settings
- Any protected route

**Only accessible to unverified users:**
- Login/Register pages
- Email verification pages
- Public pages

## Configuration

### Email Settings
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yoursite.com
```

### Celery Setup
```bash
celery -A config worker --loglevel=info
```

## Security

- ✅ UUID4 tokens (cryptographically secure)
- ✅ 24-hour expiration
- ✅ One-time use tokens
- ✅ Access control at router level
- ✅ No CSRF issues (JWT only)