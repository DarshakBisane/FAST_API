from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

# This example validates the whole model after all fields are parsed.
class Patient(BaseModel):
    age: int
    details: Dict[str, str]

    @model_validator(mode='after')
    def model_validating(cls, model):
        # If the patient is older than 60, emergency contact is mandatory.
        if model.age > 60 and 'emergency' not in model.details:
            raise ValueError('Patient older than 60 year must have the emergency contact number')
        return model


def insert_patient(patient1: Patient):
    # Show the validated model contents.
    print(patient1.age)
    print(patient1.details)


patients = {'age': 73, 'details': {'ajya': 'qwerty', 'emergency': '9511278525', 'age': '12'}}
patient1 = Patient(**patients)

insert_patient(patient1)
