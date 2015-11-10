from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.template import RequestContext, loader
from django.utils.timezone import now
import datetime
from records.models import Record
from .models import User


def user_profile(request, user_id, page=1):
    if request.user.is_authenticated():
        login = request.user.get_username()
        is_login = True
    else:
        is_login = False
        login = ''

    records = []
    user = User.objects.get(id=user_id)

    if request.user == user:
        add_record = True
    else:
        add_record = False

    page = int(page)
    limit = (page * 5)
    offset = limit - 5

    next = page
    prev = page

    if page != 1:
        prev = page - 1
        prev_avalible = True
    else:
        next = page + 1
        prev_avalible = False

    if len(Record.objects.filter(author=user)) <= limit:
        next_avalible = False
    else:
        next = page + 1
        next_avalible = True

    for r in Record.objects.filter(author=user)[offset:limit]:
        records.append(r)

    template = loader.get_template('profile.html')
    context = RequestContext(request, {
        'profile': user,
        'records': records,
        'login': login,
        'is_login': is_login,
        'add_record': add_record,
        'prev': '/id' + user_id + '/' + str(prev) + '/',
        'next': '/id' + user_id + '/' + str(next) + '/',
        'prev_avalible': prev_avalible,
        'next_avalible': next_avalible,
    })
    return HttpResponse(template.render(context))


def add(request):
    if request.is_ajax():
        text = request.POST['record']
        record = Record(text=text, author=request.user, date=now())
        record.save()
        return JsonResponse({"text": record.text, "id": record.id, "date": record.date.strftime("%d.%m.%Y %H:%M"),
                             "author_id": record.author.id, "author_name": record.author.get_full_name(),
                             "author_alias": record.author.username})


def update(request):
    if request.is_ajax():
        text = request.POST['record']
        record_id = request.POST['record_id']
        record = Record.objects.get(id=record_id)
        record.text = text
        record.save()
        return JsonResponse({"text": record.text, "id": record.id, "date": record.date.strftime("%d.%m.%Y %H:%M"),
                             "author_id": record.author.id, "author_name": record.author.get_full_name(),
                             "author_alias": record.author.username})


def remove(request):
    if request.is_ajax():
        record_id = request.POST['record_id']
        record = Record.objects.get(id=record_id)
        record.delete()
        return HttpResponse(record_id)


def subscribe(request):
    if request.is_ajax():
        id = request.POST['user_id']
        user = User.objects.get(id=id)
        request.user.subscribe_to.add(user)
        return HttpResponse('success')


def user_settings(request):
    if request.user.is_authenticated():
        is_login = True
        login = request.user.get_username()
        template = loader.get_template('settings.html')
        user = request.user
        context = RequestContext(request, {
            'profile': user,
            'is_login': is_login,
            'login': login,
            'photo': user.photo_medium,
        })
        return HttpResponse(template.render(context))
    else:
        return Http404()


def change_settings(request):
    firstname = request.POST['firstname']
    surname = request.POST['surname']
    email = request.POST['email']
    phone = request.POST['phone']
    about = request.POST['about']
    date = request.POST['date_of_birth']
    user = request.user
    user.first_name=firstname
    user.last_name=surname
    user.email=email
    user.phone=phone
    user.about=about
    user.date_of_birth=date
    if request.FILES:
        image = request.FILES['photo']
        user.photo=image
    user.save()
    return HttpResponseRedirect('/settings/')
