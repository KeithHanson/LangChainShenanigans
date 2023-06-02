#!./venv/bin/python

import os
import click

from dotenv import load_dotenv
load_dotenv()

from mmpy_bot import Bot, Settings
from plugins.default import Default

plugin_names = ['default', 'chat-with-duckduckgo-search', 'knowledge-topic-importer', 'link-helper']
plugin_explanations = [
        "A vanilla ChatGPT experience.",
        "A vanilla ChatGPT experience but with DuckDuckGo Search for current information.",
        "A way to import data into your pinecone API. Allows you to assign a topic to each imported knowledge.",
        "Link Helper is a bot to scratch an itch - pull all of the links I read together in one spot, summarize at end of day, help the knowledge stick."
        ]


plugins_string = "|".join(plugin_names)

@click.command()
@click.option('--with-plugin-explanations/--without-plugin-explanations', 
        default=False,
        help="Explain each plugin choice")
@click.option('--plugin', 
        type=click.Choice(plugin_names, case_sensitive=False),
        default="default",
        help="The plugin to run defining the bot behavior")
@click.option('--dotenv-location', 
        default=".env",
        help="Sometimes you need different variables for different bots. Use this to load the right ones.")
@click.option('--bot-mattermost-url', 
        prompt="Required. MatterMost URL (like http://dev.keithhanson.io:8065)",
        help="Specify the server for the bot to join.")
@click.option('--bot-token', 
        prompt="Required. MatterMost Bot Token (like cidxxxxxxxxxxxxxxxx)",
        help="You'll need a bot token for every bot.")
@click.option('--bot-team', 
        prompt="Required. MatterMost Team to join (like personal or company_name)",
        help="Specify the team on the server for the bot to join.")
def run(plugin, dotenv_location, bot_mattermost_url, bot_token, bot_team, with_plugin_explanations):
    if with_plugin_explanations:
        for idx, name in enumerate(plugin_names):
            click.echo(f'{name}: {plugin_explanations[idx]}')
        return

    bot = Bot(
        settings=Settings(
            MATTERMOST_URL = bot_mattermost_url,
            MATTERMOST_PORT = 8065,
            MATTERMOST_API_PATH = '/api/v4',
            BOT_TOKEN = bot_token,
            BOT_TEAM = f'<{bot_team}>',
            SSL_VERIFY = False,
        ),
        plugins=[Default()],
    )

    bot.run()

if __name__ == '__main__':
    run() 
