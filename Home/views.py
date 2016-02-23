#coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext

from User.models import *

def home(request):
    if Login.auth(request):
        user = Login.getCurrentUser(request)
        return render_to_response('Home/home.html', {'user': user}, context_instance=RequestContext(request))
    else:
        msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
        return render_to_response('User/login.html', {'msg': msg}, context_instance=RequestContext(request))

