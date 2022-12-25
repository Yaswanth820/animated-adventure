from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    fileName = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
        return self.fileName