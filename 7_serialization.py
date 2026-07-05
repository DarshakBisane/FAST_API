from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state : str
    pin : int

class Patient(BaseModel):
    name : str
    age : int = 12
    gender : str
    address : Address

address1 = {'city':'Nagpur', 'state':'Maharashtra','pin':441907}
add = Address(**address1)

patient1 = {'name':'Darshak', 'gender': 'Male', 'address' : add}
patient = Patient(**patient1)

temp = patient.model_dump(exclude=['name']) 
print(temp)

temp2 = patient.model_dump(include=['name'])
print(temp2)

temp3 = patient.model_dump(exclude={'address' : 'city'})
print(temp3)

temp4 = patient.model_dump(include={'address' : 'city'})
print(temp4)

temp5 = patient.model_dump(exclude_unset=True)
print(temp5)