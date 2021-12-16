from django.db import models

# Create your models here.


class URL(models.Model):
    og_url = models.CharField(max_length=100, primary_key=True)
    shorten_url = models.CharField(max_length=6)

    def __str__(self):
        return "{0}".format(self.og_url)
