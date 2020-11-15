import io
import pandas as pd
import csv
import os


class BooleanModel:
    def __init__(self, docsColl, query, operation):
        self.docsColl = docsColl
        self.query = query
        self.operation = operation
    
    
    
    # matriz --> matriz de tokens Nx1 (cada linha representa um documento e a coluna apresenta a lista de tokens extraídos do documento).
    # Essa função cria a matriz de incidências. Essa matriz indica se um determinado token existe em um documento (valor > 0 caso exista. Do contrário, valor = 0), assim como
    # a frequência neste documento.
    def criarMatrizIncidenciasV2(self,matriz):
        # A chave do diconário é o token. O valor associado à chave é uma matriz 1x1, em que o elemento dicionarioTokens[token][0][0] representa uma matriz 1xN, sendo que cada coluna está 
        # associada a um respectivo documento e os possíveis valores que podem assumir são maiores ou iguais a 0 (o valor 0 significada que o token não se encontra no documento e o valores
        # maiores do que 0 significam a frequência com aparecem no documento.

        try:

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
        except(Exception) as error:
            print("[BOOLEAN] Error in 'criaMatrizIncidenciaV2'{}".format(error))
            return {}

    # Recupera-se os documentos associados aos tokens extraídos da consulta. Caso um token não exista na nossa coleção, o retiramos da consulta.
    def recuperaDocumento(self, consultaTratada, operacao, matrizIncidencia, colecao):
        documentosResultado = []
        try:
            termosAusentes = ""
            for termo in consultaTratada:
                if (termo in consultaTratada) and (termo not in matrizIncidencia.keys()):
                    consultaTratada.remove(termo)
                    termosAusentes += termo + ", "
            
            if (len(termosAusentes) > 0):
                termosAusentes = termosAusentes[:(len(termosAusentes)-2)] 
                print("Os termos: " + termosAusentes + " não estão mapeados em nossa coleção, contudo iremos retornar os documentos cujos os outros termos estão presentes.")

            resultado = []
            if (len(consultaTratada) > 0) and (consultaTratada[0] in matrizIncidencia.keys()):
                resultado = matrizIncidencia[consultaTratada[0]][0]
                
                if (len(consultaTratada) > 1):
                    for i in range(1,len(consultaTratada)):
                        if (i <= len(consultaTratada)-1):
                            if (consultaTratada[i] in matrizIncidencia.keys()):
                                listaDeIncidencias = matrizIncidencia[consultaTratada[i]][0]
                                if (operacao == 1):
                                    resultado =  [ resultado[i] & (1 if listaDeIncidencias[i] !=0 else 0) for i in range(len(listaDeIncidencias)) ] 
                                elif (operacao == 2):
                                    resultado =  [ resultado[i] | (1 if listaDeIncidencias[i] !=0 else 0) for i in range(len(listaDeIncidencias)) ]  
                    
            else:
                print("[BOOLEAN] A consulta possui somente um termo e este não está mapeado em nossa coleção.")

            
            for j in range(len(resultado)):
                if (resultado[j] != 0):
                    documentosResultado.append(colecao[j])
        
            return documentosResultado
        except(Exception) as error:
            print("[BOOLEAN] Error in 'recuperaDocumentos'{}".format(error))
            return []
 
    def run(self):
        #print("vai criar matriz")
        matrizIncidencia = self.criarMatrizIncidenciasV2(self.docsColl)

        #print("vai recuperar")
        docsRecuperados = self.recuperaDocumento(self.query, self.operation, matrizIncidencia, self.docsColl)

        #print("recuperou")
        return docsRecuperados