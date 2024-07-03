from django.db import models # type: ignore

# Create your models here.
class Robot(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    purpose = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)