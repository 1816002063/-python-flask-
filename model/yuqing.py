from snownlp import SnowNLP
import csv
from cutComments import main as indexMain,getCommentList
from ciPingTotal import main as ciPingTotalMain
import os


def targetFile():
    targetFile = 'target.csv'
    commentList = getCommentList()

    rateData = []
    good = 0
    bad = 0
    midlle = 0
    for index, i in enumerate(commentList):
        try:
            value = SnowNLP(i[4]).sentiments
            if value > 0.5:
                good += 1
                rateData.append([i[4], '正面'])
            elif value == 0.5:
                midlle += 1
                rateData.append([i[4], '中性'])
            elif value < 0.5:
                bad += 1
                rateData.append([i[4], '负面'])
        except:
            continue

    for i in rateData:
        with open(targetFile, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(i)


def main():
    try:
        os.remove('./target.csv')
        os.remove("./comment_1_fenci.txt")
        os.remove("./comment_1_fenci_qutingyongci_cipin.csv")
    except:
        pass
    indexMain()
    ciPingTotalMain()
    targetFile()


if __name__ == '__main__':
    main()