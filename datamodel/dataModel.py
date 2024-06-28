from pydantic import BaseModel, EmailStr
from typing import List, Optional, Literal
from datetime import date


class NextSteps(BaseModel):
    next_visit: Optional[date]
    prescribed_meds: Optional[List[str]]
    prescribed_tests: Optional[List[str]]
    prescribed_specialist: str


p


class Patient(BaseModel):
    insurance_no: str
    fname: str
    lname: str
    addr: str
    age: int
    sex: str
    ph_no: str
    email: EmailStr
    related_docs: Optional[List[str]]
    habits: Optional[str]
    pre_existing_conditions: Optional[str]
    pre_existing_medications: Optional[str]
    blood_type: str
    insurance_provider: str
