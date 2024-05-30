from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib3
import asyncio
import lxml
import json

from src.constants import WORK_DIR, CHAT_ID, PARSE_CYCLE_DELAY
from src.custom_funcs import fill_log_file, catch_error
from src.data_funcs import collect_data, form_messages
from src.parsers import parse_all_sites
from bot import bot


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-notifications')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-proxy-certificate-handler")
options.add_argument("--disable-content-security-policy")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_size(1600, 900)


async def main():
    while True:
        try:
            driver.delete_all_cookies()
            driver.get('chrome://settings/clearBrowserData')
            await asyncio.sleep(2)
            driver.find_element(By.XPATH, '//settings-ui').send_keys(Keys.ENTER)
            await asyncio.sleep(2)
        except Exception as exc:
            print('Error in deleting cookies')
            fill_log_file(WORK_DIR, catch_error(exc))

        messages_list = []

        try:
            parse_all_sites(driver)
        except Exception as exc:
            print('Error in parsing sites')
            fill_log_file(WORK_DIR, catch_error(exc))

        try:
            data = collect_data()
        except Exception as exc:
            data = {}
            print('Error in collecting data')
            fill_log_file(WORK_DIR, catch_error(exc))

        try:
            messages = form_messages(data)
        except Exception as exc:
            messages = ''
            print('Error in forming messages')
            fill_log_file(WORK_DIR, catch_error(exc))

        messages_list.extend([messages[0+i : 4000+i] for i in range(0, len(messages), 4000)])


        i = 0
        while i < len(messages_list):
            try:
                await bot.send_message(CHAT_ID, messages_list[i])
                await asyncio.sleep(0.2)
                i += 1

            except:
                await asyncio.sleep(2)

        await asyncio.sleep(60 * PARSE_CYCLE_DELAY)


if __name__ == '__main__':
    asyncio.run(main())

