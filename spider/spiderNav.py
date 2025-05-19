import requests
import csv
import os
import numpy as np


def init():
    if not os.path.exists('navData.csv'):
        with open('navData.csv','w',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'typeName',
                'gid',
                'containerid'
            ])


def wirterRow(row):
        with open('navData.csv','a',encoding='utf8',newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow(row)

def get_html(url):
    headers  = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie':'SUB=_2AkMQrBhpf8NxqwFRmfAcyWPgaYVyygjEieKm8OmyJRMxHRl-yT9kqlE_tRB6Oyw2hrlbBv-dBkhiVUSdQsI_4At8QLLe; ALF=02_1720370966; PC_TOKEN=b01fb1ca93; XSRF-TOKEN=aNK5D5uZwDJmSf4SuSXwDsQc-E; WBPSESS=fhlE7lUFBip5iXsQIeNCGCIl8MwhBLR8p6gZc1QfOFfiAKplJ0QoP2ZQ3uqYgCC10ca9CTvbdVZz5zXtctNdCxFX4h9YLmk73SmOfy5FMaQ_mvQ8OfiUrsg4s_GiWrWIL9zz2A0i2s_mya4weV9PtLtEYthIqgnS6cytbxlV'
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        wirterRow([
            navName,
            gid,
            containerid,
        ])
    print('获取类别完成~')


if __name__ == '__main__':
    url = 'https://weibo.com/ajax/feed/allGroups'
    init()
    response = get_html(url)
    if response:
        with open('navData.csv', 'w', encoding='utf8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])
        parse_json(response)