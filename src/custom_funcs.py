from selenium import webdriver
import traceback
import datetime
import time
import os


def parse_number_str(text: str) -> int:
    list_of_digits = [x for x in text if x.isdigit()]
    number = ''.join(list_of_digits)
    
    return int(number)


def format_price(price):
    price_formated = '{:,}'.format(int(price))
    price_formated = price_formated.replace(',', '.') + ' \u20BD'

    return price_formated


def parse_str(text: str):
    text = text.encode("ascii", "ignore").decode()
    text = text.strip().replace('  ', ' ')
    return text


def scroll_down(driver: webdriver.Chrome, times: int):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)


def catch_error(exception, info = '') -> str:
    message = ''
    error_message = f'{exception} | {traceback.format_exc()}'

    if info:
        message = f'INFO --> {info} <--\n\n'

    message += f'ERROR --> {error_message.rstrip()} <--'

    return message


def write_custom_error(error_text) -> str:
    message = f'ERROR --> {error_text} <--'

    return message


def fill_log_file(dir_path, text = ''):
    date = datetime.datetime.now()
    
    today = date.strftime('%d_%m_%Y')
    now_time = date.strftime('%H:%M:%S')

    path_to_logs = os.path.join(dir_path, 'logs')
    path_to_file = os.path.join(path_to_logs, f'errors_{today}.log')

    if not os.path.isdir(path_to_logs):
        os.makedirs(path_to_logs, exist_ok=True)

    if os.path.isfile(path_to_file):
        with open(path_to_file, 'a') as file:
            file.write(now_time + ' - ' + text + '\n\n')
    else:
        with open(path_to_file, 'w') as file:
            file.write(now_time + ' - ' + text + '\n\n')
