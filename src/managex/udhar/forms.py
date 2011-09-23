from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from udhar.models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 10)
    password = forms.CharField(widget = forms.PasswordInput)
    
class AddExpenseForm(forms.ModelForm):
    friend = forms.CharField(max_length = 50)
    amount = forms.IntegerField()
    friendof = forms.CharField(max_length = 50)
    class Meta:
        model = BorrowList
        fields = ('amount',)
    def clean_friend(self):
        print self.cleaned_data
        friend = self.cleaned_data["friend"].split("@")
        try:
            friend = Friends.objects.get(id=friend[1],twitter_user = friend[0])
        except Friends.DoesNotExist:
            raise forms.ValidationError(_("A friend with this twitter username doesnot exists. "))
        return str(friend.twitter_user)+"@"+str(friend.id)

    def save(self, commit=True):
        expense = super(AddExpenseForm,self).save(commit=False)
        expense.amount = int(self.cleaned_data["amount"])
        temp = self.cleaned_data["friend"].split("@")
        expense.friend = Friends.objects.get(twitter_user = temp[0],id=temp[1])
        expense.status = 0
        if commit:
            expense.save()
        return expense 


class AddFriendForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 50)
    friendof = forms.CharField(max_length = 50) 
    last_name = forms.CharField(max_length = 50)
    twitter_username = forms.CharField(max_length = 50)
    class Meta:
        model = Friends
        fields = ('twitter_username',)
    def clean_friendof(self):
        twitter_username = self.cleaned_data["twitter_username"]
        try:
            friend = Friends.objects.filter(twitter_user = twitter_username)
            user = User.objects.get(username = str(self.cleaned_data["friendof"]))
            for f in friend:
                if f.friendof.username == user.username:
                    raise forms.ValidationError(_("A friend with same twitter username already exists as your friend"))
            return self.cleaned_data["friendof"]
        except Friends.DoesNotExist:
            return self.cleaned_data["friendof"]

    def save(self, commit=True):
        friend = super(AddFriendForm,self).save(commit=False)
        friend.first=(self.cleaned_data["first_name"])
        friend.last = (self.cleaned_data["last_name"])
        friend.twitter_user = (self.cleaned_data["twitter_username"])
        friend.friendof = User.objects.get(username = str(self.cleaned_data["friendof"]))
        if commit:
            friend.save()
        return friend

   

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length = 25)
    first_name = forms.CharField(max_length = 60)
    last_name = forms.CharField(max_length=60)
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists. "))
    def clean_password2(self):
        try:
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.ValidationError(_("The two password fields didn't match."))
        password2 = self.cleaned_data["password2"]    
        if password1 != password2: 
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2    

    def save(self, commit=True):
        user = super(RegisterForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name=(self.cleaned_data["first_name"])
        user.last_name = (self.cleaned_data["last_name"])
        if commit:
            user.save()
        return user


