import numpy as np
import math

class ProbabilisticModel:

    def __init__(self, docsColl, query, nDocsColl):
        self.docsColl = docsColl
        self.query = query
        self.nDocsColl = nDocsColl

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

    # matriz --> matriz de tokens Nx1 (cada linha representa um documento e a coluna apresenta a lista de tokens extraídos do documento).
# Essa função cria a matriz de incidências. Essa matriz indica se um determinado token existe em um documento (valor > 0 caso exista. Do contrário, valor = 0), assim como
# a frequência neste documento.
    def criarMatrizIncidenciasV2(self, matriz):

        # A chave do diconário é o token. O valor associado à chave é uma matriz 1x1, em que o elemento dicionarioTokens[token][0][0] representa uma matriz 1xN, sendo que cada coluna está 
        # associada a um respectivo documento e os possíveis valores que podem assumir são maiores ou iguais a 0 (o valor 0 significada que o token não se encontra no documento e o valores
        # maiores do que 0 significam a frequência com aparecem no documento.
        dicionarioTokensV2 = {}

        # Itera sobre os documentos
        for index in range(0, len(matriz)):
            
            # Itera em cada elemento da lista de token
            for token in matriz[index]:

            # Adiciona o token ao dicionário, caso ele não exista. Além disso, seta o valor para 1 para o documento ao qual pertence.
                if(token not in dicionarioTokensV2.keys()):
                    x                         = [0]*len(matriz)
                    x[index]                  = 1
                    dicionarioTokensV2[token] = [x]

                # Incrementa-se a frequência com que aparece no respectivo documento
                else:
                    dicionarioTokensV2[token][0][index] += 1
                
        return dicionarioTokensV2

    #Função que calcula o tamanho do documento
    def sizeDocument (self, document):
        return len(document)

    #Função que calcula o tamanho médio dos documentos da coleção
    def averageSizeDocument(self, colecao):
        avg = 0
        for document in colecao:
            avg += self.sizeDocument(document)

        avg = avg / len(colecao)

        return avg

    #Função que calcula o Ni de cada termo
    def Ni(self, frequenciasDoc, termo):
        ni = 0

        for freq in frequenciasDoc[termo][0]:
            if (freq > 0):
                ni+=1

        return ni

    #Função que calcula o B para cada termo i e documento j
    def B(self, termo, documento, colecao, frequenciasDoc, K1 = 1, b = 0.85):
        return ( (K1 + 1)*frequenciasDoc[termo][0][documento] ) / ( K1 * ( (1-b) + b*( self.sizeDocument(colecao[documento])/self.averageSizeDocument(colecao) ) )  +  frequenciasDoc[termo][0][documento]) 

    #Função que calcula a parte do log na conta de similaridade
    def logsPart(self, N, ni):
        return math.log2( (N-ni + 0.5) / (ni + 0.5)  )

    #Função que encontra os termos em comum entre a consulta e o documento em questão
    def findIntersectionBetween(self, consulta, documento):
        return list(set(consulta) & set(documento))

    #Função que calcula os valores da fórmula de similaridade (valores para o ranking)
    def similaridadeBM25(self, consulta, colecao, N):

        simConsultaDoc = {}

        frequenciasDoc = self.criarMatrizIncidenciasV2(colecao)

        for i in range(len(colecao)):
            termosEmComum = self.findIntersectionBetween(consulta, colecao[i])

            sum = 0

            for termo in termosEmComum:
                sum += self.B(termo, i, colecao, frequenciasDoc) * self.logsPart(N, self.Ni(frequenciasDoc, termo))
            
            if i not in simConsultaDoc.keys():
                simConsultaDoc[i] = sum

        return simConsultaDoc
    
    def run(self):
        dicRank = self.similaridadeBM25(self.query, self.docsColl, self.nDocsColl)

        listRank = sorted(dicRank.items(), key=lambda x: x[1], reverse=True)

        return listRank