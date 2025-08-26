
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.application.use_cases.queries.get_one import GetOneUserUseCase
from apps.user.application.use_cases.queries.resend_verify_email import ResendVerifyEmailUserUseCase
from apps.user.application.use_cases.queries.get_all import GetAllUserUseCase
from apps.user.application.use_cases.queries.logout import LogoutUserUseCase
from apps.user.application.use_cases.commands.change_password import ChangePasswordUserCommand
from apps.user.application.use_cases.queries.forgot_password import ForgotPasswordUserUseCase
from apps.user.application.use_cases.commands.password_reset import PasswordResetCommand
from apps.user.application.use_cases.queries.login import LoginUserUseCase
from apps.user.application.use_cases.commands.create_user import CreateUserCommand
from apps.user.application.use_cases.commands.soft_delete_user import SoftDeleteUserCommand
from apps.user.application.use_cases.commands.hard_delete_user import HardDeleteUserCommand
from apps.user.application.use_cases.commands.verify_email import VerifyEmailCommand
from apps.user.application.use_cases.commands.update_user import UpdateUserCommand
from apps.user.application.use_cases.queries.get_email import GetEmailUserUseCase
from apps.user.presentation.api.serlializers.serializers import UserSerializer, UserLoginSerializer, RefreshTokenSerializer, EmailSerializer, PasswordSerializer, PasswordResetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.user.infrastructure.mappers.user_mapper import UserMapper

class BestUserUseCase:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._get_one_usecase = GetOneUserUseCase()
        self._get_all_usecase = GetAllUserUseCase()
        self._create_usecase = CreateUserCommand()
        self._update_usecase = UpdateUserCommand()
        self._soft_delete_usecase = SoftDeleteUserCommand()
        self._hard_delete_usecase = HardDeleteUserCommand()
        self._get_email_usecase = GetEmailUserUseCase()
        self._login_usecase = LoginUserUseCase()
        self._logout_usecase = LogoutUserUseCase()
        self._verify_email_usecase = VerifyEmailCommand()
        self._resend_usecase = ResendVerifyEmailUserUseCase()
        self._change_password_usecase = ChangePasswordUserCommand()
        self._forgot_password_usecase = ForgotPasswordUserUseCase()
        self._password_reset_usecase = PasswordResetCommand()
        
        
class UserAuthMeView( BestUserUseCase, APIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def put(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self._update_usecase.execute(serializer.validated_data, pk)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = self._update_usecase.execute(serializer.validated_data, pk)
        return Response(data, status=status.HTTP_200_OK)

    def get(self, request):
        auth_user = request.user
        data = self._get_one_usecase.execute(auth_user.id)
        return Response(UserMapper.to_response(data), status=status.HTTP_200_OK)


class UserLoginView(BestUserUseCase,APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        result = self._login_usecase.execute(email, password)

        if isinstance(result, Response):
            return result  
        return Response(result, status=status.HTTP_200_OK)
    


class UserLogoutView(BestUserUseCase, APIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = self.serializer_class(data=request.data).data.get('refresh_token')
        if not refresh_token:
            return Response({"message": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        
        usecase = self._logout_usecase.execute(request, refresh_token)
        if usecase is None:
            return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(usecase, status=status.HTTP_200_OK)


class VerifyEmailAPIView(BestUserUseCase, APIView):

    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        try:
            uid = request.query_params.get('uid')
            token = request.query_params.get('token')
        except (TypeError, ValueError, OverflowError):
            return Response({'error': 'Invalid uid or token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if uid is None or token is None:
            return Response({'error': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)

        user = self._verify_email_usecase.execute(uid, token)
        if user is not None:
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerifyEmailAPIView(BestUserUseCase, APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            success = self._resend_usecase.execute(email)
            if success is None:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            if success:
                return Response(success, status=status.HTTP_200_OK)
            return Response(success, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(BestUserUseCase, APIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = self._change_password_usecase.execute(serializer.validated_data, request.user.id)
            if data is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ForgotPasswordView(BestUserUseCase, APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            success = self._forgot_password_usecase.execute(email)
            if success is None:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            if success:
                return Response(success, status=status.HTTP_200_OK)
            return Response(success, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(BestUserUseCase, APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request, encoded_pk, token):
        
        if encoded_pk is None or token is None:
            return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            data = self._password_reset_usecase.execute(serializer.validated_data, encoded_pk, token)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        