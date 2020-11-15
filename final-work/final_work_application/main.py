from irsystem.preProcessing import PreProcessing
from irsystem.booleanModel import BooleanModel
from irsystem.vectorialModel import VectorialModel
from irsystem.probabilisticModel import ProbabilisticModel
from irsystem.application import run
from data_processing.slicingMetadataFile import runDataProcessing
from rank_bm25 import BM25Okapi, BM25Plus
from collections import Counter


BOOLEAN = 0
VECTORIAL = 1
PROBABILISTIC = 2


run(PROBABILISTIC)


