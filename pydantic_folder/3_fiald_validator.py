from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Dict

# This example shows how to create custom validation rules for specific fields.
class Patient(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        # Convert the name to uppercase before storing it.
        return value.upper()

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        # Only allow emails from approved company domains.
        valid_domain = ["hdfc.com", "icici.com", "sbi.com"]
        domain_value = value.split('@')[-1]

        if domain_value not in valid_domain:
            raise ValueError('Domain is not valid: cannot use the offer')
        return value


def insert_patient(patient1: Patient):
    # Print the validated values after model creation.
    print(patient1.name)
    print(patient1.email)


patients = {'name': 'Ajay', 'email': 'Ahaysf@hdfc.com'}
patient1 = Patient(**patients)

insert_patient(patient1)
