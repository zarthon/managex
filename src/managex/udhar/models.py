from django.db import models
from django.contrib.auth.models import User


class Friends(models.Model):
    friendof = models.ForeignKey(User)
    first = models.CharField(max_length = 50)
    last = models.CharField(max_length = 50)
    twitter_user = models.CharField(max_length = 50)

class BorrowList(models.Model):
    friend = models.ForeignKey(Friends)
    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()

class Twitter(models.Model):
    user = models.ForeignKey(User)
    token_key = models.CharField( max_length = 500 )
    token_secret = models.CharField( max_length = 500 )

class AuthorizeURL(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField( max_length = 1000 )
