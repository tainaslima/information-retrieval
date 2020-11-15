import os


PATH = os.path.abspath(os.getcwd())

def runDataProcessing():
    f = open(os.path.join(PATH, 'data\\in\\metadata_20200716.csv'), 'r',encoding="utf8")

    f2 = open(os.path.join(PATH, 'data\\in\\metadataSliced_20200716.csv'),'w',encoding="utf8")

    f3 = open(os.path.join(PATH, 'data\\in\\qrels-covid_d5_j0.5-5.txt'),'r',encoding="utf8")

    metadataLines = f.readlines()

    qrelsLines = f3.readlines()

    linesToBeWritten = []

    numberOfTopics = [1,2,3,4,5,6,7,8,9,10]

    linesToBeWritten.append(metadataLines[0])

    maxNOfLines = 50
    i = 0
    for line in metadataLines:
        #print(line.find("coronavirus"))
        splitedLine = line.split(",")

        cord_id = splitedLine[0]
        #print(cord_id)
        abstract = splitedLine[8]
        if (abstract.find("coronavirus") > 0) or (abstract.find("COVID-19") > 0):
            for qrels in qrelsLines:
                splitedQrels = qrels.split(" ")
                if (qrels.find(cord_id) > 0) and (linesToBeWritten[-1].find(cord_id) < 0) and (int(splitedQrels[0]) in numberOfTopics):
                    #print(cord_id)
                    linesToBeWritten.append(line)
                    i += 1
        if(i > maxNOfLines):
            break
            


    f2.writelines(linesToBeWritten)

    f.close()
    f2.close()
    f3.close()

runDataProcessing()