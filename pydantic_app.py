from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

class Patient(BaseModel):
    name:str = Field(max_length=100)
    email: EmailStr                                                      # Email Validation automatically
    linkdin_url : AnyUrl
    age:int = Field(ge=0,le=100, strict=True)                            # it provide data validation. strict data converstion nhi hone deta. automatically type conversion rokta hai
    bimari : Optional[List[str]] = Field(default=None,max_length=3)      # agar kisi ko Optional data banana hai to. None bhi use kar sakte hai
    details : Dict[str,str]

def insert_patient(patient1:Patient):
    print(patient1.details['ajya'])
    print(patient1.bimari)

patients = {'name':'Ajay', 'age':13,'linkdin_url': 'https://yo.be/lRArylZCeOs?si=0rsLcSwAaA9','email':'Ahaysf@gmail.com', 'details':{'ajya': 'qwerty', 'age':'12'}}
patient1= Patient(**patients)

insert_patient(patient1)
