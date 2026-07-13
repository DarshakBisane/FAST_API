from pydantic import BaseModel

# This example demonstrates how to control what data is exported from a model.
class Address(BaseModel):
    city: str
    state: str
    pin: int


class Patient(BaseModel):
    name: str
    age: int = 12
    gender: str
    address: Address


# Create the nested address and patient models.
address1 = {'city': 'Nagpur', 'state': 'Maharashtra', 'pin': 441907}
add = Address(**address1)

patient1 = {'name': 'Darshak', 'gender': 'Male', 'address': add}
patient = Patient(**patient1)

# Exclude name from the output dictionary.
temp = patient.model_dump(exclude=['name'])
print(temp)

# Include only the name in the output dictionary.
temp2 = patient.model_dump(include=['name'])
print(temp2)

# Exclude only the city field inside the nested address object.
temp3 = patient.model_dump(exclude={'address': 'city'})
print(temp3)

# Include only the city field from the nested address object.
temp4 = patient.model_dump(include={'address': 'city'})
print(temp4)

# Show only the fields explicitly set by the user during creation.
temp5 = patient.model_dump(exclude_unset=True)
print(temp5)