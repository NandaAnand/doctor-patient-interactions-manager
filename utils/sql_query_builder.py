from typing import List, Any, Tuple
from enum import Enum


class SQLOperators(Enum):
    GTE = ">="
    LTE = "<="
    EQ = "="
    IN = "IN"
    ASC = "ASC"
    DESC = "DESC"


class SQLTypes(Enum):
    VARCHAR = "VARCHAR(255)"
    INT = "INT"
    DATE = "DATE"
    TEXT = "TEXT"
    AUTO_INCREMENT = "INT AUTO_INCREMENT"
    PRIMARY_KEY = "PRIMARY KEY"
    FOREIGN_KEY = "FOREIGN KEY"


class SQLQueryBuilder:
    from table_schemas import TableSchema

    def __init__(self):
        self.query = ""

    def select(
        self,
        columns: List[str],
        table: str,
    ) -> Any:
        self.table = table
        self.query = f"SELECT {','.join(columns)} FROM {table}"
        return self

    def conditions(self, conditions: List[Tuple]) -> Any:
        # iterate over conditions, (col, gte, val), (col, eq, val)
        conditions_queries = []
        for col, op, val in conditions:
            if col.dtype == SQLTypes.INT:
                conditions_queries.append(f"{self.table}.{col.name} {op.value} {val}")
            else:
                conditions_queries.append(f"{self.table}.{col.name} {op.value} '{val}'")
        self.query += f" WHERE {' AND '.join(conditions_queries)}"
        return self

    def order_by(self, col: str, type: SQLOperators) -> Any:
        self.query += f" ORDER BY {col} {type.value}"
        return self

    def limit(self, limit: int) -> Any:
        self.query += f" LIMIT {limit}"
        return self

    def offset(self, offset: int) -> Any:
        self.query += f" OFFSET {offset}"
        return self

    def group_by(self, cols: List[str]) -> Any:
        self.query += f" GROUP BY {','.join(cols)}"
        return self

    def create(self, table: TableSchema):
        if table.constraints:
            constraints = ", ".join(table.constraints)
        self.query = f"""CREATE TABLE IF NOT EXISTS {table.name} ({','.join([f"{column.name} {column.dtype.value}" for column in table.columns])}, {constraints})"""
        return self

    def insert_batch(self, table: str, columns: List[str]):
        self.query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s'] * len(columns))})"
        return self

    def construct_query(self):
        return self.query + ";"


if __name__ == "__main__":
    # Testing query building
    sql_builder = SQLQueryBuilder()
    columns = ["col1", "col2"]
    conditions = [("col1", SQLOperators.EQ, "val1"), ("col2", SQLOperators.LTE, "val2")]
    query = (
        sql_builder.select(columns=columns, table="table")
        .conditions(conditions=conditions)
        .limit(limit=10)
        .order_by(col="col1", type=SQLOperators.ASC)
        .group_by(cols=["col1", "col2"])
        .construct_query()
    )

    print(query)
