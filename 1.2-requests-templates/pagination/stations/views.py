from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator

import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_num = int(request.GET.get('page', 1))
    stations = list()
    with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            temp_dict = {key: value for (key, value) in row.items() if key in ['Name', 'Street', 'District']}
            stations.append(temp_dict)

    paginator = Paginator(stations, 10)
    context_page = paginator.get_page(page_num)

    context = {
         'bus_stations': context_page,
         'page': page_num,
    }
    return render(request, 'stations/index.html', context)
