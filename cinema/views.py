from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext
from cinema.models import Screening, Booking, Hall, Film
from django.views.generic import ListView, DetailView
from django.contrib import auth
from django.utils.decorators import method_decorator


class ScreeningsListView(ListView):  # представление в виде списка
    model = Screening  # модель для представления


class ScreeningsDetailView(DetailView):
    model = Screening

class HallListView(ListView):  # представление в виде списка
    model = Hall  # модель для представления


class FilmListView(ListView):  # представление в виде списка
    model = Film  # модель для представления

def screening(request, rid):
    if request.user.is_authenticated():
        if request.POST.get('screening', '') == '' and request.POST.get('submit', '') == '':
            screen = Screening.objects.get(id=rid);
            bookings = Booking.objects.filter(screening_id=screen.id)
            na = {-1: 0}
            nv = {-1: 0}
            vip = {-1: 0}
            for b in bookings:
                na[b.place] = 1;
            seatsTable = "<form method='post'>"
            seatsTable +="<input type='hidden' name='csrfmiddlewaretoken' value='" + get_token(
                request) + \
                         "'/><input type='hidden' name='screening' value='" + str(rid) + "'>" \
                                                                                         "<center><table cellpadding='0' cellspacing='5'>"
            for b in screen.hall.notvalidplaces.split(','):
                nv[int(b)]=1;

            for b in screen.hall.vipplaces.split(','):
                vip[int(b)]=1;
            place = 1;

            for i in range(screen.hall.rows):
                seatsTable += "<tr>"
                for j in range(screen.hall.seats // screen.hall.rows):
                    if na.get(place, 0) == 0 and nv.get(place, 0) == 0:
                        seatsTable = seatsTable + "<td valign='middle'"
                        if vip.get(place, 0) != 0:
                            seatsTable+=" style='background-color:blue;' "
                        seatsTable+="><input style='width: 25px; height: 25px; margin:0;' type='checkbox' name='place" + str(
                            place) + "' value='yes' /></td>"
                    else:
                        if na.get(place, 0) != 0:
                            seatsTable = seatsTable + "<td><span class='glyphicon glyphicon-remove' aria-hidden='true'></span></td>"
                        else:
                            seatsTable = seatsTable + "<td></td>"
                    place += 1
                seatsTable += "</tr>"
            seatsTable += "</table></center><p>&nbsp;</p><p align='center'><input type='submit' style='width: 140px;' class='btn btn-info form-control' value='Забронировать'/></p></form>"

            return render_to_response("cinema/book.html",
                                      RequestContext(request, {'screening': screen, 'bookings': seatsTable
                                                               }))
        else:
            if request.POST.get('submit', '') != '':
                screen = Screening.objects.get(id=rid);
                bookings = Booking.objects.filter(screening_id=screen.id)
                for i in range(screen.hall.seats):
                    if request.POST.get('place' + str(i), '') != '':
                        try:
                            a=Booking.objects.get(person=request.user.username, screening_id=screen.id, place=i)
                            return render_to_response("cinema/error.html", RequestContext(request, {}))
                        except Booking.DoesNotExist:
                            newbook = Booking(person=request.user.username, screening_id=screen.id, place=i)
                            newbook.save()

                return render_to_response("cinema/success.html", RequestContext(request, {}))
            else:
                submitForm = "<form method='post'><table><input type='hidden' name='csrfmiddlewaretoken' value='" + get_token(
                request) + \
                         "'/><input type='hidden' name='submit' value='" + str(rid) + "'>" \
                                                                                         ""
                screen = Screening.objects.get(id=rid);
                for i in range(screen.hall.seats):
                    if request.POST.get('place' + str(i), '') != '':
                        submitForm+="<input type='hidden' name='place"+str(i)+"' value='yes'/>"
                submitForm += "<h3>Вы собираетесь забронировать следующие билеты:</h3>" \
                              "<p>&nbsp;</p>"
                for i in range(screen.hall.seats):
                    if request.POST.get('place' + str(i), '') != '':
                        submitForm+="<p align='center'>"+screen.film.title+", зал:"+screen.hall.title+", место "+str(i)+"</p>"
                submitForm += "<p>&nbsp;</p>"
                if len(list(Booking.objects.filter(person=request.user.username)))>9:
                    submitForm+="<p><i>Кстати, для вас скидка 10%!</i></p>"
                submitForm+="<input type='submit' class='btn btn-primary' value='Подтверждаю!' /><a class='btn btn-warning' href='/cinema/"+rid+"/'>Перевыбор</a></form>"

                return render_to_response("cinema/book.html", RequestContext(request, {'screening': screen, 'bookings': submitForm
                                                               }))
    else:
        return HttpResponseRedirect("/cinema/login/")

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