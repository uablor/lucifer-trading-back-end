# infrastructure/mappers/user_mapper.py
from apps.user.domain.entities import User
from apps.user.config.models import User as UserModel
from shared.utils.date_format import format_date_to_lao

class UserMapper:
    @staticmethod
    def to_domain(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            is_active=user_model.is_active,
            avatar=user_model.avatar,
            is_2fa_enabled=user_model.is_2fa_enabled,
            is_verify=user_model.is_verify,
            password=user_model.password,
            is_superuser=user_model.is_superuser,
            is_staff=user_model.is_staff,
            groups=list(user_model.groups.all()),
            user_permissions=list(user_model.user_permissions.all()),
            created=user_model.created,
            modified=user_model.modified,
            is_removed=user_model.is_removed,
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        user_model = UserModel()
        if user.get("id") is not None: user_model.id = user["id"]
        user_model.username = user["username"] 
        if user.get("email") is not None: user_model.email = user["email"]
        if user.get("is_active") is not None: user_model.is_active = user["is_active"]
        if user.get("avatar") is not None: user_model.avatar = user["avatar"]
        if user.get("is_2fa_enabled") is not None: user_model.is_2fa_enabled = user["is_2fa_enabled"]
        if user.get("is_verify") is not None: user_model.is_verify = user["is_verify"]
        if user.get("password") is not None: user_model.password = user["password"]
        if user.get("is_superuser") is not None: user_model.is_superuser = user["is_superuser"]
        if user.get("is_staff") is not None: user_model.is_staff = user["is_staff"]
        return user_model
        

    @staticmethod
    def to_response(user: User) -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            # 'avatar': user.avatar,
            'is_2fa_enabled': user.is_2fa_enabled,
            'is_verify': user.is_verify,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            
            'avatar': user.avatar if user.avatar else '',
            'groups': [group.name for group in user.groups.all()] if hasattr(user.groups, 'all') else [],
            'user_permissions': [perm.name for perm in user.user_permissions.all()] if hasattr(user.user_permissions, 'all') else [],

            'created': format_date_to_lao(user.created),
            'modified': format_date_to_lao(user.modified),
            'is_removed': user.is_removed,
            
        }

    @staticmethod
    def to_list_response(users: list[User]) -> list[dict]:
        return [UserMapper.to_response(user) for user in users]

