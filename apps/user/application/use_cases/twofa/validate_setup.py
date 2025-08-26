# apps/user/application/use_cases/twofa/validate_setup.py
from django_otp.plugins.otp_totp.models import TOTPDevice

class ValidateSetupTwoFAUseCase:
    def execute(self, user, otp: str):
        try:
            device = TOTPDevice.objects.get(user=user, name="default")
            if device.verify_token(otp):
                user.is_2fa_enabled = True
                user.save(update_fields=["is_2fa_enabled"])
                return True
            return False
        except TOTPDevice.DoesNotExist:
            return False
