import pandas as pd
import numpy as np
import json
import sys

sys.path.append("..")
from utils.injectors import sql_instance
from utils.table_schemas import PatientSchema, InteractionSchema
from datamodel.models import Interaction, Patient
from utils.data_utils import DataUtils


def read_data():
    """
    Reads and processes the Interaction and Patient data from CSV files.

    The function performs the following steps:
    1. Reads the Interaction data from 'Interaction.csv' and processes it:
       - Replaces NaN values with None.
       - Parses JSON fields 'next_steps' and 'metrics'.
       - Converts the data into a list of Interaction objects.
    2. Reads the Patient data from 'Patient.csv' and processes it:
       - Replaces NaN values with None.
       - Converts the data into a list of Patient objects.

    Returns:
        tuple: A tuple containing two lists:
            - interaction_objs (list of Interaction): List of Interaction objects.
            - patient_objs (list of Patient): List of Patient objects.
    """
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
    interaction_df["qa"] = interaction_df["qa"].apply(
        lambda a: json.loads(a) if a else None
    )
    interaction_objs = interaction_df.to_dict(orient="records")
    interaction_objs = [Interaction(**obj) for obj in interaction_objs]
    # Patients
    print("Parsing Patients data..")
    patients_df = pd.read_csv("../data/Patient.csv")
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


if __name__ == "__main__":
    main()
