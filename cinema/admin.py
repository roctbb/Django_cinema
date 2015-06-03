from django.contrib import admin
from cinema.models import Hall
from cinema.models import Film
from cinema.models import Screening
from cinema.models import Booking
admin.site.register(Hall)
admin.site.register(Film)
admin.site.register(Screening)
admin.site.register(Booking)