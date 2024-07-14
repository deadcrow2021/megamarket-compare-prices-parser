from pathlib import Path
import json
import sys
import os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

path = Path(application_path)
WORK_DIR = path.parent.absolute()


TOKEN = 'bot_api_key'

CHAT_ID = -10010000000


def read_config() -> dict:
    with open(WORK_DIR / 'config.json', 'r') as file:
        data = json.loads(
            file.read()
        )

    return data


config = read_config()

LINK_DELAY = config['link_delay']

PARSE_CYCLE_DELAY = config['parse_cycle_delay']
