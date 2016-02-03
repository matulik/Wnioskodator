#coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext
from django.views.decorators.csrf import csrf_exempt

from User.models import *

@csrf_exempt
def login(request):
    if Login.auth(request):
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
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


