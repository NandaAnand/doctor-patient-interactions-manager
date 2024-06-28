from sql_query_builder import SQLTypes


PATIENT_TABLE = "PATIENT"
patients_columns = [
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
    ("pre_existing_meds", SQLTypes.TEXT),
    ("blood_type", SQLTypes.VARCHAR),
    ("insurance_provider", SQLTypes.VARCHAR),
    "PRIMARY KEY (insurance_no) ",
]
INTERACTION_TABLE = "INTERACTION"

interaction_columns = [
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
    "FOREIGN KEY (insurance_no) REFERENCES patient(insurance_no) ",
]
