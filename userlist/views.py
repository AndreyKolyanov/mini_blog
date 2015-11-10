from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from account.models import User


def user_list(request):
    if request.user.is_authenticated():
        login = request.user.get_username()
        is_login = True
    else:
        is_login = False
        login = ''
    users = []
    for u in User.objects.order_by('first_name').all():
        users.append(u)
    template = loader.get_template('user_list.html')
    context = RequestContext(request, {
        'users': users, 'is_login': is_login, 'login': login,
    })
    return HttpResponse(template.render(context))