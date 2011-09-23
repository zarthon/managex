from django.db import models
from django.contrib.auth.models import User


class Friends(models.Model):
    friendof = models.ForeignKey(User)
    first = models.CharField(max_length = 50)
    last = models.CharField(max_length = 50)
    twitter_user = models.CharField(max_length = 50,unique=True)

class BorrowList(models.Model):
    friend = models.ForeignKey(Friends)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()
