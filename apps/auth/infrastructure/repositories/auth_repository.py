
from apps.user.infrastructure.mappers.user_mapper import UserMapper
from apps.user.config.models import User as UserModel
from apps.auth.domain.repository import IAuthRepository

class AuthRepository(IAuthRepository):
    def verify_email(self, user_id: int):
        orm_obj = UserModel.objects.get(pk=user_id)
        orm_obj.is_verify = True
        orm_obj.save(update_fields=["is_verify"])
        
    def change_password(self, user_id: int, new_password: str):
        orm_obj = UserModel.objects.get(pk=user_id)
        orm_obj.password = new_password
        orm_obj.save(update_fields=["password"])
        return UserMapper.to_domain(orm_obj)