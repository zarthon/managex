from django.conf import settings
from udhar import forms as myforms
from django.http import *
from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required 
from udhar.models import *
import tweepy

#GLOBAL setting
AUTH = {}
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
                wall[(str(friend.first + " " + friend.last),_sum,str(friend.twitter_user))] = borrow_list
    else:
        return render_to_response("ShowMessage.html",{'msg_heading':'Error','msg_html':'User is an ADMIN'},context_instance=RequestContext(request)) 
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))


@login_required
def sendDM(request):
    global AUTH
    print "Inside sendm"
    if request.user.is_authenticated() and request.user.username != "admin":
        try:
            print "Phase One"
            twitter = Twitter.objects.get(user=request.user)
            auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,settings.CONSUMER_SECRET)
            auth.set_access_token(twitter.token_key,twitter.token_secret)
            api = tweepy.API(auth)
            if request.method == "GET":
                message = request.GET["message"].split("@")
                print message
                try:
                    temp = api.get_user(str(message[1]))
                    print temp.id
                    api.send_direct_message(user_id = temp.id, text=message[0])
                except:
                    return HttpResponse("Invalid User")
                return HttpResponse("Posted Successfully")
        except Twitter.DoesNotExist:
            try:
                print "Phase 2"
                url = AuthorizeURL.objects.get(user=request.user)
                return render_to_response( "authorize.html", {'url':str(url.url)}, context_instance = RequestContext(request) )
            except AuthorizeURL.DoesNotExist:
                print "Phase 3"
                auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,settings.CONSUMER_SECRET)
                auth_url = auth.get_authorization_url()
                print auth_url
                AUTH[str(request.user.username)] = auth
                url_obj = AuthorizeURL(user=request.user,url=str(auth_url))
                url_obj.save()
                print "Phase 4"
                return render_to_response( "authorize.html", {'url':str(auth_url)}, context_instance = RequestContext(request) )

@login_required
def authorize(request):
    if request.method == "POST":
        pin = request.POST["pin"]
        print AUTH
        auth = AUTH[str(request.user.username)]
        print "heelll"
        try:
            auth.get_access_token(str(pin))
        except:
            return render_to_response("ShowMessage.html", {'msg_heading':"Error", 'msg_html':"Incorrect Pin" }, context_instance=RequestContext(request))
        auth_key = auth.access_token.key
        auth_secret = auth.access_token.secret
        print "halle"
        twitter = Twitter(user=request.user,token_key=auth_key,token_secret=auth_secret)
        twitter.save()
        return HttpResponseRedirect("/home")

@login_required
def removeFriend(request):
    if request.method == "POST":
        friend_user = request.POST["friend"].split("@");
        friend = Friends.objects.get(friendof=request.user, twitter_user = str(friend_user[0]),id=int(friend_user[1]))
        friend.delete()
        return HttpResponseRedirect("/home")
    else:
        friends = Friends.objects.filter(friendof=request.user)
        return render_to_response("removefriend.html",{'friends':friends},context_instance=RequestContext(request))
