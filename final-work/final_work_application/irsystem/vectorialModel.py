import numpy as np
import math

class VectorialModel:

    def __init__(self, docsColl, query,):
        self.docsColl = docsColl
        self.query = query


    # termo     --> String contendo um único elemento.
    # documento --> Vetor de string (matriz 1x1), que representa o texto de um único documento da coleção.
    # Calcula a frequência de um determinado termo em um documento específico.
    def freqDoc(self,termo, documento):
        return documento.count(termo)

    # termo   --> String contendo um único elemento.
    # colecao --> Vetor de string (matriz 1x1), que representa o texto de um único documento da coleção.
    # Calcula a frequência de um determinado termo em um documento específico.
    def freqCol(self,termo, colecao):
        contaTermo = 0
        for documento in colecao:
            if(termo in documento):
                contaTermo+= 1
        return contaTermo

    # colecao --> Vetor coluna onde cada linha representa o texto de um documento que foi pré-processado, ou seja, foi aplicado normalização e tokenização.
    # Esta função realiza a ponderação TF-IDF nos termos dos documentos e retorna um dicionário de dicionário em que a chave do dicionário mais externo se 
    # refere ao documento e o valor associado à chave é um outro dicionário em que a chave é o termo e o valor associado é o seu peso.
    def ponderacaoTF_IDF(self,colecao):

        termoLista      = []
        dicionarioPeso  = {}

        # Insere os termos dos documentos na lista "termoLista", mas sem repetição
        for documentos in colecao:
            for termo in documentos:
                if(termo not in termoLista):
                    termoLista.append(termo)

        numeroDocumento = 0

        # Aplicação da fórmula do "Esquema de ponderação 3" do slide da aula
        for documento in colecao:
            dicionarioTemp = {}
            for termo in termoLista:
                peso = 0
                if(termo in documento):
                    peso = (1 + math.log2(self.freqDoc(termo, documento))) * (math.log2(len(colecao)/self.freqCol(termo, colecao)))
                if(termo not in dicionarioTemp.keys()):
                    dicionarioTemp[termo] = peso

            dicionarioPeso[numeroDocumento] = dicionarioTemp
            numeroDocumento+= 1

        return dicionarioPeso

    # colecao         --> Vetor coluna onde cada linha representa o texto de um documento que foi pré-processado, ou seja, foi aplicado normalização e tokenização.
    # consultaTratada --> Lista com os termos da consulta pré-processados
    # Realiza a ponderação TF-IDF nos termos da consulta e retorna um dicionário em que as chaves são os termos e os valores são os respectivos pesos.
    def ponderacaoTF_IDF2(self,colecao, consultaTratada):

        termoLista = []

        # Insere os termos dos documentos na lista "termoLista", mas sem repetição
        for documentos in colecao:
            for termo in documentos:
                if(termo not in termoLista):
                    termoLista.append(termo)

        numeroDocumento = 0

        dicionarioTemp  = {}

        # Aplicação da fórmula do "Esquema de ponderação 3" do slide da aula
        for termo in termoLista:
            peso = 0
            if(termo in consultaTratada):
                peso = (1 + math.log2( self.freqDoc(termo, consultaTratada) ) ) * (math.log2( len(colecao) / self.freqCol(termo, colecao) ) )
            if(termo not in dicionarioTemp.keys()):
                dicionarioTemp[termo] = peso

        return dicionarioTemp


    # vetorConsulta --> consulta representada como vetores de termos com pesos associados
    # vetorDoc      --> documento representado como vetores de termos com pesos associados
    # Cálculo do cosseno do ângulo formado com o vetor da consulta e o vetor do documento
    def sim(self, vetorDoc, vetorConsulta):
        somatorio = 0

        for i,j in zip(vetorDoc.keys(),range(len(vetorDoc))):
            somatorio += vetorDoc[i] * vetorConsulta[j]

        moduloVetorDoc      = np.linalg.norm(np.array(list(vetorDoc.values())))
        moduloVetorConsulta = np.linalg.norm(np.array(vetorConsulta))

        return somatorio/(moduloVetorDoc*moduloVetorConsulta)


    # dicPesosDoc      --> dicionário obtido da ponderação TF-IDF aplicada nos documentos
    # dicPesosConsulta --> dicionário obtido da ponderação TF-IDF aplicada na consulta
    # Aplica o ranqueamento dos documentos
    def rank(self, dicPesosDoc, dicPesosConsulta):
    
        dicRank = {}

        for key in dicPesosDoc.keys():
            rankDict = self.sim(dicPesosDoc[key], list(dicPesosConsulta.values()))
            dicRank[key] = rankDict
        
        return dicRank

    def run(self):
        ponderacaoDocumentos = self.ponderacaoTF_IDF(self.docsColl)
        #print("Resultado da ponderação TF-IDF para os termos da coleção:")
        #print(ponderacaoDocumentos)
        #print('\n')

        ponderacaoQueries = self.ponderacaoTF_IDF2(self.docsColl, self.query)
        dicRank                = self.rank(ponderacaoDocumentos, ponderacaoQueries)
        listRank               = sorted(dicRank.items(), key=lambda x: x[1], reverse=True)

        return listRank