from typing import List, Any, Tuple, Literal, Dict, Union
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
    def init(self):
        self.query = ""

    def select(
        self,
        columns: List[str],
        table: str,
    ) -> Any:
        self.query = f"SELECT {','.join(columns)} FROM {table}"
        return self

    def conditions(self, conditions: List[Tuple]) -> Any:
        self.query += f" WHERE {' AND '.join([f'{col1} {op.value} {col2}' for col1, op, col2 in conditions])}"  # Need to iterate over conditions, (col, gte, val), (col, eq, val),
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

    def create(self, table: str, columns: List[Union[Tuple[str, SQLTypes], str]]):
        def _format_column_definition(col: Union[Tuple[str, SQLTypes], str]):
            if isinstance(col, str):
                return col
            name, datatype = col
            return f"{name} {datatype.value}"

        self.query = f"""CREATE TABLE IF NOT EXISTS {table} ({','.join([_format_column_definition(col) for col in columns])})"""
        return self

    def insert(self, table: str, columns: List[str]):
        self.query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['?'] * len(columns))})"
        return self

    def construct_query(self):
        return self.query + ";"


if __name__ == "__main__":
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
