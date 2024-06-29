from typing import List, Union, Any, Tuple

from pydantic import BaseModel

import json

from sql_query_builder import SQLQueryBuilder, SQLOperators
from datamodel.models import Interaction, Patient
from injectors import sql_instance
from table_schemas import TableSchema, InteractionSchema, PatientSchema


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
    def __init__(self, connection_obj: Any):
        self.sql_builder = SQLQueryBuilder()
        self.conn = connection_obj

    def get_patient_by_insurance_no(self, insurance_no: str) -> List[Patient]:
        colnames_vs_objs = {col.name: col for col in PatientSchema.columns}
        self.cursor = self.conn.cursor()
        query = (
            self.sql_builder.select(columns=["*"], table=PatientSchema.name)
            .conditions(
                conditions=[
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
        self, insurance_no: int = None, labels: str = None
    ) -> List[Interaction]:
        colnames_vs_objs = {col.name: col for col in InteractionSchema.columns}
        conditions = [(colnames_vs_objs["insurance_no"], SQLOperators.EQ, insurance_no)]
        if labels:
            for label in labels.split(","):
                conditions += [(colnames_vs_objs["label"], SQLOperators.IN, label)]
        self.cursor = self.conn.cursor()
        query = (
            self.sql_builder.select(columns=["*"], table=InteractionSchema.name)
            .conditions(conditions=conditions)
            .construct_query()
        )
        print(query)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        interactions = [Interaction.from_list(row) for row in rows]
        self.cursor.close()
        return interactions

    def create_table(self, schema: TableSchema):
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
        cursor = self.conn.cursor()
        columns, rows = convert_obj_to_lists(objs=data_objs)
        insert_query = self.sql_builder.insert_batch(
            table=table_name, columns=columns
        ).construct_query()
        print(f"Insert query template: {insert_query}")
        print(columns)
        for i in range(0, len(rows), batch_size):
            print(f"Inserting for batch {i+batch_size}")
            cursor.executemany(insert_query, rows[i : i + batch_size])
            self.conn.commit()
        print("Done")

    def insert_interactions(
        self, interactions: List[Interaction], batch_size: int = 100
    ):
        self._insert_items(
            data_objs=interactions,
            table_name=InteractionSchema.name,
            batch_size=batch_size,
        )

    def insert_patients(self, patients: List[Patient], batch_size: int = 100):
        self._insert_items(
            data_objs=patients, table_name=PatientSchema.name, batch_size=batch_size
        )
