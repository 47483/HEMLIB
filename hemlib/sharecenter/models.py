from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import logging
import os
logger = logging.getLogger(__name__)

def user_upload_path(instance, filename):
    return f'uploads/{instance.user.username}/{filename}'

class Content(models.Model):
    file = models.FileField(upload_to=user_upload_path)
    filename = models.CharField(max_length=255, default="UNDEFINED")
    uploaded = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = os.path.basename(self.file.name)
        super(Content, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
            super(Content, self).delete(*args, **kwargs)
            storage.delete(path)
        else:
            super(Content, self).delete(*args, **kwargs)