import datetime
import os

import requests
from django.core.exceptions import ObjectDoesNotExist
from dotenv import load_dotenv

from selection_avto.models import Avto

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
apy_key = os.getenv("apy_key", os.environ.get("apy_key"))

url_search = "https://developers.ria.com/auto/search"
url_info = "https://developers.ria.com/auto/info"


def get_list_car(params):
    """
    получает словарь параметров запроса и возвращает ответ
    :param params: dict словарь параметров запроса
    :return: dict количество авто в запросе и список ID авто
    """
    payload = {
        "api_key": apy_key,
        "category_id": 1,
        "s_yers": [2016],
        "po_yers": [2017],
        "price_ot": 11000,
        "price_do": 13500,
        "type": [
            # 1,  # бенз
            # 2,  # дизель
            # 4,  # газ
            6,  # электро
        ],
        "gearbox": [
            1,  # механика
            2,  # автомат
            3,  # титпроник
        ],
        "countpage": 100,
        "abroad": 2,  # Не отображать авто которые находяться не в Украине
        "custom": 1,  # Не отображать нерастаможенные авто
        "with_photo": 1,  # Только с фото
        "damage": 1,  # не поврежден
    }
    payload.update(params)
    zapros_po_param = requests.get(url_search, params=payload)
    if zapros_po_param.status_code == 200:
        j = zapros_po_param.json()
        count_avto = int(j["result"]["search_result"]["count"])
        list_cars = j["result"]["search_result"]["ids"]
        return {"status": 200, "count_avto": count_avto, "list_cars": list_cars}
    else:
        return {"status": zapros_po_param.status_code}  # 429 (слишком много запросов)


def analiz_avto(car):
    """
    проверяет наличие авто в кеше
    :param car: ID авто
    :return:
    """
    params = {"api_key": apy_key, "auto_id": car}
    try:
        Avto.objects.get(autoId=car)
    except ObjectDoesNotExist:
        info_avto = requests.get(url_info, params=params)
        if info_avto.status_code != 200:
            return {
                "status": info_avto.status_code,
            }
        car_add_baze(info_avto)
    return {
        "status": 200,
    }


def make_baza_avto(car_list):
    """
    перебор списка авто для анализа
    :param car_list: list
    :return: list
    """
    baza_avto = {}
    for car in car_list:
        params = {"api_key": apy_key, "auto_id": car}
        try:
            car_baze = Avto.objects.get(autoId=car)
        except ObjectDoesNotExist:
            info_avto = requests.get(url_info, params=params)
            if info_avto.status_code != 200:
                return {"status": info_avto.status_code, "baza_avto": baza_avto}
            car_baze = car_add_baze(info_avto)

        name_avto = car_baze.markName + " " + car_baze.modelName

        if name_avto in baza_avto:
            #  высчитываем среднюю цену
            price = int(car_baze.USD)
            baza_avto[name_avto]["price"] = (
                baza_avto[name_avto]["count_item"] * baza_avto[name_avto]["price"] + price
            ) // (baza_avto[name_avto]["count_item"] + 1)
            raceInt = int(car_baze.raceInt)
            baza_avto[name_avto]["raceInt"] = (
                baza_avto[name_avto]["count_item"] * baza_avto[name_avto]["raceInt"] + raceInt
            ) // (baza_avto[name_avto]["count_item"] + 1)

            baza_avto[name_avto]["count_item"] += 1
        else:
            try:
                baza_avto[name_avto] = {
                    "count_item": 1,
                    "linkToView": car_baze.linkToView,
                    "foto": car_baze.foto,
                    "price": int(car_baze.USD),
                    "year": car_baze.year,
                    "raceInt": int(car_baze.raceInt),
                    "bodyId": car_baze.bodyId,
                }
            except TypeError as err:
                print(err)
    baza_avto = sort_baza(baza_avto)
    return {"status": 200, "baza_avto": baza_avto[:12]}


def sort_baza(baza):
    """
    сортирует словарь и возвращает отсортированный список
    :param baza: dict
    :return: list
    """
    list_to_sort = []
    for name, value in baza.items():
        list_to_sort.append(
            (
                value["count_item"],
                value["price"],
                name,
                value["foto"],
                value["year"],
                value["linkToView"],
                value["raceInt"],
                value["bodyId"],
            )
        )
    sort_list = sorted(list_to_sort, reverse=True)
    return sort_list


def car_add_baze(avto):
    info_json = avto.json()
    avto_query = Avto(
        date_message=datetime.datetime.now(),
        autoId=info_json["autoData"]["autoId"],
        raceInt=info_json["autoData"].get("raceInt"),
        USD=info_json.get("USD"),
        year=info_json["autoData"].get("year"),
        markName=info_json["markName"],
        modelName=info_json["modelName"],
        linkToView=info_json["linkToView"],
        foto=info_json["photoData"]["seoLinkB"],
        bodyId=info_json["autoData"].get("bodyId"),
    )
    avto_query.save()
    return avto_query
