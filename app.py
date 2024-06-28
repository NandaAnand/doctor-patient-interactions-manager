from typing import Union

from fastapi import FastAPI
from utils.data_utils import DataUtils

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
