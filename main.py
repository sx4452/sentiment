__author__ = 'ben'

import jieba
import codecs
import os
import jieba.analyse
import time
import sys
from TFIDF import TFIDF

reload(sys)                                                                          #Set the coding as 'utf-8' or you will get chaos
sys.setdefaultencoding('gb2312')

'''
def train(trainfile, tfidf, groundtruth, stopWords):
    stopWordsline = stopWords.readlines()
    WordPro = {}
    for i in trainfile:
        trainread = trainfile[i].read()
        seg_list = jieba.cut(trainread)
        for seg in seg_list :
            for j in range(0, len(stopWordsline)):                                                                 #delete stopwords for each line
                if(WordPro.has_key(stopWordsline[j][:-2]) == True):
                    del WordPro[stopWordsline[j][:-2]]
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                if(WordPro.has_key(seg) == True):
                    WordPro[seg] = WordPro[seg] + float(tfidf[i][seg])*float(groundtruth[i])
                else:
                    WordPro[seg] = float(tfidf[i][seg])*float(groundtruth[i])

def test(testfile, tfidf, WordPro, stopWords, groundtruth):
    stopWordsline = stopWords.readlines()
    wordresult = {}
    mytruth = {}
    fileCnt = 0;
    Mapped = 0;
    for i in testfile:
        testread = testfile[i].read()
        seg_list = jieba.cut(testread)
        curresultval = 0
        for seg in seg_list :
            for j in range(0, len(stopWordsline)):                                                                 #delete stopwords for each line
                if(wordresult.has_key(stopWordsline[j][:-2]) == True):
                    del wordresult[stopWordsline[j][:-2]]
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                if(wordresult.has_key(seg) == True):
                    wordresult[seg] = wordresult[seg] + float(WordPro[seg])*float(tfidf[i][seg])
                else:
                    wordresult[seg] = float(WordPro[seg])*float(tfidf[i][seg])
            curresultval = curresultval + wordresult[seg]
        if(curresultval > 0):
            mytruth[i] = 1;
        else:
            mytruth = -1;
        fileCnt += 1

    for i in mytruth:
        if(mytruth[i] == groundtruth[i]):
            Mapped += 1

    print 'the mapped value is '
    print float(Mapped)/float(fileCnt)
'''

def main():
    trainlabelpath = 'train2.rlabelclass'
    trainpath = 'train2'
    testlabelpath = 'test2.rlabelclass'
    testpath = 'test2'
    stopWordspath = 'Chinese-stop-words.txt'
    stopWords = codecs.open(stopWordspath, 'r', 'gbk')
    stopWordsline = stopWords.readlines()
    trainlabelfile = open(trainlabelpath, 'r')
    trainlabelreadline = trainlabelfile.readlines()
    testlabelfile = open(testlabelpath, 'r')
    testlabelreadline = testlabelfile.readlines()

    groundtruth = {}
    for trainlabel in trainlabelreadline:
        if(cmp(trainlabel[-2:], '+1') == 0):
            groundtruth[trainlabel[:-4]] = 1
        else:
            groundtruth[trainlabel[:-4]] = -1

    for testlabel in testlabelreadline:
        if(cmp(testlabel[-2:], '+1') == 0):
            groundtruth[testlabel[:-4]] = 1
        else:
            groundtruth[testlabel[:-4]] = -1

    filenames = os.listdir(trainpath)
    trainfileCnt = 0
    for filename in filenames:
        trainfileCnt += 1
    traincnt = 0
    tfidftrain = {}
    WordPro = {}
    filenames = os.listdir(trainpath)
    for filename in filenames:
        trainfile = open(trainpath + '/' + filename, 'r')
        tfidftrain[filename] = TFIDF(trainfile, stopWordsline, trainfileCnt)
        trainread = trainfile.read()
        seg_list = jieba.cut(trainread)
        for seg in seg_list :
            for j in range(0, len(stopWordsline)):                                                                 #delete stopwords for each line
                if(WordPro.has_key(stopWordsline[j][:-2]) == True):
                    del WordPro[stopWordsline[j][:-2]]
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                if(WordPro.has_key(seg) == True):
                    WordPro[seg] = WordPro[seg] + float(tfidftrain[filename][seg])*float(groundtruth[filename])
                else:
                    WordPro[seg] = float(tfidftrain[filename][seg])*float(groundtruth[filename])
        traincnt += 1
        trainfile.close()

    filenames = os.listdir(testpath)
    testfileCnt = 0
    for filename in filenames:
        testfileCnt += 1
    Mapped = 0;
    tfidftest = {}
    mytruth = {}
    filenames = os.listdir(testpath)
    for filename in filenames:
        testfile = open(testpath + '/' + filename, 'r')
        tfidftest[filename] = TFIDF(testfile, stopWordsline, testfileCnt)
        wordresult = {}
        testread = testfile.read()
        seg_list = jieba.cut(testread)
        curresultval = 0
        for seg in seg_list :
            for j in range(0, len(stopWordsline)):                                                                 #delete stopwords for each line
                if(wordresult.has_key(stopWordsline[j][:-2]) == True):
                    del wordresult[stopWordsline[j][:-2]]
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                if(wordresult.has_key(seg) == True):
                    wordresult[seg] = wordresult[seg] + float(WordPro[seg])*float(tfidftest[filename][seg])
                else:
                    wordresult[seg] = float(WordPro[seg])*float(tfidftest[filename][seg])
            curresultval = curresultval + wordresult[seg]
        if(curresultval > 0):
            mytruth[filename] = 1;
        else:
            mytruth[filename] = -1;
        testfile.close()

    for i in mytruth:
        if(groundtruth.has_key(i) == True):
            if(mytruth[i] == groundtruth[i]):
                Mapped += 1
        else:
            testfileCnt -= 1

    print 'the mapped value is '
    print float(Mapped)/float(testfileCnt)

    stopWords.close()

if __name__ == "__main__":
    start = time.clock()
    main()
    end = time.clock()
    print 'runtime is '
    print end
