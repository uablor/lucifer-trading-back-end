from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.user.application.use_cases.queries.get_one import GetOneUserUseCase
from apps.user.application.use_cases.queries.get_all import GetAllUserUseCase
from apps.user.application.use_cases.queries.login import LoginUserUseCase
from apps.user.application.use_cases.commands.create_user import CreateUserCommand
from apps.user.application.use_cases.commands.soft_delete_user import SoftDeleteUserCommand
from apps.user.application.use_cases.commands.hard_delete_user import HardDeleteUserCommand
from apps.user.application.use_cases.commands.update_user import UpdateUserCommand
from apps.user.application.use_cases.queries.get_email import GetEmailUserUseCase
from apps.user.presentation.api.serlializers.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from shared.utils.parse_pagination_params import parse_pagination_params
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.user.infrastructure.mappers.user_mapper import UserMapper
from apps.user.config.permission import UserPermission

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
     
        
class UserView(BestUserUseCase, APIView, ):
    permission_classes = [IsAuthenticated, UserPermission,]
    serializer_class = UserSerializer
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self._create_usecase.execute(serializer.validated_data)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self._update_usecase.execute(serializer.validated_data, pk)
        if data is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = self._update_usecase.execute(serializer.validated_data, pk)
        if data is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk=None):
        if pk is not None:
            data = self._get_one_usecase.execute(pk)
            if data is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)
        else:
            params = parse_pagination_params(request)
            data = self._get_all_usecase.execute(**params)
            return Response(data, status=status.HTTP_200_OK)
        
    def delete(self, request, pk=None):
        data = self._soft_delete_usecase.execute(pk)
        if data is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)


class UserRegisterView(BestUserUseCase,  APIView, ):
    permission_classes = [AllowAny,]
    serializer_class = UserRegisterSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self._create_usecase.execute(serializer.validated_data)
        return Response(UserMapper.to_response(data), status=status.HTTP_201_CREATED)


class UserHardDeleteView(BestUserUseCase, APIView,):
    permission_classes = [IsAuthenticated, UserPermission,]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete(self, request, pk=None):
        data = self._hard_delete_usecase.execute(pk)
        if data is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)


class UserRestoreView(BestUserUseCase, APIView,):
    permission_classes = [IsAuthenticated, UserPermission,]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete(self, request, pk=None):
        data = self._hard_delete_usecase.execute(pk)
        if data is None:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserMapper.to_response(data), status=status.HTTP_204_NO_CONTENT)


