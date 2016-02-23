#coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext

from User.models import *

def login(request):
    if Login.auth(request):
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist or User.MultipleObjectsReturned:
                msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
                return render_to_response('User/login.html', { 'msg' : msg } , context_instance=RequestContext(request))

            if user.checkPassword(password):
                Login.login(request)
                return redirect('/home/')
            else:
                msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
                return render_to_response('User/login.html', { 'msg' : msg } , context_instance=RequestContext(request))
        else:
            return render_to_response('User/login.html', context_instance=RequestContext(request))


def logout(request):
    if Login.auth(request):
        Login.logout(request)
    return render_to_response('User/login.html', context_instance=RequestContext(request))

