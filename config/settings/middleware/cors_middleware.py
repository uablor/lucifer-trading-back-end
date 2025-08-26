# config/settings/middleware/cors_middleware.py

from django.utils.deprecation import MiddlewareMixin

class CustomCORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        return response
