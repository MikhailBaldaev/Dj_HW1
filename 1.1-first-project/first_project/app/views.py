import os

from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    dir_list = os.listdir(r'C:\Users\emper\Desktop\Dj_HW1\dj-homeworks\1.1-first-project\first_project')
    result = [i for i in dir_list]
    return HttpResponse(f"Список файлов в рабочей директории: {', '.join(result)}")
    #raise NotImplemented
