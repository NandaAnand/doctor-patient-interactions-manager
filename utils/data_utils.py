from typing import List, Union, Any, Tuple

from pydantic import BaseModel

from sql_query_builder import SQLQueryBuilder, SQLOperators
from datamodel.models import Interaction, Patient
from injectors import sql_instance
from table_schemas import TableSchema, InteractionSchema, PatientSchema


def convert_obj_to_lists(objs: List[BaseModel]) -> Union[List, List[List]]:
    cols = list(objs[0].model_dump().keys())
    rows = [list(obj.model_dump().values()) for obj in objs]
    return cols, rows


class DataUtils:
    def __init__(self, connection_obj: Any):
        self.sql_builder = SQLQueryBuilder()
        self.conn = connection_obj

    # def get_interactions(self, patient_id: str) -> List[Interaction]:
    #     self.cursor = self.conn.cursor()
    #     query = (
    #         self.sql_builder.select(columns=["*"], table="Interactions")
    #         .conditions(conditions=["Patient_id", SQLOperators.EQ, patient_id])
    #         .limit(limit=10)
    #         .order_by(col="Date", type=SQLOperators.DESC)
    #         .group_by(cols=["label"])
    #         .construct_query()
    #     )

    #     data = self.cursor.execute()
    #     # parse
    #     # data =
    #     self.cursor.close()
    #     return data

    # def get_patient():
    #     pass

    def create_table(self, schema: TableSchema):
        query = self.sql_builder.create(
            schema.name, col_vs_dtypes=schema.col_vs_dtypes
        ).construct_query()
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
