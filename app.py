from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open('student.json','r') as s:
        data = json.load(s)
    return data

@app.get("/")
def abc():
    return {'Student Information API'}

@app.get("/home")
def xy():
    return {"Darshak": "Bisane"}

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

