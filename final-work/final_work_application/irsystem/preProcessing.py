import string
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
from nltk.stem import PorterStemmer, SnowballStemmer
import re

class PreProcessing:

    def __init__(self, df, column_name):
        self.df = df
        self.column_name = column_name
        self.entry = list(self.df[self.column_name])
        self.delimiters = string.punctuation
        self.stopwordsSet = set(stopwords.words('english'))

    def run(self):
        
        preProcessedEntries = []

        try:

            for element in self.entry: 
                # Normalizing the document and removing white spaces from the both sides
                element = str(element).lower()

                element = re.sub(r'\d+', '', element)

                for deli in self.delimiters:
                    element = element.replace(deli,"")
            
                element = element.strip()

                # Tokenizing the document
                tokens = word_tokenize(element)

                # Removing stopwords
                tokens_without_stopwords = [i for i in tokens if not i in self.stopwordsSet]

                # Stemming each token
                tokens_stemmed = []
                stemmer= PorterStemmer()
                #stemmer = SnowballStemmer("english")
                for word in tokens_without_stopwords:
                    tokens_stemmed.append(stemmer.stem(word))
                
                #print(tokens_stemmed)
                preProcessedEntries.append(tokens_stemmed)

        except(Exception) as error:
            print("[PRE PROCESSING] Error in 'run'{}".format(error))

        return preProcessedEntries