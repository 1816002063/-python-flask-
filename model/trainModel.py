import pandas as pd
import numpy as np
import csv
from snownlp import SnowNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 假设这里有一个带有情感标签的文本数据集
# 数据格式：(文本, 情感标签)
def getSentiment_data():
    sentiment_data = []
    with open('./target.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        for data in reader:
            sentiment_data.append(data)
    return sentiment_data


def model_train():
    sentiment_data = getSentiment_data()
    # 将文本数据集转换为DataFrame格式
    df = pd.DataFrame(sentiment_data, columns=['text', 'sentiment'])

    # 划分训练集和测试集
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    # 使用TF-IDF特征提取方法将文本数据转换为特征向量
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(train_data['text'])
    y_train = train_data['sentiment']
    X_test = vectorizer.transform(test_data['text'])
    y_test = test_data['sentiment']

    # 使用朴素贝叶斯分类器进行训练
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = classifier.predict(X_test)

    # 计算准确性
    accuracy = accuracy_score(y_test, y_pred)
    print(f"准确性：{accuracy}")

    return vectorizer,classifier


# 情感分类函数
def sentiment_analysis(text):
    vectorizer, classifier = model_train()
    text_vector = vectorizer.transform([text])
    sentiment = classifier.predict(text_vector)[0]
    return sentiment


if __name__ == "__main__":
    # 测试
    input_text = "什么破烂玩意？"
    result = sentiment_analysis(input_text)
    print(SnowNLP(input_text).sentiments)
    print(result)  # Output: '积极'
