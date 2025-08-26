
from apps.user.infrastructure.mappers.user_mapper import UserMapper
from apps.user.config.models import User as UserModel
from apps.user.domain.entities import  User as DomainUser
from apps.user.domain.repository import IUserRepository
from django.db import transaction
from shared.utils.pagination import fetch_with_pagination


class UserRepository(IUserRepository):
    
    def get_by_id(self, pk: int):
        try:
            data = UserModel.objects.get(pk=pk)
            return UserMapper.to_domain(data)
        except UserModel.DoesNotExist:
            return None
    
    @transaction.atomic
    def save(self, user: DomainUser):
        orm_obj = UserMapper.to_model(user)
        orm_obj.save()
        orm_obj.groups.set(user.get('groups', []))
        orm_obj.user_permissions.set(user.get('user_permissions', []))
        return UserMapper.to_domain(orm_obj)
        
    def get_all(self, **kwargs):
        orm_objs = UserModel.objects.all()
        return fetch_with_pagination(
            queryset=orm_objs,
            to_domain=UserMapper.to_domain,
            to_response=UserMapper.to_response,
            **kwargs
        )
    
    def get_by_email(self, email: str):
        orm_obj = UserModel.objects.get(email=email)
        user = UserMapper.to_domain(orm_obj)
        return user
    
    def get_by_username(self, username: str):
        orm_obj = UserModel.objects.get(username=username)
        user = UserMapper.to_domain(orm_obj)
        return user
    
    @transaction.atomic
    def update(self, newuser: dict, orm_obj):
        
        print('newuser', newuser), print('orm_obj', orm_obj)
        for attr, value in newuser.items():
            if attr in ['groups', 'user_permissions']:
                continue
            setattr(orm_obj, attr, value)

        orm_obj.save()

        if 'groups' in newuser:
            orm_obj.groups.set(newuser['groups'])
        if 'user_permissions' in newuser:
            orm_obj.user_permissions.set(newuser['user_permissions'])

        return UserMapper.to_domain(orm_obj)

    def hard_delete(self, user_id: int):
        orm_obj = UserModel.all_objects.get(pk=user_id)
        orm_obj.delete(force_policy="hard")
        return UserMapper.to_domain(orm_obj)

    def soft_delete(self, user_id: int):
        orm_obj = UserModel.objects.get(pk=user_id)
        orm_obj.delete()
        orm_obj.is_active = False
        orm_obj.save(update_fields=["is_active"])
        return UserMapper.to_domain(orm_obj)

    def verify_email(self, user_id: int):
        orm_obj = UserModel.objects.get(pk=user_id)
        orm_obj.is_verify = True
        orm_obj.save(update_fields=["is_verify"])
        
    def change_password(self, user_id: int, new_password: str):
        orm_obj = UserModel.objects.get(pk=user_id)
        orm_obj.password = new_password
        orm_obj.save(update_fields=["password"])
        return UserMapper.to_domain(orm_obj)