from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):
    hieght : int 
    width:int
   

    @computed_field
    @property
    def area(self) -> int :
        area = self.hieght*self.width
        return area

def insert_patient(patient1:Patient):
    print(patient1.area)


patients = {'hieght':23, 'width':73}
patient1= Patient(**patients)

insert_patient(patient1)
