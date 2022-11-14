import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

# FILE_NAME = r'C:\Users\ilmat\OneDrive\Desktop\Seminar 2\Dresses dataset\Attribute DataSet.xlsx'

class CaseRecommend:
    def __init__(self, file, L, n_nearest = 4):
        self.file = file
        self.L = L
        self.max = []
        self.min = []
        self.labelEncoders = []
        self.X = None
        self.original = None
        self.n = n_nearest
        self.first = 0
        self.nbrs = None
        self.cols = []
        self.load_df(self.file, self.L)

    # map function for price
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

    @staticmethod
    def stringMap(s):
        if s == str:
            return np.Nan
        return s


    def getdf(self):
        return self.df


    def getX(self):
        return self.X


    def load_df(self,file, L):

        self.df = pd.read_excel(file, sheet_name='Sheet1')
        self.original = pd.read_excel(file, sheet_name='Sheet1')

        self.df['Price'] = self.df['Price'].map(self.priceMap)
        self.df['Size'] = self.df['Size'].map(self.sizeMap)


        br = 0

        for col in self.df:
            self.cols.append(col)
            if L[br] == 0:
                self.df[col] = self.df[col].str.lower()
            br += 1
        # print(self.cols)



        self.X = self.df.values
        X_T = self.X.T


        br = 0

        le = LabelEncoder()
        for i in L:
            self.labelEncoders.append(0)

        for col in self.df:

            # getting the max and min vales in the int classes
            if L[br] == 1:
                self.max.append(np.nanmax(X_T[br]))
                self.min.append(np.nanmin(X_T[br]))

            # encoding strings into integers
            elif L[br] == 0:
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


    # manipulacija predmeta koji vraća GUI
    def inputMap(self, example, L):
        '''
        Transforming an example into the right type for knn
        '''
        if len(example) == 13:
            example.append(1)
        elif len(example) == 12:
            example = [111] + example + [1]
        example[2] = self.priceMap(example[2])
        example[4] = self.sizeMap(example[4])


        for i in range(len(L)):
            if L[i] == 0:
                example[i] = int(self.labelEncoders[i][example[i].lower()])
            if L[i] == 1 and type(example[i]) == str:
                example[i] = int(example[i])
        # print(example)

        return example


    def similarity(self,T,X):
        '''
        Similiarity function
        '''
        Igt = lambda t,x: int(t>x)
        Ilt = lambda t,x: int(t<x)

        # Zato što knn koristi udaljenost trebamo oduzeti sličnost od 1 (1 - similiarity)

        def sim(ti, xi, i):
            if self.max[i] == 'string':
                return 1 - int(abs(ti - xi )< 10**-3)
            # asymmetry
            elif self.cols[1:-1][i] == 'Price':
                return abs(ti-xi)/(self.max[i]-self.min[i]) - 1.2*Ilt(ti,xi)*abs(ti-xi)/(self.max[i]-self.min[i])
            elif self.cols[1:-1][i] == 'Rating':
                return abs(ti-xi)/(self.max[i]-self.min[i]) - 1.2*Igt(ti,xi)*abs(ti-xi)/(self.max[i]-self.min[i])
            return abs(ti-xi)/(self.max[i]-self.min[i])

        # equal weights
        w = 1/(len(T)-1)
        sum = 0
        for i in range(1,len(T)-1):
            sum += w*sim(T[i], X[i], i)
        if sum == 0:
            return sum

        return np.max([sum - (w*0.75)*X[-1], 0])

    # funkcija vraća self.n najsličnijih predmeta
    def recommend(self, input):
        # return input
        input = self.inputMap(input, self.L)

        # Koristimo isti model za sve iteracije
        if self.first == 0:
            self.nbrs = NearestNeighbors(n_neighbors = 1, metric=self.similarity)
            self.nbrs.fit(self.X)
            self.first = 1

        A = self.nbrs.kneighbors(np.array([input]), n_neighbors=self.n)

        values = self.original.values

        n_neighbors = []

        for j in range(self.n):
            temp = []
            for i in values[A[1][0][j]]:
                if type(i) == str:
                    i.replace('\n','')
                    temp.append(i)
                elif np.isnan(i):
                    temp.append("NaN")
                else:
                    temp.append(i)
            n_neighbors.append([temp, 1 - A[0][0][j]])
        # print(n_neighbors[0][0])
        return n_neighbors

