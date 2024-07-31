from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, Redis
from environs import Env
from gigachat import GigaChat
env =  Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')
ADMIN_IDS = list(map(int,env.list('ADMIN_IDS')))
GIGACHAT_API_KEY = env('GIGACHAT_API_KEY')
BOT_DESCRIPTION = """Этот бот – ассистент-нейросеть, помогающий командам создавать новые продукты или решать проблемы.
Добавьте его в группу и поднимите эффективность работы!"""
BOT_USERNAME="@example_bot"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="MARKDOWN"))
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis) 
dp = Dispatcher(storage=storage)
giga = GigaChat(credentials= GIGACHAT_API_KEY, verify_ssl_certs=False)