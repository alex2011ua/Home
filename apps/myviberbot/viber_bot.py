import os

from dotenv import load_dotenv
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv("viber_token", os.environ.get("viber_token"))
bot_configuration = BotConfiguration(
    name="AlexUA",
    avatar="http://alexua.pp.ua/static/start/favico.jpg",
    auth_token=token,
)
viber = Api(bot_configuration)


def send_viber(text):
    viber.send_messages(to="/VKJ0H7uV9L0SBS0KG821g==", messages=[TextMessage(text=text)])
