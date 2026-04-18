from django.db import models

# Create your models here.

from django.db import models

class LogFile(models.Model):
    file = models.FileField(upload_to='logs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)