import io
import pandas as pd
import csv
import os
import xml.etree.ElementTree as et 
import datetime as dt
from rank_bm25 import BM25Okapi, BM25Plus
from prettytable import PrettyTable
from .preProcessing import PreProcessing
from .booleanModel import BooleanModel
from .vectorialModel import VectorialModel
from .probabilisticModel import ProbabilisticModel
from evaluation.queryEvaluation import runEval
from evaluation.metrics import runMetrics

PATH = os.path.abspath(os.getcwd())
BOOLEAN = 0
VECTORIAL = 1
PROBABILISTIC = 2

def readTrecCovidFiles():
    # Lendo o arquivo com os documentos (.csv) para um DataFrame
    dfMetadata = pd.read_csv(os.path.join(PATH, 'data\\in\\metadataSliced_20200716.csv'))

    dfDocs = dfMetadata[['cord_uid', 'title', 'abstract']]

    
    # Lendo o arquivo de test collection (.xml) para um DataFrame
    dfTestCollNameCols = ["topic_number", "query", "question", "narrative"]
    dfTestCollRows = []

    xtree = et.parse(PATH + "\\data\\in\\topics-rnd5.xml")

    xroot = xtree.getroot()

    for node in xroot: 
        s_number = int(node.get("number"))
        s_query = node.find("query").text.strip()
        s_question = node.find("question").text.strip()
        s_narrative = node.find("narrative").text.strip()
        dfTestCollRows.append(  {'topic_number': s_number, 'query': s_query, 'question': s_question, 'narrative': s_narrative}   )

    dfTestColl = pd.DataFrame(dfTestCollRows, columns = dfTestCollNameCols)

    return dfDocs, dfTestColl

def runSearchBoolean(dfDocs, dfTestColl):

    result = {}
    result['query'] = {}
    result['question'] = {}
    result['narrative'] = {}

    try:
        #print("foi")
        for i in range(len(dfTestColl['queryProc'])):
            bm = BooleanModel(list(dfDocs['abstractProc']), list(dfTestColl['queryProc'][i]), 1).run()
            bm2 = BooleanModel(list(dfDocs['abstractProc']), list(dfTestColl['questionProc'][i]), 1).run()
            bm3 = BooleanModel(list(dfDocs['abstractProc']), list(dfTestColl['narrativeProc'][i]), 1).run()
            
        
            result['query'][dfTestColl['topic_number'][i]] = []
            result['question'][dfTestColl['topic_number'][i]] = []
            result['narrative'][dfTestColl['topic_number'][i]] = []

            if(len(bm) > 0):
                k = 0
                for j in range(len(dfDocs)):
                    if(set(dfDocs['abstractProc'][j]) == set(bm[k])):
                        result['query'][dfTestColl['topic_number'][i]].append([dfDocs['cord_uid'][j]])
                        k += 1
                    if(k>= len(bm)):
                        break

            if(len(bm2) > 0):
                l = 0
                for j in range(len(dfDocs)):
                    if(set(dfDocs['abstractProc'][j]) == set(bm2[l])):
                        result['question'][dfTestColl['topic_number'][i]].append([dfDocs['cord_uid'][j]])
                        l += 1
                    if(l>= len(bm2)):
                        break
            
            if(len(bm3) > 0):
                p = 0
                for j in range(len(dfDocs)):
                    if(set(dfDocs['abstractProc'][j]) == set(bm3[p])):
                        result['narrative'][dfTestColl['topic_number'][i]].append([dfDocs['cord_uid'][j]])
                        p += 1
                    if(p>= len(bm3)):
                        break

        #print("fo2i")
            #print(retrievedDocs)

    except(Exception) as error:
        print("[RUN BOOLEAN] Error in 'runSearchBoolean'{}".format(error))
    
    return result

def runSearchVectorial(dfDocs, dfTestColl):
    result = {}
    result['query'] = {}
    result['question'] = {}
    result['narrative'] = {}

    try: 
        fr1 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")
            
        qrelsLines = fr1.readlines()
        
        judgements = []

        for qrel in qrelsLines:
            qrelSplitted = qrel.split(" ")
            judgements.append( {"topic_number": qrelSplitted[0], "iteration": qrelSplitted[1], "cord_uid": qrelSplitted[2], "relevance": qrelSplitted[3]}   )
            
        fr1.close()


        for i in range(len(dfTestColl['queryProc'])-40):
            vec = VectorialModel(list(dfDocs['abstractProc']), list(dfTestColl['queryProc'][i])).run()
            vec2 = VectorialModel(list(dfDocs['abstractProc']), list(dfTestColl['questionProc'][i])).run()
            vec3 = VectorialModel(list(dfDocs['abstractProc']), list(dfTestColl['narrativeProc'][i])).run()
            

        
            result['query'][dfTestColl['topic_number'][i]] = []
            result['question'][dfTestColl['topic_number'][i]] = []
            result['narrative'][dfTestColl['topic_number'][i]] = []


            if(len(vec) > 0):
            
                for item in vec:
                    pos = item[0]
                    rank = item[1]

                    result['query'][dfTestColl['topic_number'][i]].append(   [  dfDocs['cord_uid'][pos],rank  ]  )

            if(len(vec2) > 0):
            
                for item2 in vec2:
                    pos2 = item2[0]
                    rank2 = item2[1]

                    result['question'][dfTestColl['topic_number'][i]].append(   [  dfDocs['cord_uid'][pos2],rank2 ]  )


            if(len(vec3) > 0):
            
                for item3 in vec3:
                    pos3 = item3[0]
                    rank3 = item3[1]

                    result['narrative'][dfTestColl['topic_number'][i]].append(   [  dfDocs['cord_uid'][pos3],rank3 ]  )
    except(Exception) as error:
        print("[RUN VECTORIAL] Error in 'runSearchVectorial'{}".format(error))
    return result

#Disabled 
""" def runSearchProbabilistic(dfDocs, dfTestColl):
    result = {}
    result['query'] = {}
    result['question'] = {}
    result['narrative'] = {}

    for i in range(len(dfTestColl['queryProc'])-40):
        prob = ProbabilisticModel(list(dfDocs['abstractProc']), list(dfTestColl['queryProc'][i]), len(dfDocs['abstractProc'])).run()
        prob2 = ProbabilisticModel(list(dfDocs['abstractProc']), list(dfTestColl['questionProc'][i]), len(dfDocs['abstractProc'])).run()
        prob3 = ProbabilisticModel(list(dfDocs['abstractProc']), list(dfTestColl['narrativeProc'][i]), len(dfDocs['abstractProc'])).run()
        

    
        result['query'][dfTestColl['topic_number'][i]] = []
        result['question'][dfTestColl['topic_number'][i]] = []
        result['narrative'][dfTestColl['topic_number'][i]] = []


        if(len(prob) > 0):
        
            for item in prob:
                pos = item[0]
                rank = item[1]

                result['query'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][pos],rank]  )

        if(len(prob2) > 0):
        
            for item2 in prob2:
                pos2 = item2[0]
                rank2 = item2[1]

                result['question'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][pos2],rank2]  )


        if(len(prob3) > 0):
        
            for item3 in prob3:
                pos3 = item3[0]
                rank3 = item3[1]

                result['narrative'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][pos3],rank3]  )

    return result """

def runSearchProbabilistic2(dfDocs, dfTestColl):
    bm25 = BM25Plus(list(dfDocs['abstractProc']))

    result = {}
    result['query'] = {}
    result['question'] = {}
    result['narrative'] = {}

    try:
        for i in range(len(dfTestColl['queryProc'])-40):
            result['query'][dfTestColl['topic_number'][i]] = []
            result['question'][dfTestColl['topic_number'][i]] = []
            result['narrative'][dfTestColl['topic_number'][i]] = []

        
            docScoresQuery = bm25.get_scores(list(dfTestColl['queryProc'][i]))
            docScoresQuestion = bm25.get_scores(list(dfTestColl['questionProc'][i]))
            docScoresNarrative = bm25.get_scores(list(dfTestColl['narrativeProc'][i]))


            if(len(docScoresQuery) > 0):
            
                for j in range(len(docScoresQuery)):
                    result['query'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][j],docScoresQuery[j]]  )

                result['query'][dfTestColl['topic_number'][i]].sort(key=lambda tup: tup[1], reverse=True)

            if(len(docScoresQuestion) > 0):
            
                for k in range(len(docScoresQuestion)):
                    result['question'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][k],docScoresQuestion[k]]  )

                result['question'][dfTestColl['topic_number'][i]].sort(key=lambda tup: tup[1], reverse=True)

            if(len(docScoresNarrative) > 0):
            
                for l in range(len(docScoresNarrative)):
                    result['narrative'][dfTestColl['topic_number'][i]].append(   [dfDocs['cord_uid'][l],docScoresNarrative[l]]  )
                
                result['narrative'][dfTestColl['topic_number'][i]].sort(key=lambda tup: tup[1], reverse=True)
    except(Exception) as error:
        print("[RUN PROBABILISTIC] Error in 'runSearchProbabilistic'{}".format(error))

    return result

#Disabled
""" def writeResults(model, results):
    try:
        fw = open(os.path.join(PATH, 'data\\out\\result' + model+ '_20200716.csv'),'w',encoding="utf8")

        fr1 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")
        
        qrelsLines = fr1.readlines()
        
        judgements = []

        for qrel in qrelsLines:
            qrelSplitted = qrel.split(" ")
            judgements.append( {"topic_number": qrelSplitted[0], "iteration": qrelSplitted[1], "cord_uid": qrelSplitted[2], "relevance": qrelSplitted[3]}   )


        linesToBeWritten = []

        for topic_number, listRank in results['query'].items():
            
            for item in listRank:
                line = "" + "," + str(topic_number) + "," + "query" + "," + str(item[0]) + "," + str(item[1]) + "," + getDocRelevance(judgements, topic_number, item[0])
                linesToBeWritten.append(line)

        for topic_number2, listRank2 in results['question'].items():
            
            for item2 in listRank2:
                line2 = "" + "," + str(topic_number2) + "," + "question" + "," + str(item2[0]) + "," + str(item2[1]) + "," + getDocRelevance(judgements, topic_number2, item2[0])
                linesToBeWritten.append(line2)

        for topic_number3, listRank3 in results['narrative'].items():
            
            for item3 in listRank3:
                line3 = "" + "," + str(topic_number3) + "," + "narrative" + "," + str(item3[0]) + "," + str(item3[1]) + "," + getDocRelevance(judgements, topic_number3, item3[0])
                linesToBeWritten.append(line3)

        fw.writelines(linesToBeWritten)

        fr1.close()
        fw.close()
    except(Exception) as error:
        print("[WRITE RESULTS] Error in 'writeResults'{}".format(error)) """

def printResults(results):

    x = PrettyTable()

    column_names = list(results.keys())

    for key, value in results.items():

        if(isinstance(value, dict)):
            x.add_column(key, list(value.values()))
        else:
            x.add_column(key, [value])

    print(x)

def run(model):
    
    print("[APP] ({printTime}) Loading test collection and document collection...\n".format(printTime=dt.datetime.now()))

    dfDocs, dfTestColl = readTrecCovidFiles()

    print("[APP] ({printTime}) Test collection and document collection loaded!\n".format(printTime=dt.datetime.now()))

    print("[APP] ({printTime}) Starting information retrieval...\n".format(printTime=dt.datetime.now()))

    try:
        print("[APP] ({printTime}) Starting pre-processing of documents and queries...\n".format(printTime=dt.datetime.now()))

        dfDocs['abstractProc'] = PreProcessing(dfDocs, 'abstract').run()
        dfTestColl['queryProc'] = PreProcessing(dfTestColl, 'query').run()
        dfTestColl['questionProc'] = PreProcessing(dfTestColl, 'question').run()
        dfTestColl['narrativeProc'] = PreProcessing(dfTestColl, 'narrative').run()

        print("[APP] ({printTime}) Pre-processing of documents and queries ended!\n".format(printTime=dt.datetime.now()))

        if(model == BOOLEAN):

            print("[APP] ({printTime}) Starting to search with boolean model...\n".format(printTime=dt.datetime.now()))

            resultBoolean = runSearchBoolean(dfDocs, dfTestColl)

            print("[APP] ({printTime}) Search with boolean model ended!\n".format(printTime=dt.datetime.now()))
        
            print("[APP] ({printTime}) Starting analysis...\n\n".format(printTime=dt.datetime.now()))
            
            evalBol = runEval(resultBoolean,'Boolean')

            print("[APP] ({printTime}) Analysis ended!\n\n".format(printTime=dt.datetime.now()))

            print("[APP] Results \n")

            print(evalBol)
        
        elif(model == VECTORIAL):
            print("[APP] ({printTime}) Starting to search with vectorial model...\n".format(printTime=dt.datetime.now()))

            resultVectorial = runSearchVectorial(dfDocs, dfTestColl)

            print("[APP] ({printTime}) Search with vectorial model ended!\n".format(printTime=dt.datetime.now()))
        
            print("[APP] ({printTime}) Starting analysis...\n\n".format(printTime=dt.datetime.now()))
            
            evalVec = runEval(resultVectorial,'Vectorial')
            precisionAt10, mapResults = runMetrics(resultVectorial, evalVec)

            print("[APP] ({printTime}) Analysis ended!\n\n".format(printTime=dt.datetime.now()))

            print("[APP] Results \n")

            print("     Precision at 10\n")
            printResults(precisionAt10)
            print("     MAP\n")
            printResults(mapResults)

        elif(model == PROBABILISTIC):
            print("[APP] ({printTime}) Starting to search with probabilistic model...\n".format(printTime=dt.datetime.now()))

            resultProbabilistic2 = runSearchProbabilistic2(dfDocs, dfTestColl)

            print("[APP] ({printTime}) Search with probabilistic model ended!\n".format(printTime=dt.datetime.now()))
        
            print("[APP] ({printTime}) Starting analysis...\n\n".format(printTime=dt.datetime.now()))
            
            evalProb2 = runEval(resultProbabilistic2,'ProbabilisticBM25Plus')
            precisionAt10, mapResults = runMetrics(resultProbabilistic2, evalProb2)

            print("[APP] ({printTime}) Analysis ended!\n\n".format(printTime=dt.datetime.now()))

            print("[APP] Results \n")

            print("     Precision at 10\n")
            printResults(precisionAt10)
            print("     MAP\n")
            printResults(mapResults)
        
        else:
            print("[APP] Type of model not recognized. Use just boolean, vectorial or probabilistic.")

        print("[APP] ({printTime}) Information retrieval ended!\n".format(printTime=dt.datetime.now()))
    except(Exception) as  error:
        print("[APP] Error in 'init'{}".format(error))

