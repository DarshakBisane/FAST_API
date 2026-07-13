from pydantic import BaseModel

# This example shows how to use nested models inside another model.
class Address(BaseModel):
    city: str
    state: str
    pin: int


class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address


# Create the nested address object first.
address1 = {'city': 'Nagpur', 'state': 'Maharashtra', 'pin': 441907}
add = Address(**address1)

# Then create a patient using that nested address model.
patient1 = {'name': 'Darshak', 'age': 19, 'gender': 'Male', 'address': add}
patient = Patient(**patient1)

# Print the nested values to understand the model structure.
print(patient)
print(patient.name)
print(patient.address.city)
print(patient.address.pin)

