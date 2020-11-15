import io
import pandas as pd
import csv
import os
import xml.etree.ElementTree as et 
from collections import Counter

PATH = os.path.abspath(os.getcwd())


def findIntersectionBetween(consulta, documento):
    return list(set(consulta) & set(documento))

def revocacao(Rcurr, R, A):
  intersec = findIntersectionBetween(Rcurr,A)
  return len(intersec)/len(R)

def precisao(R, A):
  intersec = findIntersectionBetween(R, A)
  return len(intersec)/len(A)

def getPrecisaoRanking2(A, R):
  precisions = []
  acc = []
  for doc in A:
    if(doc in R):
      acc = A[:A.index(doc)+1]
      precisions.append([doc, precisao(R, acc)])

  return precisions

def getRankValue(doc, rank):
  for element in rank:
    if (element[0] == doc):
      return element[1]

def MAPi (rank, Ri):
  sum = 0
  precisions = getPrecisaoRanking2([element[0] for element in rank],Ri)

  sum = 0 
  for element in precisions:
    if(getRankValue(element[0], rank) > 0):
      sum += element[1]
  
  return (1/len(Ri)) * sum

def MAP(results, relevanceSet):
    sumQueries = 0
    mapQueries = 0

    sumQuestions = 0
    mapQuestions = 0

    sumNarrative = 0 
    mapNarrative = 0

    try:

        for topic, listRank in results['query'].items():
            sumQueries += MAPi(listRank, relevanceSet[topic])
        
        for topic, listRank in results['question'].items():
            sumQuestions += MAPi(listRank, relevanceSet[topic])

        for topic, listRank in results['narrative'].items():
            sumNarrative += MAPi(listRank, relevanceSet[topic])

        mapQueries = sumQueries/len(results['query'])
        mapQuestions = sumQuestions/len(results['question'])
        mapNarrative = sumNarrative/len(results['narrative'])
    
    except(Exception) as error:
        print("[METRICS] Error in 'MAP' {}".format(error))

    return {'mapQueries': mapQueries, 'mapQuestions': mapQuestions, 'mapNarrative': mapNarrative}

def precisionAt10(results):

    precision10 = {}
    precision10['query'] = {}
    precision10['question'] = {}
    precision10['narrative'] = {}

    try:
        for topic, listRank in results['query'].items():
            listRankTop10 = listRank[:10]
            c = Counter(elem[2] for elem in listRankTop10)

            precision10['query'][topic] = float((c[2] + c[1])/10)

        for topic, listRank in results['question'].items():
            listRankTop10 = listRank[:10]
            c = Counter(elem[2] for elem in listRankTop10)

            precision10['question'][topic] = float((c[2] + c[1])/10)

        for topic, listRank in results['narrative'].items():
            listRankTop10 = listRank[:10]
            c = Counter(elem[2] for elem in listRankTop10)

            precision10['narrative'][topic] = float((c[2] + c[1])/10)
    except(Exception) as error:
        print("[METRICS] Error in 'precisionAt10' {}".format(error))


    return precision10
 
def getRevevantDocsSet():
    relevantDocs = {}
    try:

        fr1 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")
        
        qrelsLines = fr1.readlines()

        for qrel in qrelsLines:
            qrelSplitted = qrel.strip().split(" ")

            if( int(qrelSplitted[0]) not in relevantDocs.keys() ):
                relevantDocs[ int(qrelSplitted[0]) ] = []
            else:
                if (qrelSplitted[3] == "2") or  (qrelSplitted[3] == "1"):
                    relevantDocs[ int(qrelSplitted[0]) ].append(qrelSplitted[2])
            
        
        fr1.close()
    
    except(Exception) as error:
        print("[METRICS] Error in 'getRevevantDocsSet' {}".format(error))

    return relevantDocs

def runMetrics(results, resultsTop10):
    precision10 = {}
    try:
        relevantDocsSet = getRevevantDocsSet() 

        precision10 = precisionAt10(results)

        mapResults = MAP(results, relevantDocsSet)
    
    except(Exception) as error:
        print("[METRICS] Error in 'runMetrics' {}".format(error))

    return precision10, mapResults



