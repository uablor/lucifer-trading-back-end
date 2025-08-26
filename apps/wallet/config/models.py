from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel
from apps.user.config.models import User
class Wallet(SoftDeletableModel, TimeStampedModel):

    demo_balance = models.IntegerField( default=1000)
    currency = models.CharField(max_length=50, blank=False, null=False)
    real_balance = models.IntegerField(blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)  # auto_now=True will update this field to the current time whenever the model is saved
    reserved = models.IntegerField(blank=False, null=False)
    admin_wallet = models.BooleanField(default=False)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, null=True )

    def __str__(self):
        return f"Wallet {self.id} - {self.currency}"
