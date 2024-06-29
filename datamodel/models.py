from pydantic import BaseModel, EmailStr
from typing import List, Optional, Literal
from datetime import date


class NextSteps(BaseModel):
    next_visit: Optional[str] = None
    prescribed_meds: Optional[List[str]] = None
    prescribed_tests: Optional[List[str]] = None
    prescribed_specialist: Optional[str] = None


class Interaction(BaseModel):
    id: int
    insurance_no: int
    ailment: Optional[str] = None
    symptoms: Optional[str] = None
    metrics: Optional[dict] = None  # recording such as BP, ECP
    remarks: Optional[str] = None
    health_status: Optional[int] = None
    qa: Optional[str] = None
    next_steps: Optional[
        NextSteps
    ] = None  # (next_visit, prescribed_meds, prescribed_tests, prescribed_specialist}
    label: Optional[str] = None


class Patient(BaseModel):
    insurance_no: int
    fname: str
    lname: str
    addr: Optional[str] = None
    age: Optional[int] = None
    sex: str
    ph_no: Optional[str] = None
    email: Optional[EmailStr] = None
    related_docs: Optional[List[str]] = None
    habits: Optional[str] = None
    pre_existing_conditions: Optional[str] = None
    pre_existing_medications: Optional[str] = None
    blood_type: Optional[str] = None
    insurance_provider: str
