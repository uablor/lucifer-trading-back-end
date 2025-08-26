from django.urls import path, include
from .list_api_view import ListApiAPIView
app_name = 'api'
urlpatterns = [
    path('', ListApiAPIView.as_view(), name='list-user'),
    path('user/', include('config.urls.restful_url.user_urls')),
    path('auth/', include('config.urls.restful_url.auth_urls')),
    path('twofa/', include('config.urls.restful_url.twofa_urls')),


]

