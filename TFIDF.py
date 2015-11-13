__author__ = 'ben'

import jieba
import os
import jieba.analyse
import math
import time

def TFIDF(inputFile, fileCnt):
    TF = {}
    tf = {}
    idf = {}
    inputFile.seek(0)
    inputread = inputFile.read()
    seg_list = jieba.cut(inputread)
    segCnt = 0;
    for seg in seg_list :
        if (seg != '' and seg != "\n" and seg != "\n\n" and seg != "\t") :
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
