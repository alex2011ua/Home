import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .avto_api import analiz_avto, get_list_car, make_baza_avto


def ajax(request):
    """
    возвращает количество найденыз авто
    :param request:
    :return: count_avto
    """
    type_en = []
    gearbox = []
    for item in request.POST:
        if item == "benz":
            type_en.append(1)
        elif item == "dizel":
            type_en.append(2)
        elif item == "gaz":
            type_en.append(4)
        elif item == "elektro":
            type_en.append(6)
        elif item == "mex":
            gearbox.append(1)
        elif item == "avtomat":
            gearbox.append(2)
        elif item == "tip":
            gearbox.append(3)
    params = {
        "s_yers": [
            request.POST.get("s_yers"),
        ],
        "po_yers": [
            request.POST.get("po_yers"),
        ],
        "price_ot": int(request.POST.get("price_ot")),
        "price_do": int(request.POST.get("price_do")),
        "type": type_en,
        "gearbox": gearbox,
    }
    list_car = get_list_car(params)
    return HttpResponse(list_car["count_avto"])


def ajax_analiz(request):
    """
    добавляет авто в кеш
    :param request:
    :return:
    """
    avtos = request.POST.getlist("list_avto[]")
    for avto in avtos:
        status = analiz_avto(avto)
        if status["status"] != 200:
            print(status["status"])
    return JsonResponse({"status": 200})


def ajax_zvit(request):
    """
    формирует HTML с карточками машин
    :param request:
    :return:
    """
    avtos = request.POST.getlist("baza[]")
    sort_list = make_baza_avto(avtos)

    return render(request, "selection_avto/ca.html", sort_list)
