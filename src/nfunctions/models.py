from django.db import models
from acctmang.models import User

# Create your models here.
class UrlHit(models.Model):
    url = models.URLField()
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.url)

    def increase(self):
        self.hits += 1
        self.save()


class HitCount(models.Model):
    url_hits = models.ForeignKey(UrlHit, editable=False, on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=1000)
    action = models.URLField(default="https://minify.tech/general/")
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def add_notfication(self, user, message, action):
        notification = Notification(user=user, message=message, action=action)
        notification.save()

    