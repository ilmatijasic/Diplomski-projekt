import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder
from functools import partial


class CaseRecommend:
    def __init__(self, file, categories = {}, n_nearest = 4):
        self.file = file
        self.categories = categories  # Work in progress, should be [ "Irrelevant", "Nominal", "Ordinal" ], might add "Interval" and "Ratio"
        self.mapping = {}
        self.max = []
        self.min = []
        self.labelEncoders = []
        self.X = None
        self.original = None
        self.n = n_nearest
        self.first = 0
        self.nbrs = None
        self.cols = []
        self.load_df()

    # map function for price
    @staticmethod
    def dictMap(s, dictionary: dict, default = -1):
        '''Mapping of original values into usable values'''
        if type(s) == str:
            s = str.lower(s)
            return dictionary.get(s, default)
        else:
            return s

    # Will be deleted after the function mapDict is implemented correctly
    @staticmethod
    def priceMap(s):
        if type(s) == str:
            s = str.lower(s)
            if s == 'low':
                return 1
            elif s == 'average':
                return 2
            elif s == 'very-high':
                return 3
            return 4
        else:
            return s


    # Will be deleted after the function mapDict is implemented correctly
    @staticmethod
    def sizeMap(s):
        if type(s) == str:
            s = str.lower(s)
            if s == 'small' or s == 's':
                return 's'
            elif s == 'm':
                return 'm'
            elif s == 'free':
                return 'free'
            elif s == 'l':
                return 'l'
            return 'xl'
        else:
            return 'none'

    # Will be deleted after the function mapDict is implemented correctly
    @staticmethod
    def stringMap(s):
        if s == str:
            return np.Nan
        return s

    # Work in progress
    def load_df_in_progress(self):
        ''' Loading file and turning it into a pandas dataframe'''

        self.df = pd.read_excel(self.file)
        self.original = pd.read_excel(self.file)

        for col in self.df:
            self.cols.append(col)
            if col not in self.categories:
                self.categories[col] = None
                self.mapping[col] = None

    # Work in progress
    def map_values(self):

        for col in self.mapping:
            if self.mapping[col] is not None:
                self.df[col] = self.df[col].map(partial(self.dictMap, dictionary=self.mapping[col]))


        # print(self.cols)

        self.X = self.df.values
        X_T = self.X.T


        br = 0

        le = LabelEncoder()
        for i in L:
            self.labelEncoders.append(0)

        for col in self.df:

            # getting the max and min vales in the int classes
            if self.categories[col] == "Ordinal":
                self.max.append(np.nanmax(X_T[br]))
                self.min.append(np.nanmin(X_T[br]))

            # encoding strings into integers
            elif self.categories[col] == "Nominal":
                self.X[:, br] = le.fit_transform(self.X[:, br])
                keys = le.classes_
                values = le.transform(le.classes_)
                dictionary = dict(zip(keys, values))
                self.labelEncoders[br]=dictionary

                self.max.append('string')
                self.min.append('string')
            else:
                self.max.append('irrelevant')
                self.min.append('irrelevant')
            br += 1

    # Will be deleted after the function load_df_in_progress is implemented correctly
    def load_df(self):
        ''' Loading file and turning it into a pandas dataframe'''

        self.df = pd.read_excel(self.file)
        self.original = pd.read_excel(self.file)

        self.df['Price'] = self.df['Price'].map(self.priceMap)
        self.df['Size'] = self.df['Size'].map(self.sizeMap)


        br = 0

        for col in self.df:
            self.cols.append(col)
            if self.categories[br] == 0:
                self.df[col] = self.df[col].str.lower()
            br += 1
        # print(self.cols)

        self.X = self.df.values
        X_T = self.X.T


        br = 0

        le = LabelEncoder()
        for i in self.categories:
            self.labelEncoders.append(0)

        for col in self.df:

            # getting the max and min vales in the int classes
            if self.categories[br] == 1:
                self.max.append(np.nanmax(X_T[br]))
                self.min.append(np.nanmin(X_T[br]))

            # encoding strings into integers
            elif self.categories[br] == 0:
                self.X[:, br] = le.fit_transform(self.X[:, br])
                keys = le.classes_
                values = le.transform(le.classes_)
                dictionary = dict(zip(keys, values))
                self.labelEncoders[br]=dictionary

                self.max.append('string')
                self.min.append('string')
            else:
                self.max.append('irrelevant')
                self.min.append('irrelevant')
            br += 1


    # Mapping of values for gui
    def inputMap(self, example):
        '''
        Transforming an example into the right type for knn
        '''
        if len(example) == 13:
            example.append(1)
        elif len(example) == 12:
            example = [111] + example + [1]
        example[2] = self.priceMap(example[2])
        example[4] = self.sizeMap(example[4])


        for i in range(len(self.categories)):
            if self.categories[i] == 0:
                example[i] = int(self.labelEncoders[i][example[i].lower()])
            if self.categories[i] == 1 and type(example[i]) == str:
                example[i] = int(example[i])
        # print(example)

        return example


    def similarity(self,T,X):
        '''
        Similiarity function
        '''
        Igt = lambda t,x: int(t>x)
        Ilt = lambda t,x: int(t<x)

        def sim(ti, xi, i):
            if self.max[i] == 'string':
                return int(abs(ti - xi )< 10**-3)
            # asymmetry
            elif self.cols[1:-1][i] == 'Price':
                temp = abs(ti-xi)/(self.max[i]-self.min[i])
                return 1 - temp + 1.2*Ilt(ti,xi)*temp
            elif self.cols[1:-1][i] == 'Rating':
                temp = abs(ti-xi)/(self.max[i]-self.min[i])
                return 1 - temp + 1.2*Igt(ti,xi)*temp
            return 1 - abs(ti-xi)/(self.max[i]-self.min[i])

        # equal weights
        w = 1/(len(T)-1)
        sum = 0
        for i in range(1,len(T)-1):
            sum += w*sim(T[i], X[i], i)
        if sum == 0:
            return sum

        return sum + (w)*X[-1]

    # Function returns self.n most similiar items
    def recommend(self, input):
        '''Takes input, returns recommendation'''
        # return input
        input = self.inputMap(input)


        partial_similarity = partial(self.similarity, T=input)
        output = np.array([partial_similarity(X=i) for i in self.X])
        sorted_output = output.argsort()[::-1][:self.n]


        values = self.original.values

        recommendations = []

        for j in range(self.n):
            temp = []
            for i in values[sorted_output[j]]:
                if type(i) == str:
                    i.replace('\n','')
                    temp.append(i)
                elif np.isnan(i):
                    temp.append("NaN")
                else:
                    temp.append(i)
            recommendations.append([temp, output[sorted_output[j]]])

        return recommendations

if __name__ == '__main__':
    input = ['sexy', 'low', '0', 'S', 'summer', 'o-neck', 'sleevless', 'empire', 'microfiber', 'chiffon', 'ruffles', 'animal']
    # output = [[1006032852, 'Sexy', 'Low', 4.6, 'M', 'Summer', 'o-neck', 'sleevless', 'empire', 'NaN', 'chiffon', 'ruffles', 'animal', 1], 0.833076923076923]
    FILE_NAME = r'Dresses dataset/Attribute DataSet.xlsx'


    L = [2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

    cRecommend = CaseRecommend(FILE_NAME, L)

    out = cRecommend.recommend(input)

    print(out)
