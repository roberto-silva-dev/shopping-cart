from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse
from authapp.serializers import ProfileSerializer, LoginSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(description="Bad Request: Validation error or other issue"),
        },
        description="Perform the login",
        summary="Login",
    )
    def post(self, request):
        if self.request.user.is_authenticated:
            return Response(ProfileSerializer(self.request.user).data)
        session_key = request.session.session_key
        user = authenticate(
            request,
            username=self.request.data.get('username'),
            password=self.request.data.get('password'),
        )
        if user:
            request.original_session_key = session_key
            login(request, user)
            return Response(ProfileSerializer(user).data)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCsrfTokenView(APIView):
    @extend_schema(
        description="Set the CSRF token on cookies",
        summary="Set CSRF token cookie",
    )
    def get(self, request):
        return Response({'message': 'CSRF token set successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Logout the current user",
        summary="Logout user",
    )
    def post(self, request, *args, **kwargs):
        logout(self.request)
        return Response({'message': 'Logout successful'})


@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(APIView):

    @extend_schema(
        responses={
            200: ProfileSerializer,
        },
        description="Retrieve the current user details if authenticated or session key if not",
        summary="Profile details",
    )
    def get(self, request, *args, **kwargs):
        return Response(
            ProfileSerializer(self.request.user).data if self.request.user.is_authenticated else {
                'session_key': self.request.session.session_key
            }
        )
