from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

class ListApiAPIView(APIView):

    def get(self, request, *args, **kwargs):
        data = {
            
            "auth": {
                "auth-me": reverse("api:user-auth-me", request=request),
                "user-logout": reverse("api:user-logout", request=request),
                "user-login": reverse("api:user-login", request=request),
                
                "emali" : {
                "verify-email": reverse("api:verify-email", request=request),
                "resend-verify-email": reverse("api:resend-verify-email", request=request),
                },
                "password": {
                "change-password": reverse("api:change-password", request=request),
                "validate-forgot-password-otp": reverse("api:forgot-password", request=request),
                "password-reset": reverse("api:password-reset", request=request),
                },
                "twofa": {
                "generate-otp": reverse("api:generate-otp", request=request),
                "validate-otp": reverse("api:validate-otp", request=request),
                "validate-otp-user-login": reverse("api:validate-otp-user-login", request=request),
                },

            },
            "account": {
                "user-crud": reverse("api:user-view", request=request),
                "user-register": reverse("api:user-register", request=request),
                "user-restore": reverse("api:user-restore", kwargs={"pk": 5}, request=request),
                "user-hard-delete": reverse("api:user-hard-delete", kwargs={"pk": 5}, request=request),
            },
            "wallet": {
                # "wallet": reverse("api:wallet-view", request=request),
                # "wallet-register": reverse("api:wallet-register", request=request),
                # "wallet-restore": reverse("api:wallet-restore", kwargs={"pk": 5}, request=request),
                # "wallet-hard-delete": reverse("api:wallet-hard-delete", kwargs={"pk": 5}, request=request),
            },
        }
        
        return Response(data)
