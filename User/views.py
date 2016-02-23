# coding=UTF-8

from django.shortcuts import redirect, render_to_response, RequestContext

from User.models import *


def login(request):
    if Login.auth(request) == True:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist or User.MultipleObjectsReturned:
                msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
                return render_to_response('User/changepassword.html', {'msg': msg}, context_instance=RequestContext(request))

            if user.checkPassword(password):
                login = Login.login(request)
                if login == True:
                    return redirect('/home/')
                elif login == GLOBAL_EXPIRED:
                    return redirect('/changepassword/')
                else:
                    msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
                    return render_to_response('User/login.html', {'msg': msg}, context_instance=RequestContext(request))

            else:
                msg = u'Błędna nazwa użytkownika lub hasła. Spróbuj ponownie.'
                return render_to_response('User/login.html', {'msg': msg}, context_instance=RequestContext(request))
        else:
            return render_to_response('User/login.html', context_instance=RequestContext(request))


def logout(request):
    if Login.auth(request):
        Login.logout(request)
    return render_to_response('User/login.html', context_instance=RequestContext(request))


def changepassword(request):
    log = Login.auth(request)
    if log == True:
        return redirect('/home/')
    elif log == GLOBAL_EXPIRED:
        if request.method == 'POST':
            user = Login.getCurrentUser(request)
            if user:
                oldpass = request.POST['oldpassword']
                newpass = request.POST['newpassword']
                reppass = request.POST['repeatnewpassword']
                if not user.checkPassword(oldpass):
                    msg = u'Stare hasło jest niepoprawne.'
                    return render_to_response('User/changepassword.html', {'msg': msg},
                                              context_instance=RequestContext(request))
                if newpass == oldpass:
                    msg = u'Stare i nowe hasło są takie same. Sprobuj ponownie.'
                    return render_to_response('User/changepassword.html', {'msg': msg},
                                              context_instance=RequestContext(request))
                if newpass != reppass:
                    msg = u'Nowe i powtórzone hasło nie są jednakowe. Sprobuj ponownie.'
                    return render_to_response('User/changepassword.html', {'msg': msg},
                                              context_instance=RequestContext(request))
                if len(newpass) < PASSWORD_LENGTH:
                    msg = u'Hasło musi mieć conajmnie 6 znaków.'
                    return render_to_response('User/changepassword.html', {'msg': msg},
                                              context_instance=RequestContext(request))

                # If here:
                user.password = newpass
                user.save()
                return redirect('/home/')
        else:
            return render_to_response('User/changepassword.html', context_instance=RequestContext(request))
    else:
        msg = u'Coś poszło nie tak. Spróbuj ponownie.'
        return render_to_response('User/login.html', {msg: msg}, context_instance=RequestContext(request))
