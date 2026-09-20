
from datetime import timedelta
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import User, Customer, EmailOTP
from .utils import (
    OTP_SEND_LIMIT_PER_IP,
    create_otp_for_email,
    record_otp_send,
    sanitize_for_output,
    send_otp_email,
)

# Create your views here.

def login_view(request):
    """Display login page"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def login_user(request):
    """Handle user login with email and password"""
    if request.method == 'POST':
        email = sanitize_for_output(request.POST.get('email', '').strip())
        password = sanitize_for_output(request.POST.get('password', ''))
        login_method = request.POST.get('login_method', 'password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Please enter email and password.'})
        
        try:
            user = User.objects.get(email=email)
            
            # Check if user is verified
            if not user.is_verified:
                return render(request, 'login.html', {'error': 'Please verify your email first.'})
            
            # Authenticate user
            if user.check_password(password):
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password.'})
        
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'login.html')


def register_view(request):
    """Display registration page"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'register.html')


def register_user(request):
    """Handle user registration"""
    if request.method == 'POST':
        email = sanitize_for_output(request.POST.get('email', '').strip())
        password = sanitize_for_output(request.POST.get('password', '').strip())
        confirm_password = sanitize_for_output(request.POST.get('confirm_password', '').strip())
        first_name = sanitize_for_output(request.POST.get('first_name', '').strip())
        last_name = sanitize_for_output(request.POST.get('last_name', '').strip())
        
        # Validation
        if not all([email, password, confirm_password, first_name]):
            return render(request, 'register.html', 
                         {'error': 'Please fill all required fields.'})
        
        if password != confirm_password:
            return render(request, 'register.html', 
                         {'error': 'Passwords do not match.'})
        
        if len(password) < 8:
            return render(request, 'register.html', 
                         {'error': 'Password must be at least 8 characters.'})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', 
                         {'error': 'Email already registered.'})

        if not record_otp_send(request):
            return render(request, 'register.html', {
                'error': f'OTP send limit reached for this IP. Maximum {OTP_SEND_LIMIT_PER_IP} sends allowed.'
            })

        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_verified=False
            )

            # Create customer profile
            Customer.objects.create(user=user)

            # Generate and send OTP
            otp = create_otp_for_email(email)
            send_otp_email(email, otp)

            # Store email in session for verification
            request.session['verification_email'] = email

            return render(request, 'verify_otp.html',
                         {'email': email, 'message': 'OTP sent to your email.'})

        except Exception as e:
            return render(request, 'register.html',
                         {'error': f'Registration failed: {str(e)}'})
    
    return render(request, 'register.html')


def verify_otp(request):
    """Handle OTP verification"""
    email = request.session.get('verification_email')
    
    if not email:
        return redirect('register')
    
    if request.method == 'POST':
        user_otp = sanitize_for_output(request.POST.get('otp', '').strip())

        if not user_otp:
            return render(request, 'verify_otp.html',
                         {'error': 'Please enter OTP.', 'email': email})
        
        # Find matching OTP
        otp_record = EmailOTP.objects.filter(
            email=email,
            otp=user_otp,
            is_used=False
        ).order_by('-created_at').first()
        
        if not otp_record:
            return render(request, 'verify_otp.html', 
                         {'error': 'Invalid OTP.', 'email': email})
        
        # Check if OTP is expired (5 minutes)
        if timezone.now() - otp_record.created_at > timedelta(minutes=5):
            return render(request, 'verify_otp.html', 
                         {'error': 'OTP has expired. Please request a new one.', 'email': email})
        
        # Mark OTP as used and verify user
        try:
            user = User.objects.get(email=email)
            user.is_verified = True
            user.save()
            
            otp_record.is_used = True
            otp_record.save()
            
            # Clear session
            if 'verification_email' in request.session:
                del request.session['verification_email']
            
            # Auto-login user
            login(request, user)
            
            return redirect('home')
        
        except User.DoesNotExist:
            return render(request, 'verify_otp.html', 
                         {'error': 'User not found.', 'email': email})
        except Exception as e:
            return render(request, 'verify_otp.html', 
                         {'error': f'Verification failed: {str(e)}', 'email': email})
    
    return render(request, 'verify_otp.html', {'email': email})


def resend_otp(request):
    """Resend OTP to email"""
    if request.method == 'POST':
        email = sanitize_for_output(request.POST.get('email', '').strip())

        if not email:
            return render(request, 'verify_otp.html',
                         {'error': 'Email is required.'})

        if not record_otp_send(request):
            return render(request, 'verify_otp.html', {
                'error': f'OTP send limit reached for this IP. Maximum {OTP_SEND_LIMIT_PER_IP} sends allowed.',
                'email': email,
            })

        try:
            # Create new OTP
            otp = create_otp_for_email(email)
            send_otp_email(email, otp)

            request.session['verification_email'] = email

            return render(request, 'verify_otp.html',
                         {'email': email, 'message': 'OTP resent successfully.'})

        except Exception as e:
            return render(request, 'verify_otp.html',
                         {'error': f'Failed to resend OTP: {str(e)}', 'email': email})
    
    return redirect('register')


@login_required(login_url='login')
def home(request):
    """User home page"""
    # Prevent unverified users from accessing home
    if not request.user.is_verified:
        logout(request)
        return redirect('login')
    
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    return render(request, 'home.html', {'customer': customer})


def logout_user(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')
