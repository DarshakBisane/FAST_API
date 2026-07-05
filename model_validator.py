from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):
    name:str 
    email:EmailStr
    age:int
    bimari : List[str]
    details : Dict[str,str]

    @model_validator(mode='after')
    def model_validating(cls,model):
        if model.age>60 and 'emergency' not in model.details:
            raise ValueError('Patient older than 60 year must have the emergency contact number')
        return model

def insert_patient(patient1:Patient):
    print(patient1.name)
    print(patient1.email)

patients = {'name':'Ajay', 'age':73,'email':'Ahaysf@hdfc.com', 'details':{'ajya': 'qwerty','emergency':'9511278525', 'age':'12'}, 'bimari':['ajay','sumit','akshay','atul']}
patient1= Patient(**patients)

insert_patient(patient1)
