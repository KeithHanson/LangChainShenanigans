import os

from dotenv import load_dotenv
load_dotenv()

from mmpy_bot import Bot, Settings
from plugins.default import Default

bot = Bot(
    settings=Settings(
        MATTERMOST_URL = "http://dev.keithhanson.io",
        MATTERMOST_PORT = 8065,
        MATTERMOST_API_PATH = '/api/v4',
        BOT_TOKEN = os.environ["BOT_TOKEN"],
        BOT_TEAM = "<Personal>",
        SSL_VERIFY = False,
    ),
    plugins=[Default()],
)
bot.run()
