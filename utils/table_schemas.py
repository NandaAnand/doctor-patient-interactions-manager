from typing import List, Tuple, Any
from pydantic import BaseModel

from sql_query_builder import SQLTypes


class TableSchema(BaseModel):
    name: str
    col_vs_dtypes: List[Tuple[str, Any]]


PatientSchema = TableSchema(
    name="PATIENT",
    col_vs_dtypes=[
        ("insurance_no", SQLTypes.VARCHAR),
        ("fname", SQLTypes.VARCHAR),
        ("lname", SQLTypes.VARCHAR),
        ("addr", SQLTypes.VARCHAR),
        ("age", SQLTypes.INT),
        ("sex", SQLTypes.VARCHAR),
        ("ph_no", SQLTypes.VARCHAR),
        ("email", SQLTypes.VARCHAR),
        ("related_docs", SQLTypes.TEXT),
        ("habits", SQLTypes.TEXT),
        ("pre_existing_conditions", SQLTypes.TEXT),
        ("pre_existing_medications", SQLTypes.TEXT),
        ("blood_type", SQLTypes.VARCHAR),
        ("insurance_provider", SQLTypes.VARCHAR),
        ("PRIMARY KEY (insurance_no) ", None),
    ],
)

InteractionSchema = TableSchema(
    name="INTERACTION",
    col_vs_dtypes=[
        ("id", SQLTypes.AUTO_INCREMENT),
        ("insurance_no", SQLTypes.VARCHAR),
        ("ailment", SQLTypes.VARCHAR),
        ("symptoms", SQLTypes.VARCHAR),
        ("interaction_date", SQLTypes.DATE),
        ("metrics", SQLTypes.VARCHAR),
        ("remarks", SQLTypes.VARCHAR),
        ("health_status", SQLTypes.INT),
        ("qa", SQLTypes.TEXT),
        ("next_steps", SQLTypes.VARCHAR),
        ("label", SQLTypes.VARCHAR),
        ("FOREIGN KEY (insurance_no) REFERENCES patient(insurance_no) ", None),
    ],
)
