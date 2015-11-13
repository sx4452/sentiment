__author__ = 'ben'

import jieba
import os
import jieba.analyse
import time
from TFIDF import TFIDF

def main():
    ############################inputFile#################################
    trainlabelpath = 'train2.rlabelclass'
    trainpath = 'train2'
    testlabelpath = 'test2.rlabelclass'
    testpath = 'test2'
    trainlabelfile = open(trainlabelpath, 'r')
    trainlabelreadline = trainlabelfile.readlines()
    testlabelfile = open(testlabelpath, 'r')
    testlabelreadline = testlabelfile.readlines()

    ############################groundtruth###############################
    groundtruth = {}
    for trainlabel in trainlabelreadline:
        if(cmp(trainlabel[-3:-1], '+1') == 0):
            groundtruth[trainlabel[:-4]] = 1
        else:
            groundtruth[trainlabel[:-4]] = -1

    for testlabel in testlabelreadline:
        if(cmp(testlabel[-3:-1], '+1') == 0):
            groundtruth[testlabel[:-4]] = 1
        else:
            groundtruth[testlabel[:-4]] = -1

    ########################train####################################
    filenames = os.listdir(trainpath)
    trainfileCnt = 0
    for filename in filenames:
        trainfileCnt += 1
    traincnt = 0
    tfidftrain = {}
    WordPro = {}
    filenames = os.listdir(trainpath)
    for filename in filenames:
        trainfile = open(trainpath + '\\' + filename, 'r')
        tfidftrain[filename] = TFIDF(trainfile, trainfileCnt)
        trainfile.seek(0)
        trainread = trainfile.read()
        seg_list = jieba.cut(trainread)
        for seg in seg_list :
            if (seg != '' and seg != "\n" and seg != "\n\n" and seg != "\t" and tfidftrain[filename].has_key(seg) == True):
                if(WordPro.has_key(seg) == True):
                    WordPro[seg] = WordPro[seg] + float(tfidftrain[filename][seg])*float(groundtruth[filename])
                else:
                    WordPro[seg] = float(tfidftrain[filename][seg])*float(groundtruth[filename])
        traincnt += 1
        trainfile.close()

    #######################test###########################################
    filenames = os.listdir(testpath)
    testfileCnt = 0
    for filename in filenames:
        testfileCnt += 1
    Mapped = 0;
    Balanced = 50.0
    tfidftest = {}
    mytruth = {}
    filenames = os.listdir(testpath)
    for filename in filenames:
        testfile = open(testpath + '\\' + filename, 'r')
        tfidftest[filename] = TFIDF(testfile, testfileCnt)
        wordresult = {}
        testfile.seek(0)
        testread = testfile.read()
        seg_list = jieba.cut(testread)
        curresultval = 0.0
        for seg in seg_list :
            if (seg != '' and seg != "\n" and seg != "\n\n" and seg != "\t" and tfidftest[filename].has_key(seg) == True and WordPro.has_key(seg) == True):
                if(wordresult.has_key(seg) == True):
                    wordresult[seg] = wordresult[seg] + float(WordPro[seg])*float(tfidftest[filename][seg])
                else:
                    wordresult[seg] = float(WordPro[seg])*float(tfidftest[filename][seg])
                if(wordresult[seg] > 0 and groundtruth[filename] == -1):wordresult[seg] = float(wordresult[seg])/float(Balanced)
                curresultval = float(curresultval) + float(wordresult[seg])
        if(curresultval < 0):
            mytruth[filename] = -1;
        else:
            mytruth[filename] = 1;
        testfile.close()

    for i in mytruth:
        if(groundtruth.has_key(i) == True):
            if(mytruth[i] == groundtruth[i]):
                Mapped += 1
        else:
            testfileCnt -= 1

    print 'the mapped value is '
    print float(Mapped)/float(testfileCnt)

if __name__ == "__main__":
    start = time.clock()
    main()
    end = time.clock()
    print 'runtime is '
    print end
