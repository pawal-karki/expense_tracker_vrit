from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    EmailVerificationSerializer,
    ResendEmailVerificationSerializer
)
from .models import EmailVerification


def send_verification_email_to_terminal(user, verification_key):
    """Print verification URL to terminal for development"""
    verification_url = f"http://localhost:8000/auth/account-confirm-email/{verification_key}"
    print("\n" + "="*80)
    print("EMAIL VERIFICATION REQUIRED")
    print(f"User: {user.username} ({user.email})")
    print(f"Verification URL: {verification_url}")


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint with email verification
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create email verification token
        verification = EmailVerification.objects.create(user=user)
        
        # Print verification URL to terminal
        send_verification_email_to_terminal(user, verification.key)
        
        # Return user data without tokens (user needs to verify email first)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'message': 'User registered successfully. Please check terminal for email verification link.',
            'verification_required': True
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """
    User login endpoint
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Return user data with tokens
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(access_token),
            },
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_view(request):
    """
    Verify email endpoint
    """
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Check if there's already a pending verification
        verification = EmailVerification.objects.filter(
            user=user, 
            is_verified=False
        ).first()
        
        if verification:
            send_verification_email_to_terminal(user, verification.key)
            return Response({
                'message': 'Verification email sent. Please check terminal for verification link.',
                'email': email
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'error': 'No pending verification found for this email.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_email_verification_view(request):
    """
    Resend email verification endpoint
    """
    serializer = ResendEmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Deactivate old verification tokens
        EmailVerification.objects.filter(user=user, is_verified=False).update(is_verified=True)
        
        # Create new verification token
        verification = EmailVerification.objects.create(user=user)
        
        # Print verification URL to terminal
        send_verification_email_to_terminal(user, verification.key)
        
        return Response({
            'message': 'New verification email sent. Please check terminal for verification link.',
            'email': email
        }, status=status.HTTP_200_OK)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def email_confirm_redirect(request, key):

    #Email confirmation endpoint

    try:
        verification = EmailVerification.objects.get(key=key, is_verified=False)
        
        if verification.is_expired():
            return JsonResponse({
                'error': 'Verification link has expired. Please request a new one.',
                'expired': True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify the email
        verification.verify()
        
        print(f"\n EMAIL VERIFIED: {verification.user.username} ({verification.user.email})\n")
        
        return Response({
            'message': 'Email verified successfully! You can now log in.',
            'user': {
                'username': verification.user.username,
                'email': verification.user.email,
                'is_active': verification.user.is_active
            }
        }, status=status.HTTP_200_OK)
        
    except EmailVerification.DoesNotExist:
        return JsonResponse({
            'error': 'Invalid or already used verification link.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def account_email_verification_sent_view(request):

    return Response({
        'message': 'Email verification has been sent. Please check terminal for verification link.',
        'instructions': 'Click on the verification link to activate your account.'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
   
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
