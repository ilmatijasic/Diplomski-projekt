import pandas as pd
import json


class Config():
    def __init__(self, file):
        self.file = file
        self.df = pd.read_excel(self.file)
        self.config={}
        for col in self.df:
            self.config[col] = 'Irrelevant'
        self.config['Ordinal order'] = {}

    def getConfig(self, indent = 2):
        return json.dumps(self.config, indent = indent)

    def writeConfigToFile(self, path, indent = 2):
        with open(path, 'w') as f:
            f.write(json.dumps(self.config, indent = indent))



if __name__ == '__main__':
    FILE_NAME = r'Dresses dataset/Attribute DataSet.xlsx'

    conf = Config(FILE_NAME)
    print(json.loads(conf.getConfig()))

    conf.writeConfigToFile('conf.json')