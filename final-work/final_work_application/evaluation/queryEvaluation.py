import io
import pandas as pd
import csv
import os
import xml.etree.ElementTree as et 
from irsystem.preProcessing import PreProcessing
from irsystem.booleanModel import BooleanModel
from irsystem.vectorialModel import VectorialModel
from irsystem.probabilisticModel import ProbabilisticModel

PATH = os.path.abspath(os.getcwd())

def getDocRelevance(judgements, topic_number, cord_uid):

    relevance = -1

    for judgement in judgements:
        if (int(judgement["topic_number"]) == topic_number) and (judgement["cord_uid"] == cord_uid):
            relevance = int(judgement["relevance"])
            break
    
    return relevance


def getTop10Rank(results):
    resultTop10 = {}
    resultTop10['query'] = {}
    resultTop10['question'] = {}
    resultTop10['narrative'] = {}
    
    

    try:

        fr1 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")
        
        qrelsLines = fr1.readlines()
    
        judgements = []

        for qrel in qrelsLines:
            qrelSplitted = qrel.strip().split(" ")
            judgements.append( {"topic_number": qrelSplitted[0], "iteration": qrelSplitted[1], "cord_uid": qrelSplitted[2], "relevance": qrelSplitted[3]}   )
        
        fr1.close()



        for i in range(len(results['query'])):
            topic = i+1
            resultTop10['query'][topic] = []
            resultTop10['question'][topic] = []
            resultTop10['narrative'][topic] = []

            j = 0
            for item in results['query'][topic]:
                relevanceQuery = getDocRelevance(judgements, topic, item[0])
                item.append(relevanceQuery)

                if (relevanceQuery != -1):    
                    resultTop10['query'][topic].append( item )
                    j += 1

                if(j == 10):
                    break


            j = 0
            for item in results['question'][topic]:
                relevanceQuery = getDocRelevance(judgements, topic, item[0])
                item.append(relevanceQuery)

                if (relevanceQuery != -1):
                    resultTop10['question'][topic].append( item )
                    j += 1

                if(j == 10):
                    break
            
            j = 0
            for item in results['narrative'][topic]:
                relevanceQuery = getDocRelevance(judgements, topic, item[0])
                item.append(relevanceQuery)

                if (relevanceQuery != -1):
                    resultTop10['narrative'][topic].append( item )
                    j += 1

                if(j == 10):
                    break
            
            #resultTop10['query'][topic] = results['query'][topic][:len(results['query'][topic])-41]
            #resultTop10['question'][topic] = results['question'][topic][:len(results['question'][topic])-41]
            #resultTop10['narrative'][topic] = results['narrative'][topic][:len(results['narrative'][topic])-41]
    
    except(Exception) as error:
        print("[QUERY EVAL] Error in 'getTop10Rank'{}".format(error))
        
    return resultTop10

#Disabled
""" def getResultsOfTop10Rank(results):
    resultTop10 = getTop10Rank(results)

    fr1 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")
        
    qrelsLines = fr1.readlines()
    
    judgements = []

    for qrel in qrelsLines:
        qrelSplitted = qrel.strip().split(" ")
        judgements.append( {"topic_number": qrelSplitted[0], "iteration": qrelSplitted[1], "cord_uid": qrelSplitted[2], "relevance": qrelSplitted[3]}   )
        
    fr1.close()

    try:

        for i in range(len(resultTop10['query'].keys())):
            topic = i+1
            for j in range(len(resultTop10['query'][topic])):
                relevanceQuery = getDocRelevance(judgements, topic, resultTop10['query'][topic][j][0])
                relevanceQuestion = getDocRelevance(judgements, topic, resultTop10['question'][topic][j][0])
                relevanceNarrative = getDocRelevance(judgements, topic, resultTop10['narrative'][topic][j][0])
                
                resultTop10['query'][topic][j].append(relevanceQuery)
                resultTop10['question'][topic][j].append(relevanceQuestion)
                resultTop10['narrative'][topic][j].append(relevanceNarrative)
    except(Exception) as error:
        print("[QUERY EVAL] Error in 'getResultsOfTop10Rank'{}".format(error))

    return resultTop10 """

#Disabled
""" def writeRun(typeOfQuery, model, results):
    #typeOfQuery = 'query'
    #model = 'Prob'
    try: 

        fw = open(os.path.join(PATH, 'data\\out\\run1' + model + typeOfQuery + '_20200716.txt'),'w',encoding="utf8")

        linesToBeWritten = []

        header = "topic cord_uid position rank_value relevance" + "\n"

        linesToBeWritten.append(header)

        for topic, listRank in results[typeOfQuery].items():

            for i in range(len(listRank)):
                pos = i+1

                line = str(topic) + " " +  str(listRank[i][0]) + " " + str(pos) + " " + str(listRank[i][1]) + " " + str(listRank[i][2]) +"\n"

                linesToBeWritten.append(line)
        
        fw.writelines(linesToBeWritten)

        fw.close()
    except(Exception) as error:
        print("[QUERY EVAL] Error in 'writeRun'{}".format(error)) """

def runEval(results, model):
    try:
        resTop10 = getTop10Rank(results)
    except(Exception) as error:
        print("[QUERY EVAL] Error in 'runEval'{}".format(error))
    return resTop10

