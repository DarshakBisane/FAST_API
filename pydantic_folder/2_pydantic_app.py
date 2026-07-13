from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

# This example shows how Pydantic validates and parses input automatically.
class Patient(BaseModel):
    # Name must be a string and should not exceed 100 characters.
    name: str = Field(max_length=100)
    # EmailStr automatically validates that the email format is correct.
    email: EmailStr
    # AnyUrl ensures the value is a valid URL.
    linkdin_url: AnyUrl
    # strict=True prevents unwanted automatic conversion of age values.
    age: int = Field(ge=0, le=100, strict=True)
    # Optional list of illnesses; None is allowed if the field is not provided.
    bimari: Optional[List[str]] = Field(default=None, max_length=3)
    # Dictionary with string keys and string values.
    details: Dict[str, str]


def insert_patient(patient1: Patient):
    # This function prints the stored patient details for demonstration.
    print(patient1.details['ajya'])
    print(patient1.bimari)


# Sample data that will be validated by the Patient model.
patients = {
    'name': 'Ajay',
    'age': 13,
    'linkdin_url': 'https://yo.be/lRArylZCeOs?si=0rsLcSwAaA9',
    'email': 'Ahaysf@gmail.com',
    'details': {'ajya': 'qwerty', 'age': '12'}
}
patient1 = Patient(**patients)

insert_patient(patient1)
