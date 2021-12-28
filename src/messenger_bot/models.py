from django.db import models


# Create your models here.
class BotUser(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя")
    user_id = models.BigIntegerField(null=False)
    chat_id = models.BigIntegerField(null=True, blank=True, default=None)
    notifies_on = models.BooleanField(default=True)
