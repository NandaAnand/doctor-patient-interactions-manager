from typing import List, Tuple

from sql_query_builder import SQLQueryBuilder, SQLOperators
from datamodel import Interaction
from injectors import sql_instance


class DataUtils:
    def init(self):
        pass

    def get_interactions(self, patient_id: str) -> List[Interaction]:
        self.cursor = self.conn.cursor()

        query = (
            self.sql_builder.select(columns=["*"], table="Interactions")
            .conditions(conditions=["Patient_id", SQLOperators.EQ, patient_id])
            .limit(limit=10)
            .order_by(col="Date", type=SQLOperators.DESC)
            .group_by(cols=["label"])
            .construct_query()
        )

        data = self.cursor.execute()
        # parse
        # data =
        self.cursor.close()
        return data

    def get_patient():
        pass

    def insert_interactions(
        self, interactions: List[Interaction], batch_size: int = 100
    ):
        cursor = self.conn.cursor()
        columns = list(interactions[0].dict().keys())
        rows = [tuple(interaction.to_dict().values()) for interaction in interactions]
        insert_query = self.sql_builder.insert(
            "Interaction", columns=columns
        ).construct_query()

        # TODO include batch wise upload
        for i in range(0, batch_size):
            print(f"Inserting for batch {i+batch_size}")
            cursor.executeMany(insert_query, rows[i : i + batch_size])
            self.conn.commit()
        cursor.close()
