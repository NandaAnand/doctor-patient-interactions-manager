import pandas as pd
import numpy as np
import json
import sys

from injectors import sql_instance
from table_schemas import PatientSchema, InteractionSchema
from datamodel.models import Interaction, Patient
from data_utils import DataUtils


def read_data():
    # Interaction
    print("Parsing Interaction data..")
    interaction_df = pd.read_csv("../data/Interaction.csv")
    interaction_df = interaction_df.replace(np.nan, None)
    interaction_df["next_steps"] = interaction_df["next_steps"].apply(
        lambda a: json.loads(a) if a else None
    )
    interaction_df["metrics"] = interaction_df["metrics"].apply(
        lambda a: json.loads(a) if a else None
    )
    interaction_objs = interaction_df.to_dict(orient="records")
    interaction_objs = [Interaction(**obj) for obj in interaction_objs]
    # Patients
    print("Parsing Patients data..")
    patients_df = pd.read_csv("../data/ Patient.csv")
    patients_df = patients_df.replace(np.nan, None)
    patient_objs = patients_df.to_dict(orient="records")
    patient_objs = [Patient(**obj) for obj in patient_objs]

    return interaction_objs, patient_objs


def main():
    interaction_objs, patient_objs = read_data()
    connection = sql_instance()
    if not connection:
        return
    data_utils = DataUtils(connection)
    data_utils.create_table(schema=PatientSchema)
    data_utils.insert_patients(patients=patient_objs)
    data_utils.create_table(schema=InteractionSchema)
    data_utils.insert_interactions(interactions=interaction_objs)
    patients = data_utils.get_patient_by_insurance_no(111)
    print(patients[0].model_dump())
    interactions = data_utils.get_interaction_info(222)
    print(interactions[0].model_dump())


if __name__ == "__main__":
    main()
