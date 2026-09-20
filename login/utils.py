import html
import random
import re
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

OTP_SEND_LIMIT_PER_IP = 3


def sanitize_for_output(value):
    """Strip script/iframe tags and HTML event attributes before output."""
    if value is None:
        return ''

    text = str(value)
    text = re.sub(r'<\s*/?\s*script\b[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/?\s*iframe\b[^>]*>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
    text = re.sub(r'on\w+\s*=\s*[^\s>]+', '', text, flags=re.IGNORECASE)
    return html.escape(text, quote=True)


def get_client_ip(request):
    """Get a normalized client IP address from the request."""
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def record_otp_send(request):
    """Record an OTP send attempt for this IP and allow only 3 sends."""
    client_ip = get_client_ip(request)
    cache_key = f'otp_send_count_{client_ip}'
    current_count = cache.get(cache_key, 0)

    if current_count >= OTP_SEND_LIMIT_PER_IP:
        return False

    cache.set(cache_key, current_count + 1, timeout=60 * 60 * 24)
    return True


def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(email, otp):
    """Send OTP to user's email"""
    subject = "Your OTP for Event Workshop Registration"
    message = f"""
Hello,

Your OTP for registering on Event Workshop is: {otp}

This OTP is valid for 5 minutes.

If you didn't request this, please ignore this email.

Best regards,
Event Workshop Team
    """

    try:
        # Always print OTP to console for visibility
        print("\n" + "="*50)
        print(f"📧 OTP EMAIL SENT TO: {email}")
        print(f"🔑 OTP CODE: {otp}")
        print("="*50 + "\n")

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or 'noreply@eventworkshop.com',
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"\n❌ Error sending email: {e}\n")
        return False


def create_otp_for_email(email):
    """Create and save OTP for an email"""
    otp = generate_otp()
    EmailOTP.objects.create(email=email, otp=otp)
    print(f"\n✅ OTP Created: {otp} for {email}")
    return otp
