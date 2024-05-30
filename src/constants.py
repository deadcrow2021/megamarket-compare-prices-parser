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

# path = Path(application_path)
# # WORK_DIR = path.parent.absolute()
# WORK_DIR = path


TOKEN = '7273513520:AAEGzRQsvbRgzVQa5acCxARdQB-oF_Y3oao'

CHAT_ID = -1002176388996
# -1002176388996


def read_config() -> dict:
    with open(WORK_DIR / 'config.json', 'r') as file:
        data = json.loads(
            file.read()
        )

    return data


config = read_config()

LINK_DELAY = config['link_delay']

PARSE_CYCLE_DELAY = config['parse_cycle_delay']
