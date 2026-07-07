from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict

class Patient(BaseModel):
    name:str 
    email:EmailStr

    @field_validator('name')
    @classmethod
    def name_validator(cls,value):
        return value.upper()

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domain = ["hdfc.com","icici.com","sbi.com"]

        domain_value = value.split('@')[-1]
        if domain_value not in valid_domain:
            raise ValueError('Domain is not valid: cannot use the offer')
        return value

def insert_patient(patient1:Patient):
    print(patient1.name)
    print(patient1.email)

patients = {'name':'Ajay','email':'Ahaysf@hdfc.com'}
patient1= Patient(**patients)

insert_patient(patient1)
