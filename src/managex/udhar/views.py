from django.conf import settings
from udhar import forms as myforms
from django.http import *
from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from udhar.models import *
import tweepy

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    if not request.user.is_authenticated():
        form = myforms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST["username"],password=request.POST["password"])
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect("/home")
            else:
                return render_to_response( 'login.html',{'form':form,'data':request.POST,'error':True},context_instance=RequestContext(request))
        else:
            return render_to_response("login.html",{'form':form,'data':request.POST},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

def logout(request):
    auth_logout(request)
    return render_to_response('logout.html',{},context_instance=RequestContext(request))

def register(request):
    if not request.user.is_authenticated():
		form = myforms.RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username = request.POST["username"],password=request.POST["password1"])
			auth_login(request,user)
			return HttpResponseRedirect('/')
		else:
			return render_to_response("signup.html",{'signup_form':form,'signup':True,'data':request.POST},context_instance=RequestContext(request))

@login_required
def addFriend(request):
    form = myforms.AddFriendForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/home')
    else:
        return render_to_response("addfriend.html",{'addfriend_form':form,'addfriend':True,'data':request.POST},context_instance=RequestContext(request))

@login_required
def addExpense(request):
    if request.user.is_authenticated() and request.user.username != "admin":
        friends = Friends.objects.filter(friendof=request.user)
        form = myforms.AddExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/home')
        else:
            return render_to_response("addexpense.html",{'addexpense_form':form,'addexpense':True,'data':request.POST,'friends':friends},context_instance=RequestContext(request))
    else:
        return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'User is an ADMIN'},context_instance=RequestContext(request)) 


@login_required
def home(request):
    if request.user.is_authenticated() and request.user.username != "admin":
        friend_list = Friends.objects.filter(friendof = request.user)
        wall = {}
        borrow_list = None
        if friend_list is not None:
            for friend in friend_list:
                borrow_list = BorrowList.objects.filter(friend = friend,status=0).order_by('time').reverse()
                _sum = 0
                for borrow in borrow_list:
                    _sum += borrow.amount
                wall[(str(friend.first + " " + friend.last),_sum,friend.twitter_user)] = borrow_list
    else:
        return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'User is an ADMIN'},context_instance=RequestContext(request)) 
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))

@login_required
def removeExpense(request):
    if request.method == "GET":
        expenseid = request.GET["id"]
        expense = BorrowList.objects.get(id=expenseid)
        if str(expense.friend.friendof) == str(request.user.username):
            expense.status = 1
            expense.save()
            return HttpResponse("success")
        else:
            return HttpResponse("error")

@login_required
def expenseHistory(request):
    if request.user.is_authenticated() and request.user.username != "admin":
        friend_list = Friends.objects.filter(friendof = request.user)
        wall = {}
        borrow_list = None
        history = True
        if friend_list is not None:
            for friend in friend_list:
                borrow_list = BorrowList.objects.filter(friend = friend,status=1).order_by('time').reverse()
                _sum = 0
                for borrow in borrow_list:
                    _sum += borrow.amount
                wall[(str(friend.first + " " + friend.last),_sum)] = borrow_list
    else:
        return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'User is an ADMIN'},context_instance=RequestContext(request)) 
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))


@login_required
def sendDM(request):
    if request.user.is_authenticated() and request.user.username != "admin":
        try:
            twitter = Twitter.objects.get(user=request.user)
            auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,settings.CONSUMER_SECRET)
            auth.set_access_token(twitter.auth_key,twitter.token_secret)
            api = tweepy.API(auth)
            if request.method == "GET":
                message = request.POST["message"]
                api.update_status(message)
        except Twitter.DoesNotExist:
            try:
                url = AuthorizeURL.objects.get(user=request.user)
                return render_to_response( "authorize.html", {'url':str(url)}, context_instance = RequestContext(request) )
            except AuthorizeURL.DoesNotExist:
                auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,settings.CONSUMER_SECRET)
                auth_url = auth.get_authorization_url()
                url_obj = AuthorizeURL(user=request.user,url=str(auth_url))
                url_obj.save()
                return render_to_response( "authorize.html", {'url':str(auth_url)}, context_instance = RequestContext(request) )

@ogin_required
def authorize(request):
    if request.method == "GET":
        pin = request.GET["pin"]
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,settings.CONSUMER_SECRET)
        auth.get_access_token(pin)
        auth_key = auth.access_key
        auth_secret = auth.access_secret
        twitter = Twitter(user=request.user,auth_key,token_secret)
        twitter.save()

