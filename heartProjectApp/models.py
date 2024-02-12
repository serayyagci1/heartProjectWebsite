from django.db import models

class Picture(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')  # Update this line
    category = models.CharField(max_length=50, default='default_category')

    def __str__(self):
        return self.title


