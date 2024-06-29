from typing import List, Optional
from pydantic import BaseModel

from sql_query_builder import SQLTypes


class TableSchema(BaseModel):
    class Column(BaseModel):
        name: str
        dtype: Optional[SQLTypes] = None

    name: str
    columns: List[Column]
    constraints: Optional[List[str]] = None


PatientSchema = TableSchema(
    name="PATIENT",
    columns=[
        TableSchema.Column(name="insurance_no", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="fname", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="lname", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="addr", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="age", dtype=SQLTypes.INT),
        TableSchema.Column(name="sex", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="ph_no", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="email", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="related_docs", dtype=SQLTypes.TEXT),
        TableSchema.Column(name="habits", dtype=SQLTypes.TEXT),
        TableSchema.Column(name="pre_existing_conditions", dtype=SQLTypes.TEXT),
        TableSchema.Column(name="pre_existing_medications", dtype=SQLTypes.TEXT),
        TableSchema.Column(name="blood_type", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="insurance_provider", dtype=SQLTypes.VARCHAR),
    ],
    constraints=["PRIMARY KEY (insurance_no) "],
)

InteractionSchema = TableSchema(
    name="INTERACTION",
    columns=[
        TableSchema.Column(name="id", dtype=SQLTypes.INT),
        TableSchema.Column(name="insurance_no", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="ailment", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="symptoms", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="interaction_date", dtype=SQLTypes.DATE),
        TableSchema.Column(name="metrics", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="remarks", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="health_status", dtype=SQLTypes.INT),
        TableSchema.Column(name="qa", dtype=SQLTypes.TEXT),
        TableSchema.Column(name="next_steps", dtype=SQLTypes.VARCHAR),
        TableSchema.Column(name="label", dtype=SQLTypes.VARCHAR),
    ],
    constraints=[
        "PRIMARY KEY (id)",
        "FOREIGN KEY (insurance_no) REFERENCES PATIENT(insurance_no) ",
    ],
)
