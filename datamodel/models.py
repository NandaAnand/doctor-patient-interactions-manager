from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date
import json


class NextSteps(BaseModel):
    """
    A class to represent the next steps in a patient's treatment plan.

    Attributes:
        next_visit (Optional[str]): The date for the next visit.
        prescribed_meds (Optional[List[str]]): List of prescribed medications.
        prescribed_tests (Optional[List[str]]): List of prescribed tests.
        prescribed_specialist (Optional[str]): The specialist prescribed.
    """

    next_visit: Optional[str] = None
    prescribed_meds: Optional[List[str]] = None
    prescribed_tests: Optional[List[str]] = None
    prescribed_specialist: Optional[str] = None


class Interaction(BaseModel):
    """
    A class to represent an interaction with a patient.

    Attributes:
        id (int): The interaction ID.
        insurance_no (int): The patient's insurance number.
        ailment (Optional[str]): The patient's ailment.
        symptoms (Optional[str]): The patient's symptoms.
        interaction_date (Optional[date]): The date of interaction.
        metrics (Optional[dict]): Health metrics recorded during interaction.
        remarks (Optional[str]): Additional remarks.
        health_status (Optional[int]): Health status rating.
        qa (Optional[Dict[str, str]]): Q&A related to the interaction.
        next_steps (Optional[NextSteps]): Next steps in the treatment plan.
        label (Optional[str]): Label for the interaction.
    """

    @classmethod
    def from_list(cls, vals):
        res = None
        fields = {}
        for k, v in zip(cls.model_fields.keys(), vals):

            if isinstance(v, str):
                try:
                    v = json.loads(v)
                except Exception as e:
                    v = v
            if k in ["metrics", "qa", "next_steps"] and v == "":
                v = None
            fields[k] = v
        try:
            res = cls(**fields)
        except Exception as e:
            print(e)
        return res

    id: int
    insurance_no: str
    ailment: Optional[str] = None
    symptoms: Optional[str] = None
    interaction_date: Optional[date] = None
    metrics: Optional[dict] = None  # recording such as BP, ECP
    remarks: Optional[str] = None
    health_status: Optional[int] = None
    qa: Optional[Dict[str, str]] = None
    next_steps: Optional[
        NextSteps
    ] = None  # (next_visit, prescribed_meds, prescribed_tests, prescribed_specialist}
    label: Optional[str] = None


class Patient(BaseModel):
    """
    A class to represent a patient.

    Attributes:
        insurance_no (str): The patient's insurance number.
        fname (str): The patient's first name.
        lname (str): The patient's last name.
        addr (Optional[str]): The patient's address.
        age (Optional[int]): The patient's age.
        sex (str): The patient's sex.
        ph_no (Optional[str]): The patient's phone number.
        email (Optional[str]): The patient's email address.
        related_docs (Optional[List[str]]): List of related documents.
        habits (Optional[str]): The patient's habits.
        pre_existing_conditions (Optional[str]): The patient's pre-existing conditions.
        pre_existing_medications (Optional[str]): The patient's pre-existing medications.
        blood_type (Optional[str]): The patient's blood type.
        insurance_provider (str): The patient's insurance provider.
    """

    @classmethod
    def from_list(cls, vals):
        return cls(**{k: v for k, v in zip(cls.model_fields.keys(), vals)})

    insurance_no: str
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
