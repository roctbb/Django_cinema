from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from cinema.models import Screening, Booking
from django.views.generic import ListView, DetailView
from django.contrib import auth
from django.utils.decorators import method_decorator


class ScreeningsListView(ListView):  # представление в виде списка
    model = Screening  # модель для представления


class ScreeningsDetailView(DetailView):
    model = Screening


def screening(request, rid):
    if request.POST.get('screening', '') == '':
        screen = Screening.objects.get(id=rid);
        bookings = Booking.objects.filter(screening_id=screen.id)
        na = {-1: 0}
        for b in bookings:
            na[b.place] = 1;
        seatsTable = "<form method='post'><table><input type='hidden' name='csrfmiddlewaretoken' value='" + get_token(
            request) + \
                     "'/><input type='hidden' name='screening' value='" + str(rid) + "'>" \
                                                                                     ""

        place = 1;

        for i in range(screen.hall.rows):
            seatsTable += "<tr>"
            for j in range(screen.hall.seats // screen.hall.rows):
                if na.get(place, 0) == 0:
                    seatsTable = seatsTable + "<td><input type='checkbox' name='place" + str(
                        place) + "' value='yes' /></td>"
                else:
                    seatsTable = seatsTable + "<td></td>"
                place += 1
            seatsTable += "</tr>"
        seatsTable += "</table><p>&nbsp;</p><input type='submit'/></form>"

        return render_to_response("cinema/book.html",
                                  RequestContext(request, {'screening': screen, 'bookings': seatsTable
                                                           }))
    else:
        screen = Screening.objects.get(id=rid);
        bookings = Booking.objects.filter(screening_id=screen.id)
        for i in range(screen.hall.seats):
            if request.POST.get('place' + str(i), '') != '':
                newbook = Booking(person=request.user.username, screening_id=screen.id, place=i)
                newbook.save()

        return render_to_response("cinema/success.html", RequestContext(request, {}))


def login(request):
    if request.POST.get('username', '') != '':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user)
            # Перенаправление на "правильную" страницу
            return HttpResponseRedirect("/cinema/")
        else:
            # Отображение страницы с ошибкой
            return HttpResponseRedirect("/cinema/login/")
    else:
        return render_to_response("cinema/login.html", RequestContext(request, {}))


def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/cinema/login/")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/cinema/login/")
        else:
            return render_to_response("cinema/register.html", {
            'form': form}, context_instance=RequestContext(request))
    else:
        form = UserCreationForm()
        return render_to_response("cinema/register.html", {
            'form': form,
        }, context_instance=RequestContext(request))