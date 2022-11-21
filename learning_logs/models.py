from xmlrpc.client import DateTime
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    # モデルの学んでいるトピック
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        # モデルの文字列表現
        return self.text
    
class Entry(models.Model):
    # トピックに関して学んだ具体的なこと
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
class Meta:
    verbose_name_plural = 'entries'
    
    def __str__(self):
        # モデルの文字列表現を返す
        return f"{self.text[:25]}..."
        
class City(models.Model):
    name = models.CharField(max_length=25)
    my_city = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
class Meta:
    verbose_name_plural = 'cities'
