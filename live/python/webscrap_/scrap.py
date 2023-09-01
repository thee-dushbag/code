from bs4 import BeautifulSoup, Tag
from yarl import URL
from more_itertools import flatten
import httpx as hx, csv

HOST, PORT = 'localhost', 5052
url = URL(f'http://{HOST}:{PORT}')

def get_headers(path: str):
    content = hx.get(str(url.with_path(path))).content
    soup = BeautifulSoup(content.decode(), 'lxml')
    htags = [f'h{u}' for u in range(1, 7)]
    headers = [soup.find_all(htag) for htag in htags]
    return tuple(flatten(headers))

def _get_user_data(tag: Tag):
    user_attrs = tag.find_all('div', class_='user-attr')
    all_user_attrs = {}
    for user_attr in user_attrs:
        key = user_attr.find('span', class_='attr-key').text.lower().strip()
        value = user_attr.find('span', class_='attr-value').text.strip()
        all_user_attrs[key] = value
    return all_user_attrs

def get_users(path: str):
    content = hx.get(str(url.with_path(path))).content
    soup = BeautifulSoup(content.decode(), 'lxml')
    users = soup.find('div', class_='users')
    return [_get_user_data(user) for user in users.find_all('div', class_='user')]


def save_users_csv(csv_file: str, users: list[dict], field_names=None):
    if users and not field_names:
        field_names = users[0].keys()
    else: raise Exception(users, field_names)
    with open(csv_file, 'w') as file:
        csv_ = csv.DictWriter(file, field_names)
        csv_.writeheader()
        csv_.writerows(users)


def get_users_csv(csv_file: str):
    with open(csv_file) as file:
        csv_ = csv.DictReader(file)
        return list(csv_)