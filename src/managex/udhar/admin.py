from udhar.models import * 
from django.contrib import admin


class FriendsAdmin(admin.ModelAdmin):
    list_display = ('id','twitter_user')
admin.site.register(Friends,FriendsAdmin)
admin.site.register(BorrowList)
