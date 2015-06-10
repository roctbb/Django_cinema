from django.db import models


class Hall(models.Model):
    title = models.CharField(max_length=255) # заголовок поста
    seats = models.IntegerField();
    rows = models.IntegerField();
    vipplaces = models.CharField(max_length=255)
    notvalidplaces =  models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    photo = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "halls/%i/" % self.id

class Film(models.Model):
    title = models.CharField(max_length=255) # заголовок поста
    description = models.CharField(max_length=1000)
    photo = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "films/%i/" % self.id

class Screening(models.Model):
    film = models.ForeignKey(Film)
    date = models.DateTimeField(u'Время') # дата публикации
    hall = models.ForeignKey(Hall)
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/cinema/%i/" % self.id

class Booking(models.Model):
    screening = models.ForeignKey(Screening)
    person = models.CharField(max_length=255)
    place = models.IntegerField();
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/booking/%i/" % self.id