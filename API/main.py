from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import consultes
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Alumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    DescAula: str

@app.get("/alumne/listAll", response_model=List[Alumne])
def list_all_alumnes():
    return consultes.list_all_alumnes()

@app.get("/alumne/list", response_model=List[Alumne])
def read_alumnes(orderby: str = None, contain: str = None, skip: int = 0, limit: int = None):
    return consultes.query_alumnes(orderby, contain, skip, limit)

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    contents = await file.read()
    lines = contents.decode("utf-8").splitlines()
    reader = csv.reader(lines)
    next(reader)
    for row in reader:
        descAula, edifici, pis, nomAlumne, cicle, curs, grup = row
        consultes.insert_alumne_from_csv(nomAlumne, cicle, curs, grup, descAula, edifici, pis)
    return {"status": "Alumnes carregats correctament"}
