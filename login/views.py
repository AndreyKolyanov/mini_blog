#coding:utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from account.models import User


def logging(request, error=0):
    template = loader.get_template('login.html')
    message = ''
    show_message = False
    if error == str(1):
        message = u'Ошибка: аккаунт заблокирован'
        show_message = True
    if error == str(2):
        message = u'Ошибка: логин и пароль не совпадают'
        show_message = True
    context = RequestContext(request, {
        'message':message, 'show_message': show_message,
    })
    return HttpResponse(template.render(context))


def log(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/id'+str(user.id))
        else:
            return HttpResponseRedirect('/login/error/1')
    else:
        return HttpResponseRedirect('/login/error/2')


def new_user(request, error=0):
    template = loader.get_template('register.html')
    message = ''
    show_message = False

    if error == str(1):
        message += u'Ошибка: логин занят\n'
        show_message = True
    if error == str(2):
        message += u'Ошибка: пароли не совпадают\n'
        show_message = True
    if error == str(3):
        message += u'Ошибка: заполнтие все поля\n'
        show_message = True

    context = RequestContext(request, {
        'message':message, 'show_message': show_message,
    })
    return HttpResponse(template.render(context))


def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    password_again = request.POST['password_again']

    if password == '' or username == '' or password_again == '':
        return HttpResponseRedirect('/registration/error/3')

    if password != password_again:
        return HttpResponseRedirect('/registration/error/2')
    for u in User.objects.all():
        if u.get_username() == username:
            return HttpResponseRedirect('/registration/error/1')
    user = User.objects.create_user(username=username, password=password)
    user.save()
    user = authenticate(username=username, password=password)
    login(request, user)
    return HttpResponseRedirect('/settings')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/users/')
