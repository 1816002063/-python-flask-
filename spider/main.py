from spiderContent import start as contentStart
from spiderComments import start as commentsStart
import os
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1/wb?charset=utf8mb4')


def save_to_sql():
    try:
        articleOldPd = pd.read_sql('select * from article', engine)
        articleNewPd = pd.read_csv('./articleData.csv')
        concatPd = pd.concat([articleNewPd, articleOldPd], join='inner')
        concatPd = concatPd.drop_duplicates(subset='id', keep='last')
        concatPd.to_sql('article', con=engine, if_exists='replace', index=False)

        commentOldPd = pd.read_sql('select * from comments', engine)
        commentNewPd = pd.read_csv('./commentsData.csv')
        concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
        concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
        concatCommentPd.to_sql('comments', con=engine, if_exists='replace', index=False)
    except:
        articleNewPd = pd.read_csv('./articleData.csv')
        commentNewPd = pd.read_csv('./commentsData.csv')
        articleNewPd.to_sql('article', con=engine, if_exists='replace', index=False)
        commentNewPd.to_sql('comments', con=engine, if_exists='replace', index=False)

    # os.remove('./articleData.csv')
    # os.remove('./commentsData.csv')

def main():
    print('正在爬取文章内容...')
    contentStart(5, 5)
    print('正在爬取评论内容...')
    commentsStart()
    print('爬取完毕正在存储中...')
    save_to_sql()


if __name__ == '__main__':
    main()
