import pandas as pd
from injectors import sql_instance
from sql_query_builder import SQLQueryBuilder
from table_schema import (
    patients_columns,
    PATIENT_TABLE,
    INTERACTION_TABLE,
    interaction_columns,
)


def main():
    connection = sql_instance()
    if not connection:
        return
    sql_builder = SQLQueryBuilder()
    query = sql_builder.create(PATIENT_TABLE, patients_columns).construct_query()
    print(query)
    query = sql_builder.create(INTERACTION_TABLE, interaction_columns).construct_query()
    print(query)


if __name__ == "__main__":
    main()
