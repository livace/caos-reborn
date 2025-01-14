from utils.constants import FILES_PATH, CONFIG_PATH, COOKIES_PATH, LINKS_PATH

import os
import requests
import configparser
import json, pickle
from bs4 import BeautifulSoup as bs
from clint.textui import puts, colored, prompt


def init():
    if not os.path.exists(FILES_PATH):
        os.mkdir(FILES_PATH)

    open(CONFIG_PATH, 'a').close()
    open(COOKIES_PATH, 'a').close()
    open(LINKS_PATH, 'a').close()

    login = prompt.query('Tell me your login: ')
    password = prompt.query('Tell me your password: ')
    group = prompt.query('Tell me you group number from the caos.ejudge.ru: ')

    config = configparser.ConfigParser()
    config['Credentials'] = {}
    config['Group'] = {}

    config['Credentials']['login'] = login
    config['Credentials']['password'] = password
    config['Group']['group_number'] = group

    open(CONFIG_PATH, 'a').close()
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

    init_session()


def init_session():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    credentials = {
        'login': config['Credentials']['login'],
        'password': config['Credentials']['password']
    }

    session = requests.session()

    url = 'https://caos.ejudge.ru/ej/client?contest_id=1{:02d}'.format(int(config['Group']['group_number']))
    start_page = session.post(
        url,
        data=credentials,
        headers=dict(referer=url),
    )

    soup = bs(start_page.content, 'html.parser')
    if 'Permission denied' in soup.text:
        puts(colored.red("Invalid login or password. Run './caos init' again with correct credentials"))
        exit(0)

    links = soup.find_all('a', {'class': 'menu'})[:-1]

    open(LINKS_PATH, 'a').close()
    with open(LINKS_PATH, 'w') as linksfile:
        linksfile.write(json.dumps(dict(map(lambda x: (x.text, x['href']), links)), indent=2))

    open(COOKIES_PATH, 'a').close()
    with open(COOKIES_PATH, 'wb') as cookiesfile:
        pickle.dump(session.cookies, cookiesfile)
