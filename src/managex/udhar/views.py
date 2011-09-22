from django.conf import settings
from udhar import forms as myforms
from django.http import *
from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logout')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    if not request.user.is_authenticated():
        form = myforms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST["username"],password=request.POST["password"])
            if user is not None:
                auth_login(request,user)
                return HttpResponseRedirect("/logout")
            else:
                return HttpResponse('wrong.html',{},context_instance=RequestContext(request))
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


def home(request):
    pass
