from typing import List, Union, Any, Tuple

from pydantic import BaseModel

import json

from utils.sql_query_builder import SQLQueryBuilder, SQLOperators
from datamodel.models import Interaction, Patient
from utils.table_schemas import TableSchema, InteractionSchema, PatientSchema


def convert_obj_to_lists(objs: List[BaseModel]) -> Union[List, List[List]]:
    cols = list(objs[0].model_dump().keys())
    rows = []
    # @TODO make it more clean and readable
    for obj in objs:
        row = []
        for col in cols:
            value = obj.model_dump()[col]
            if isinstance(value, (dict, BaseModel)):
                value = json.dumps(value)
            row.append(value)
        rows.append(row)
    return cols, rows


class DataUtils:
    """
    A utility class for database operations related to patients and interactions.
    """

    def __init__(self, connection_obj: Any):
        self.sql_builder = SQLQueryBuilder()
        self.conn = connection_obj

    def get_patient_by_insurance_no(self, insurance_no: str) -> List[Patient]:
        """
        Retrieve patient details by insurance number.

        Args:
            insurance_no (str): The insurance number of the patient.

        Returns:
            List[Patient]: A list of Patient objects.
        """
        colnames_vs_objs = {col.name: col for col in PatientSchema.columns}
        self.cursor = self.conn.cursor()
        query = (
            self.sql_builder.select(columns=["*"], table=PatientSchema.name)
            .conditions(
                intersections=[
                    (colnames_vs_objs["insurance_no"], SQLOperators.EQ, insurance_no)
                ]
            )
            .construct_query()
        )
        print(query)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        patients = [Patient.from_list(row) for row in rows]
        self.cursor.close()
        return patients

    def get_interaction_info(
        self,
        insurance_no: int = None,
        labels: str = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[Interaction]:
        """
        Retrieve interaction information based on insurance number and optional labels.

        Args:
            insurance_no (int, optional): Insurance number of the patient.
            labels (str, optional): Comma-separated string of labels to filter interactions.
            offset (int, optional): Offset for pagination.
            limit (int, optional): Limit for pagination.

        Returns:
            List[Interaction]: A list of Interaction objects.
        """
        colnames_vs_objs = {col.name: col for col in InteractionSchema.columns}
        intersections = [
            (colnames_vs_objs["insurance_no"], SQLOperators.EQ, insurance_no)
        ]
        unions = []
        if labels:
            for label in labels.split(","):
                unions += [(colnames_vs_objs["label"], SQLOperators.LIKE, label)]
        self.cursor = self.conn.cursor()
        query = (
            self.sql_builder.select(columns=["*"], table=InteractionSchema.name)
            .conditions(intersections=intersections, unions=unions)
            .limit(limit)
            .offset(offset)
            .construct_query()
        )
        print(query)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        interactions = [Interaction.from_list(row) for row in rows]
        self.cursor.close()
        return interactions

    def create_table(self, schema: TableSchema):
        """
        Create a database table based on the provided schema.

        Args:
            schema (TableSchema): The schema of the table to create.
        """
        query = self.sql_builder.create(schema).construct_query()
        cursor = self.conn.cursor()
        print(query)
        cursor.execute(query)
        self.conn.commit()
        print("Created Table..")
        cursor.close()

    def _insert_items(
        self, data_objs: List[BaseModel], table_name: str, batch_size: int = 100
    ):
        """
        Insert a batch of items into a specified table.

        Args:
            data_objs (List[BaseModel]): List of Pydantic BaseModel objects to insert.
            table_name (str): The name of the table to insert into.
            batch_size (int, optional): The size of each batch to insert.
        """
        cursor = self.conn.cursor()
        columns, rows = convert_obj_to_lists(objs=data_objs)
        insert_query = self.sql_builder.insert_batch(
            table=table_name, columns=columns
        ).construct_query()
        print(f"Insert query template: {insert_query}")
        for i in range(0, len(rows), batch_size):
            print(f"Inserting for batch {i+batch_size}")
            cursor.executemany(insert_query, rows[i : i + batch_size])
            self.conn.commit()
        print("Done")

    def insert_interactions(
        self, interactions: List[Interaction], batch_size: int = 100
    ):
        """
        Insert a list of interaction records into the database.

        Args:
            interactions (List[Interaction]): List of Interaction objects to insert.
            batch_size (int, optional): The size of each batch to insert.
        """
        self._insert_items(
            data_objs=interactions,
            table_name=InteractionSchema.name,
            batch_size=batch_size,
        )

    def insert_patients(self, patients: List[Patient], batch_size: int = 100):
        """
        Insert a list of patient records into the database.

        Args:
            patients (List[Patient]): List of Patient objects to insert.
            batch_size (int, optional): The size of each batch to insert.
        """
        self._insert_items(
            data_objs=patients, table_name=PatientSchema.name, batch_size=batch_size
        )
