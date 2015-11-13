__author__ = 'ben'

import jieba
import codecs
import os
import jieba.analyse
import math
import time
import sys

reload(sys)                                                                          #Set the coding as 'utf-8' or you will get chaos
sys.setdefaultencoding('gb2312')

def TFIDF(inputFile, stopWordsline, fileCnt):
    TF = {}
    tf = {}
    idf = {}
    inputread = inputFile.read()
    seg_list = jieba.cut(inputread)
    segCnt = 0;
    for seg in seg_list :
        for j in range(0, len(stopWordsline)):                                                                 #delete stopwords for each line
            if(tf.has_key(stopWordsline[j][:-2]) == True):
                del tf[stopWordsline[j][:-2]]
        if (seg != '' and seg != "\n" and seg != "\n\n") :
            segCnt += 1
            if seg in tf :
                tf[seg] += 1
            else:
                tf[seg] = 1
    for j in tf:
        TF[j] = float(tf[j])/float(segCnt)                                                                    #TF:the number of keyword'i' in lineCnt
        if(idf.has_key(j) == True):
            idf[j] += 1
        else:
            idf[j] = 1
    tf.clear()
    tfidf = {}
    for j in TF:
        tfidf[j] = round(TF[j] * math.log(float(fileCnt)/float(idf[j]), 10), 4)
    return tfidf
