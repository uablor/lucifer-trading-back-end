from django.urls import path
from apps.user.presentation.api.views.user_views import UserView, UserRegisterView, UserHardDeleteView, UserRestoreView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()


# Create a router and register the viewset with it.
# Don't include the API root; we want to handle the root ourselves.
# router.register(r"users", SoftDeleteUserView, basename="users")

urlpatterns = [

    path('', UserView.as_view(), name='user-view'),
    path('<int:pk>/', UserView.as_view(), name='user-detail'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('<int:pk>/hard_delete/', UserHardDeleteView.as_view(), name="user-hard-delete"),
    path('<int:pk>/restore/', UserRestoreView.as_view(), name="user-restore"),
    
]

urlpatterns += router.urls