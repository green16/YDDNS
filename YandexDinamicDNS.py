#!/usr/bin/python3
import json
import http.client
from urllib.parse import urlencode
from urllib.request import urlopen, Request


def get_settings():
    with open('settings.json') as data_file:
        data = json.load(data_file)
        return  data

def get_ip():
    connection = http.client.HTTPConnection('ident.me')
    connection.request("GET", "")

    r1 = connection.getresponse()

    data = r1.read()
    connection.close()
    return data.decode()

def get_record(d):
    url = 'https://pddimp.yandex.ru/api2/admin/dns/list?'
    post_fields = {
        'domain' : d,
        'token' : token
    }
    request = Request(url, urlencode(post_fields).encode())
    request.method = "GET"
    return json.loads(urlopen(request).read().decode())


ip = get_ip()
try:
    last_ip = open("lastip", mode='r+')
except IOError:
    last_ip = open("lastip", mode='w')
if last_ip.read() != ip:
    token = get_settings()["token"]
    domain = get_settings()["domain"]
    for d in domain:
        record_id = get_record(d)
        if record_id['success'] == 'ok':
            id=''
            for r in record_id['records']:
                if r['domain'] == d:
                 id=r['record_id']
                 url = 'https://pddimp.yandex.ru/api2/admin/dns/edit'
                 post_fields = {
                    'domain': d,
                    'record_id': id,
                    'content': ip,
                    'token': token
                    }

                 request = Request(url, urlencode(post_fields).encode())
                 data = urlopen(request).read().decode()
    last_ip.write(ip)
    last_ip.close()
