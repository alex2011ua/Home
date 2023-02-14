import json

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from house.core.Telegram import bot

from .viber_bot import send_viber


@csrf_exempt
def trx_bot(request):
    try:
        json_answer = json.loads(request.body.decode("utf-8"))
        if json_answer["event"] == "message":
            message = json_answer["message"]["text"]
            bot.send_message(message)
            send_viber(message)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=200)
    except Exception as err:
        bot.send_message(err)


"""
if request.method == "GET":
    bot.send_message('GET methodd')
    viber = json.loads(request.body.decode('utf-8'))
    if viber['event'] == 'conversation_started':
        bot.send_message("Приветствую пользователя")
        conversation(viber) #Обработка запроса - обзор функции следующий абзац.

    elif viber['event'] == 'webhook':
        # print(viber)
        # print("Webhook успешно установлен")
        return HttpResponse(status=200)
    elif viber['event'] == 'message':
        #print(viber)
        #print("Webhook успешно установлен")
        return HttpResponse(status=200)

    else:
        print("Это не Webhook - пробуй еще раз, или используй POSTMAN")
        return HttpResponse(status=500)
    return HttpResponse(status=200)


def conversation(viber):
    id = viber['user']['id']
    if viber['subscribed']:
        send_text(id, 'ВЫ УЖЕ ПОДПИСАНЫ')
    else:
        send_text(id, 'Что умеет этот бот?\n\nЗависит от ваших идей. Отправь мне что угодно и присоединяйся...')
"""
