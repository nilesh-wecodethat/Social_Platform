from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=5)
    photo = models.ImageField(
        upload_to="user/%Y/%m/%d/", blank=True
    )  # it defines the directory path where the uploaded image will be saved

    def __str__(self):
        return f"Profile for user {self.user.username}"
