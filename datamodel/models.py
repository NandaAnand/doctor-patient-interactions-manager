from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import json


class NextSteps(BaseModel):
    next_visit: Optional[str] = None
    prescribed_meds: Optional[List[str]] = None
    prescribed_tests: Optional[List[str]] = None
    prescribed_specialist: Optional[str] = None


class Interaction(BaseModel):
    @classmethod
    def from_list(cls, vals):
        fields = {}
        for k, v in zip(cls.model_fields.keys(), vals):
            if isinstance(v, str):
                try:
                    v = json.loads(v)
                except:
                    v = v
            fields[k] = v
        return cls(**fields)

    id: int
    insurance_no: int
    ailment: Optional[str] = None
    symptoms: Optional[str] = None
    interaction_date: Optional[date] = None
    metrics: Optional[dict] = None  # recording such as BP, ECP
    remarks: Optional[str] = None
    health_status: Optional[int] = None
    qa: Optional[str] = None
    next_steps: Optional[
        NextSteps
    ] = None  # (next_visit, prescribed_meds, prescribed_tests, prescribed_specialist}
    label: Optional[str] = None


class Patient(BaseModel):
    @classmethod
    def from_list(cls, vals):
        return cls(**{k: v for k, v in zip(cls.model_fields.keys(), vals)})

    insurance_no: int
    fname: str
    lname: str
    addr: Optional[str] = None
    age: Optional[int] = None
    sex: str
    ph_no: Optional[str] = None
    email: Optional[str] = None
    related_docs: Optional[List[str]] = None
    habits: Optional[str] = None
    pre_existing_conditions: Optional[str] = None
    pre_existing_medications: Optional[str] = None
    blood_type: Optional[str] = None
    insurance_provider: str
