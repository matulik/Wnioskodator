#coding=UTF-8

from django.db import models
from django.utils import timezone

from User.models import User

class Application(models.Model):
    dateAdded = models.DateTimeField(blank=False, default=timezone.now, verbose_name=u'Data dodania')
    whoAdded = models.ForeignKey(User, blank=False, verbose_name=u'Dodane przez')
    dateLastEdited = models.DateTimeField(blank=True, default=timezone.now, verbose_name=u'Data ostatniej edycji')
    applicationNumber = models.CharField(max_length=50, blank=False, verbose_name=u'Numer wniosku')
    applicationOwner = models.CharField(max_length=50, blank=False, verbose_name=u'Nazwa wnioskodawcy')
    applicationTitle = models.CharField(max_length=50, blank=False, verbose_name=u'Tytuł projektu')
    firstViewBy = models.CharField(max_length=50, blank=False, verbose_name=u'Pierwsze sprawdzenie')
    secondViewBy = models.CharField(max_length=50, blank=False, verbose_name=u'Drugie sprawdzenie')
    firstStageOpinion = models.CharField(max_length=50, blank=False, verbose_name=u'Wynik oceny')
    additionalDescription = models.CharField(max_length=150, blank=False, verbose_name=u"Dodatkowe uwagi")

    class Meta:
        db_table = 'APPLICATION'

