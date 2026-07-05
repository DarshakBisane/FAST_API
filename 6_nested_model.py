from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state : str
    pin : int

class Patient(BaseModel):
    name : str
    age : int
    gender : str
    address : Address

address1 = {'city':'Nagpur', 'state':'Maharashtra','pin':441907}
add = Address(**address1)

patient1 = {'name':'Darshak', 'age':19, 'gender': 'Male', 'address' : add}
patient = Patient(**patient1)

print(patient)
print(patient.name)
print(patient.address.city)
print(patient.address.pin)


