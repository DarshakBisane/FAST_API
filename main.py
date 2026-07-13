from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

# Initialize the FastAPI application instance.
app = FastAPI()


# ======================= Patient Model =======================

class Patient(BaseModel):
    # This model defines the validation rules for a patient record.

    id: Annotated[str, Field(..., description="Id of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the Patient", examples=["Darshak Bisane"])]
    age: Annotated[int, Field(..., description="Age of the Patient", examples=[19], gt=0, lt=130)]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender", examples=["Male"])]
    city: Annotated[str, Field(..., description="City", examples=["Kawalewada"])]
    height: Annotated[float, Field(..., gt=0, description="Height in meters", examples=[1.56])]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg", examples=[54])]

    @computed_field
    @property
    def bmi(self) -> float:
        # BMI is calculated from weight and height.
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        # This converts BMI into a simple health category.
        if self.bmi < 18.5:
            return "UnderWeight"

        elif self.bmi < 25:
            return "Normal"

        elif self.bmi < 30:
            return "OverWeight"

        else:
            return "Obese"


# ======================= Update Model =======================

class UpdatePatient(BaseModel):
    # This model supports partial updates by allowing optional fields.

    name: Annotated[Optional[str], Field(default=None, description="Name", examples=["Darshak"])]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=130)]
    gender: Annotated[
        Optional[Literal["Male", "Female", "Other"]],
        Field(default=None)
    ]
    city: Annotated[Optional[str], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# ======================= Utility Functions =======================

def load_data():
    # Read all saved patient records from the JSON file.
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    # Save the updated data back to the JSON file.
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


# ======================= Routes =======================

@app.get("/")
def home():
    # Simple health check route for the API.
    return {"message": "Patient Information API"}


@app.get("/view")
def view():
    # Return the complete list of patients.
    return load_data()


@app.get("/view_patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="Patient ID", examples=["P001"])
):
    # Fetch one patient by their unique ID.
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")

    return data[patient_id]


@app.get("/sort")
def sort_data(
    sorted_by: str = Query(...),
    order: str = Query("asc")
):
    # Sort the records by name or age in ascending or descending order.
    valid_fields = ["name", "age"]

    if sorted_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Use one of {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Order should be asc or desc"
        )

    data = load_data()

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sorted_by),
        reverse=(order == "desc")
    )

    return sorted_data


@app.post("/create")
def create_data(patient: Patient):
    # Create a new patient after validating the request body.
    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient already exists."
        )

    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully"}
    )


@app.put("/edit/{patient_id}")
def update_patient(
    patient_id: str,
    patient_info: UpdatePatient
):
    # Update an existing patient using the supplied fields.
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Patient Not Found"
        )

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_info.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id

    updated_patient = Patient(**existing_patient_info)

    data[patient_id] = updated_patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient Updated Successfully"}
    )