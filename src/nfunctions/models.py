from django.db import models

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