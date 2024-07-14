import requests
import time
import bs4

from selenium.webdriver.common.by import By
from selenium import webdriver

from src.data_funcs import read_data, write_data, update_data
from src.constants import WORK_DIR, LINK_DELAY
from src.custom_funcs import (
    write_custom_error,
    parse_number_str,
    fill_log_file,
    scroll_down,
    catch_error,
    parse_str,
)


def parse_alloxa_page(driver: webdriver.Chrome, url: str, scroll_times: int, item_type: str):
    data = read_data()

    driver.get(url)
    time.sleep(2)

    scroll_down(driver, scroll_times)

    try:
        text = driver.page_source
        soup = bs4.BeautifulSoup(text, features='lxml')
        cards: bs4.ResultSet = soup.find_all("div", class_="fn_product")
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return

    for card in cards:
        try:
            title_block = card.find("a", class_="product-prev__title")

            title = parse_str(title_block.text)
            price = parse_number_str(card.find("span", class_="product-price__now").text)
            link = title_block.get('href')
            update_data(data, title, price, link, item_type)
        except Exception as exc:
            fill_log_file(WORK_DIR, catch_error(exc))

    write_data(data)
    time.sleep(LINK_DELAY)


def parse_mobilochka(driver: webdriver.Chrome, url: str, scroll_times: int, item_type: str):
    data = read_data()

    driver.get(url)
    scroll_down(driver, scroll_times)
    time.sleep(1)

    try:
        text = driver.page_source
        soup = bs4.BeautifulSoup(text, features='lxml')
        cards = soup.find_all("div", class_="swiper-slide")
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return
    
    for card in cards:
        try:
            title_block = card.find("div", class_="day-product-title")
            link_block = title_block.find("a")

            title = parse_str(link_block.find("span").text)
            price = parse_number_str(card.find("div", class_="day-product-price").find("span").text)
            link = link_block.get('href')
            update_data(data, title, price, link, item_type, 'mobilochka', False)
        except Exception as exc:
            fill_log_file(WORK_DIR, catch_error(exc))
        
    
    write_data(data)
    time.sleep(LINK_DELAY)


# "/" warning
def parse_maxmobiles(url, item_type: str):
    data = read_data()

    page_number = 1

    while True:
        req = requests.get(url + f'page-{page_number}/?items_per_page=300', verify=False)

        if page_number >= 10:
            fill_log_file(
                WORK_DIR,
                write_custom_error(f'Error while parsing maxmobiles. Too much pages, maybe cycling error. URL -> {req}')
            )
            return

        if req.status_code >= 400:
            break

        try:
            soup = bs4.BeautifulSoup(req.text, features='lxml')
            cards = soup.find_all("div", class_="ut2-gl__content")
        except Exception as exc:
            fill_log_file(WORK_DIR, catch_error(exc))
            return

        for card in cards:
            try:
                title_block = card.find("a", class_="product-title")

                title = parse_str(title_block.text)
                price = parse_number_str(card.find("span", class_="ty-price").find("span").text)
                link = title_block.get('href')
                update_data(data, title, price, link, item_type, 'maxmobiles', False)
            except Exception as exc:
                fill_log_file(WORK_DIR, catch_error(exc))

        page_number += 1
        time.sleep(LINK_DELAY)
    
    write_data(data)


def parse_mi_xx(driver):
    data = read_data()

    driver.get('https://mi-xx.ru/smartfony/')
    driver.refresh()
    time.sleep(10)
    try:
        pagination = driver.find_element(By.CLASS_NAME, 'pagination')
        all_items_button = pagination.find_elements(By.CLASS_NAME, 'page-item')[-1]
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return
    
    # try:
    #     all_items_button.click()
    # except:
    #     print('Try click all button')
    
    # try:
    #     all_items_button_link = all_items_button.find_element(By.CLASS_NAME, 'page-link')
    #     all_items_button_link.click()
    # except:
    #     print('Try click all button link')

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        webdriver.ActionChains(driver).move_to_element(all_items_button).click(all_items_button).perform()
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return
    
    try:
        text = driver.page_source
        soup = bs4.BeautifulSoup(text, features='lxml')
        cards = soup.find_all("div", {"calss" : "slider-item__wrapper"})
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return

    for card in cards:
        try:
            title_block = card.find("div", class_="item-card__title")
            link_block = title_block.find("a")

            title = parse_str(link_block.find("span", class_="line-clump").text)
            try:
                price = parse_number_str(card.find("div", class_="item-card__price").find("span", class_="item-card__price__sale").text)
            except:
                pass
            link = 'https://mi-xx.ru' + link_block.get('href')
            update_data(data, title, price, link, 'xiaomi', 'mi_xx', False)
        except Exception as exc:
            fill_log_file(WORK_DIR, catch_error(exc))

    write_data(data)
    time.sleep(LINK_DELAY)


def parse_mi92():
    data = read_data()

    try:
        req = requests.get('https://mi92.ru/smartfonyi/?items_per_page=200', verify=False)
        soup = bs4.BeautifulSoup(req.text, features='lxml')
        cards = soup.find_all("div", class_="ty-column4")
    except Exception as exc:
        fill_log_file(WORK_DIR, catch_error(exc))
        return

    for card in cards:
        try:
            title_block = card.find("a", class_="product-title")

            title = parse_str(title_block.text)
            price = parse_number_str(card.find("span", class_="ty-price-num").text)
            link = title_block.get('href')
            update_data(data, title, price, link, 'xiaomi', 'mi92', False)
        except Exception as exc:
            fill_log_file(WORK_DIR, catch_error(exc))

    write_data(data)
    time.sleep(LINK_DELAY)



def parse_all_sites(driver):
    # iphone
    parse_alloxa_page(driver, 'https://allohastore.ru/smartfony/smartfony-iphone/', 40, 'iphone')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/apple-tehnika-kupit/smartfony-a/', 160, 'iphone')
    parse_maxmobiles('https://maxmobiles.ru/iphone/', 'iphone')

    # apple watch
    parse_alloxa_page(driver, 'https://allohastore.ru/umnye-chasy-i-braslety/chasy-apple-watch/', 20, 'watch')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/apple-tehnika-kupit/chasy-a/', 30, 'watch')

    # macbook
    parse_alloxa_page(driver, 'https://allohastore.ru/noutbuki/apple-macbook-noutbuki/', 20, 'mac')
    parse_maxmobiles('https://maxmobiles.ru/mac/', 'mac')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/apple-tehnika-kupit/noutbuki-a/', 160, 'mac') # 34

    # samsung
    parse_alloxa_page(driver, 'https://allohastore.ru/smartfony/smartfony-samsung-galaxy/', 60, 'samsung')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/samsung-tehnika-kupit/smartfony-s/', 160, 'samsung')

    # xiaomi
    parse_alloxa_page(driver, 'https://allohastore.ru/smartfony/smartfony-xiaomi/', 80, 'xiaomi')
    parse_mi92()
    parse_mobilochka(driver, 'https://mobilo4ka.ru/xiaomi-tehnika-kupit/smartfony-x/', 200, 'xiaomi') # 48
    parse_mi_xx(driver)

    # ps
    parse_alloxa_page(driver, 'https://allohastore.ru/igrovye-pristavki/', 5, 'ps')
    parse_maxmobiles('https://maxmobiles.ru/vse-dlya-igr/', 'ps')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/sony-tehnika-kupit/konsoli-so/', 4, 'ps')

    # dyson
    parse_alloxa_page(driver, 'https://allohastore.ru/tehnika-dlya-doma/feny/', 2, 'dyson')
    parse_alloxa_page(driver, 'https://allohastore.ru/tehnika-dlya-doma/pylesosy/pylesos-dyson/', 2, 'dyson')
    parse_alloxa_page(driver, 'https://allohastore.ru/tehnika-dlya-doma/vypryamitel-dyson/', 2, 'dyson')
    parse_maxmobiles('https://maxmobiles.ru/dyson/', 'dyson')

    # ipad
    parse_alloxa_page(driver, 'https://allohastore.ru/planshety/apple-ipad/', 80, 'ipad')
    parse_maxmobiles('https://maxmobiles.ru/ipad/', 'ipad')
    parse_mobilochka(driver, 'https://mobilo4ka.ru/apple-tehnika-kupit/planshety-a/', 40, 'ipad') # 11
