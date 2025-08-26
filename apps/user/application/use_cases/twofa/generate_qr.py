# apps/user/application/use_cases/twofa/generate_qr.py
import pyotp, base64, qrcode
from io import BytesIO
from apps.user.application.use_cases.best_use_case import BestUserUseCase
class GenerateTwoFAUseCase(BestUserUseCase):
    def execute(self, user):
        from django_otp.plugins.otp_totp.models import TOTPDevice

        device, created = TOTPDevice.objects.get_or_create(user=user, name="default")

        # base32 secret
        secret = base64.b32encode(device.bin_key).decode('utf-8')
        totp = pyotp.TOTP(secret)

        # provisioning URI (ใช้ scan QR)
        otp_url = totp.provisioning_uri(name=user.username, issuer_name="MyApp")

        # Generate QR code as base64
        qr_img = qrcode.make(otp_url)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"secret": secret, "otp_url": otp_url, "qr_code": qr_base64}
