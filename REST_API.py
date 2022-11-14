from fastapi import FastAPI, Query
from recommend import CaseRecommend
import numpy as np
from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    style: str
    price: str
    rating: float
    size: str
    season: str
    neckLine: str
    sleeveLength: str
    waistline: str
    material: str
    fabricType: str
    decoration: str
    patternType: str


FILE_NAME = r'Dresses dataset/Attribute DataSet.xlsx'

L = [2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

cRecommend = CaseRecommend(FILE_NAME, L)

df = cRecommend.getdf()
df = df.fillna('')


app = FastAPI()

@app.get("/")
def home():
    return "Hello, this is an API for a Case based recommender system made by: Ivor Leon Matijašić"

@app.get("/columns")
def columns():
    return {"Column names": list(df.columns)}


@app.get("/recommend/")
async def get_recommend(item: Item):
    return cRecommend.recommend(list(item.dict().values()))


