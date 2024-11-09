from django.db import models

# Create your models here.
class Advertisement(models.Model):
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()

    def __str__(self):
        return self.link  # or any other string representation you prefer
