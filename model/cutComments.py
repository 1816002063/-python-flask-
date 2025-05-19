from utils.getPublicData import getAllCommentsData
import jieba
import jieba.analyse as analyse
targetTxt = 'cutComments.txt'


def stopwordslist():
    stopwords = [line.strip() for line in open('./stopWords.txt',encoding='UTF-8').readlines()]
    return stopwords

def getCommentList():
    return getAllCommentsData()

def seg_depart(sentence):
    sentence_depart = jieba.cut(" ".join([x[4] for x in sentence]).strip())
    stopwords = stopwordslist()
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
    return outstr

def writer_comment_fenci():
    with open(targetTxt, 'a+', encoding='utf-8') as targetFile:
        seg = jieba.cut(seg_depart(getCommentList()), cut_all=False)
        # 分好词之后之间用空格隔断
        output = ' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('写入成功！')

# 提取关键词
def main():
    writer_comment_fenci()


if __name__ == '__main__':
    main()

