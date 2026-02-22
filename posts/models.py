from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    keywords = models.TextField(help_text="Comma-separated keywords")
    upload_date = models.DateTimeField(auto_now_add=True)
    image_features = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=[('gentlemen', 'gentlemen'), ('ladies', 'ladies'), ('neutral', 'neutral')], default = 'neutral')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.caption
    
    class Meta:
        ordering = ['-upload_date']


class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, choices=[
        ('default', 'Default'),
        ('benito', 'Benito'),
        ('earthy', 'Earthy'),
        ('marty_supreme', 'Marty Supreme'),
        ('lanacore', 'Lanacore'),
        ('italian_summer', 'Italian Summer')
    ], default='default')
    contact_number = models.CharField(max_length=10, blank=True)

    
    def __str__(self):
        return f"{self.user.username} - {self.theme}"