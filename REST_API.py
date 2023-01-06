from fastapi import FastAPI, UploadFile, File, HTTPException
from recommend import CaseRecommend
import numpy as np
from typing import List
from pydantic import BaseModel
import pandas as pd
import uvicorn


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


FILE_PATH = r'Dresses dataset/Attribute DataSet.xlsx'

L = [2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

cRecommend = CaseRecommend(FILE_PATH, L)

# df = cRecommend.getdf()
# df = df.fillna('')

df = None

app = FastAPI()

@app.get("/")
def home():
    return "Hello, this is an API for a Case based recommender system made by: Ivor Leon Matijašić"


@app.post("/file")
def filepath(file: UploadFile = File(...)):
    # print(file)
    global df
    df = CaseRecommend(file.file.read(), L)
    # print(df.cols)
    file.file.close()
    return {"File name": file.filename}

@app.get("/columns")
def columns():
    if df is not None:
        return {"Column names": list(df.cols)}
    raise HTTPException(status_code=404, detail="File has not been uploaded!")



@app.get("/recommend/")
def get_recommend(item: Item):
    if df is not None:
        return df.recommend(list(item.dict().values()))
    raise HTTPException(status_code=404, detail="File has not been uploaded!")


if __name__ == "__main__":
    uvicorn.run("REST_API:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)


