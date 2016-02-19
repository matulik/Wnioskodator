# coding=UTF-8

from django.db import models
from hashlib import sha1

# Session expiry time (in [ms])
SESSION_EXPIRED_TIME = 30000
TOKEN_KEY = u"DUPA"


class User(models.Model):
    username = models.CharField(max_length=50, blank=False, verbose_name=u'Login')
    password = models.CharField(max_length=50, blank=False, verbose_name=u'Password')
    firstname = models.CharField(max_length=50, verbose_name=u'Name')
    surname = models.CharField(max_length=50, verbose_name=u'Surename')
    email = models.EmailField()
    access_lvl = models.IntegerField(default=0, verbose_name=u'Access level')
    token = models.CharField(max_length=40, blank=True)

    class Meta:
        db_table = 'USER'

    def hashPassword(self, password):
        return sha1(password.encode('utf8')).hexdigest()

    def checkPassword(self, password):
        if self.hashPassword(password) == self.password:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        self.password = self.hashPassword(self.password)
        self.token = Login.generateToken(self)
        super(User, self).save(*args, **kwargs)


class Login():
    @staticmethod
    def login(request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print u'Bad username or password'
            return False
        if user and user.checkPassword(password):
            request.session['login'] = True
            request.session['id'] = user.id
            request.session.set_expiry(SESSION_EXPIRED_TIME)
            print u'Login successfully'
            return True
        else:
            print u'Bad username or password'
            return False

    @staticmethod
    def logout(request):
        request.session.flush()
        request.session['login'] = False
        request.session['id'] = None
        print u'Logout'

    @staticmethod
    def auth(request):
        if not request.session.get('login', None) or not request.session.get('id', None):
            return False
        if request.session['login'] == True and request.session['id'] != None:
            return True
        else:
            return False

    @staticmethod
    def getCurrentUserToken(user):
        return user.token

    @staticmethod
    def generateToken(user):
        token = user.username + str(user.id) + TOKEN_KEY
        return sha1(token.encode('utf8')).hexdigest()

    @staticmethod
    def setToken(user):
        user.token = Login.getToken()
        user.save()

    @staticmethod
    def getCurrentUser(request):
        # Try to get token
        try:
            token = request.META['HTTP_TOKEN']
        except:
            print "No token"
            token = None

        if token:
            try:
                user = User.objects.get(token=token)
                return user
            except User.DoesNotExist:
                return None
        else:
            try:
                uid = request.session['id']
                user = User.objects.get(id=uid)
                return user
            except User.DoesNotExist:
                return None

    @staticmethod
    def tokenAuth(request):
        try:
            token = request.META['HTTP_TOKEN']
        except:
            return False

        if token:
            user = Login.getUserByToken(token)
            if user:
                return True
        return False
