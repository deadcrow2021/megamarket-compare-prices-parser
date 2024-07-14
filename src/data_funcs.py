from difflib import SequenceMatcher
import json
import os

from src.constants import WORK_DIR
from src.custom_funcs import format_price
from src.filter_funcs import (
    default_filter,
    filter_samsung,
    filter_iphone,
    filter_xiaomi,
    filter_watch,
    filter_dyson,
    filter_ipad,
    filter_mac,
    filter_ps,
)


def read_data() -> dict:
    with open(WORK_DIR / 'data.json') as file:
        data = json.loads(
            file.read()
        )

    return data


def write_data(data: dict):

    if data:
        with open(os.path.join(WORK_DIR / 'data.json'), 'w') as file:
            json_data = json.dumps(data)
            file.write(json_data)


def update_data(
    data: dict,
    name: str,
    price: str,
    link: str,
    item_type,
    shop=None,
    alloxa_shop=True) -> dict:

    if alloxa_shop:
        elem = data['alloxa']
        elem = elem[item_type]
    else:
        elem = data['others']
        elem = elem[item_type]
        elem = elem[shop]
    
    elem.update({name: [price, link]})


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def compare_data(result_data: dict, item_type: str, shop: str, filter_func = default_filter, min_price_diff: float = 0, min_ratio: float = 0):
    data = read_data()

    my_data: dict = data['alloxa'][item_type]
    data: dict = data['others'][item_type][shop]

    for my_title, my_price_link in my_data.items():
        best_ratio: tuple = ('', 0) # item, ratio

        my_price = my_price_link[0]
        my_link = my_price_link[1]

        my = filter_func(my_title)

        for item, price_link in data.items(): # item: [price, link]
            ratio = similar(my, filter_func(item))
            
            if best_ratio[1] < ratio:
                best_ratio = (item, ratio)
        
        best_ratio_item_title = best_ratio[0]
        best_ratio_item_price, best_ratio_item_link = data[best_ratio_item_title]

        if my_price > best_ratio_item_price and \
                        (best_ratio_item_price / my_price > min_price_diff) and \
                        best_ratio[1] > min_ratio:
            result_data.setdefault((my_title, format_price(my_price), my_link), []).append(
                (
                    best_ratio_item_title,
                    format_price(best_ratio_item_price),
                    best_ratio_item_link
                )
            )


def collect_data():
    data = {}

    compare_data(data, 'iphone', 'maxmobiles', filter_iphone, 0.85, 0.85)
    compare_data(data, 'iphone', 'mobilochka', filter_iphone, 0.95, 0.80)
    
    compare_data(data, 'watch', 'mobilochka', filter_watch, 0.80, 0.799)
    
    compare_data(data, 'mac', 'maxmobiles', filter_mac, 0.90, 0.8)
    compare_data(data, 'mac', 'mobilochka', filter_mac, 0.90, 0.8)

    compare_data(data, 'samsung', 'mobilochka', filter_samsung, 0.82, 0.8)
    
    compare_data(data, 'xiaomi', 'mobilochka', filter_xiaomi, 0.8, 0.8)
    compare_data(data, 'xiaomi', 'mi_xx', filter_xiaomi, 0.8, 0.8)
    compare_data(data, 'xiaomi', 'mi92', filter_xiaomi, 0.8, 0.8)
    
    compare_data(data, 'ps', 'mobilochka', filter_ps, 0.8, 0.75)
    compare_data(data, 'ps', 'maxmobiles', filter_ps, 0.8, 0.75)

    compare_data(data, 'dyson', 'maxmobiles', filter_dyson, 0, 0.7)

    compare_data(data, 'ipad', 'mobilochka', filter_ipad, 0.9, 0.7)
    compare_data(data, 'ipad', 'maxmobiles', filter_ipad, 0.9, 0.7)

    return data


def form_messages(data: dict) -> str:
    messages_list = []

    for my_item, other_items in data.items():
        msg = ''
        
        title, price, link = my_item
        
        msg += f'Alloxa:\n{title} - {price} - [{link}]\n'
        msg += f'Другие:\n'
        
        for other in other_items:
            title_o, price_o, link_o = other
            msg += f'{title_o} - {price_o} - [{link_o}]\n'
        
        messages_list.append(msg)

    messages = '\n=====\n\n'.join(messages_list)
    return messages
