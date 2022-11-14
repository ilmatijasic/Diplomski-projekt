import numpy as np
from sklearn.neighbors import NearestNeighbors

from recommend import CaseRecommend
from gui import GUI


FILE_NAME = r'Dresses dataset\Attribute DataSet.xlsx'

if __name__ == '__main__':

    # tipovi vrijednosti za značajke
    # strings: 0, int: 1, irrelevant: 2
    L = [2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

    cRecommend = CaseRecommend(FILE_NAME, L)

    df = cRecommend.getdf()
    # df = df.fillna('')

    # print(list(df.columns))
    # opcije za GUI dropdown menu
    df_dict={}
    br = 0

    for col in df.columns:

        if L[br] == 0:
            uniques = list(df[col].unique())
            if np.nan in uniques:
                uniques.remove(np.nan)
            df_dict[col] = uniques
        if col == 'Price':
            df_dict[col] = ['low', 'average', 'high', 'very high']
        if col == 'Rating':
            df_dict[col] = [i for i in range(6)]
        if col == 'Size':
            df_dict[col] = ['S', 'M', 'L', 'XL', 'Free']
        # print(col)
        br+=1


    GUI(df_dict, cRecommend.recommend)




