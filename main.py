from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Id of the patient", examples=["P001"])]
    name : Annotated[str, Field(..., description="Name of the Patient", examples=["Darshak Bisane"])]
    age: Annotated[int, Field(..., description="Age of the Patient", examples=[19], gt=0, lt=130)]
    gender: Annotated[Literal['Male','Female','Other'] ,Field(..., description="Gender of the Patient", examples=['Male'])]
    city: Annotated[str, Field(..., description="City of the patient", examples=['Kawalewada'])]
    hieght : Annotated[float, Field(...,gt=0, description="Hieght of the Patient in mtrs", examples=[156])]
    wieght : Annotated[float, Field(...,gt=0, description="Wieght of the patient in Kg", examples=[54])]

    @computed_field  # ye dynamically field banane ke liye use hota hai aur field return karta hai jo function ke name se identify/use karte hai 
    @property
    def bmi(self) -> float:
        bmi = round(self.wieght/(self.hieght**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'UnderWieght'
        elif self.bmi < 25 :
            return 'Normal'
        elif self.bmi < 30 :
            return 'Normal'
        else:
            return 'Obese'

#opening the file and loading data into variable 
def load_data():
    with open('patients.json','r') as s:
        data = json.load(s) # t read a data from json file
    return data

#saving the data into json file
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data,f,indent=4) #to write a data into json file

@app.get("/")
def abc():
    return {'Patient Information API'} 

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/view_student/{s_id}")
def view_student(s_id:str = Path(...,description="Id of student from json file", example="student1")):
    #load data from json
    data = load_data()

    if s_id in data:
        return data[s_id]
    raise HTTPException(status_code=404, detail=" Student not found")

@app.get("/sort")
def sort_data(sorted_by: str, order: str = Query('asc')):
    
    valid_fields = ['id','age','name']

    if sorted_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'cant sort students using this column. Use: {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid Order Use: asc/desc")

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x : x.get(sorted_by,0) , reverse=sort_order)

    return sorted_data

@app.post('/create')
def createData(patient : Patient): # patient sidha pydantic model ko call kar rha hai.

    #loading existing data
    data = load_data()

    #checking if Patient already Exists
    if patient.id in data:
        raise HTTPException(detail='The given Patient is already exist in DataBase.', status_code=400)

    #inserting patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    #Save data to the Json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})