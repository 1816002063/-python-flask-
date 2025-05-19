import time
import requests
import csv
import os
from datetime import datetime


def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv', 'w', encoding='utf8', newline='') as csvfile:
            wirter = csv.writer(csvfile)
            wirter.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])


def wirterRow(row):
    with open('commentsData.csv', 'a', encoding='utf8', newline='') as csvfile:
        wirter = csv.writer(csvfile)
        wirter.writerow(row)


def get_html(url, id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Cookie': 'SUB=_2A25LZ0pGDeRhGeFG41sU9S7OyTmIHXVoHcOOrDV8PUNbmtAGLVrskW9NeJyF1EwU4M6Mwu9-6gpcbZqbZsenWnXr; ALF=02_1720370966; PC_TOKEN=b01fb1ca93; XSRF-TOKEN=6bMnUs3SoYsFReAgdjqzwN-E; WBPSESS=ExkktpaA-4CRe1RiH-_VWofdlYS3vZKOZC5ExzH8lmCoZvoq6OkKLXL5o5b6_jEIUjHP9lhX8MJeTp9MidkUVeQYqAc8wK0NeCjV5m0SQu0RQVD00GTUm9D0mMJWLvVOduVY_ty1FHPl3CIIyGe_Ew=='
    }
    params = {
        'is_show_bulletin': 2,
        'id': id
    }
    print(url)
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_json(response, articleId):
    commentList = response['data']
    for comment in commentList:
        created_at = datetime.strptime(comment['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        like_counts = comment['like_counts']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location'].split(' ')[0]
        authorAvatar = comment['user']['avatar_large']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '无'
        content = comment['text_raw']
        wirterRow([
            articleId,
            created_at,
            like_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar,
        ])


def start():
    init()
    url = 'https://weibo.com/ajax/statuses/buildComments'
    with open('./articleData.csv', 'r', encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for index, article in enumerate(reader, start=1):
            articleId = article[0]
            print(f'{index} 正在爬取id值为{articleId}的文章评论')
            time.sleep(0.4)
            response = get_html(url, articleId)
            parse_json(response, articleId)


if __name__ == '__main__':
    start()
