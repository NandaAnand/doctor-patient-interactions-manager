from typing import List, Any, Optional, Tuple
from enum import Enum


class SQLOperators(Enum):
    """
    Enum for SQL Operators and keywords
    """

    GTE = ">="
    LTE = "<="
    EQ = "="
    IN = "IN"
    ASC = "ASC"
    DESC = "DESC"
    CONTAINS = "CONTAINS"
    LIKE = "LIKE"
    LOWER = "LOWER"
    AND = " AND "
    OR = " OR "


class SQLTypes(Enum):
    """
    Enum for SQL datatypes
    """

    VARCHAR = "VARCHAR(255)"
    INT = "INT"
    DATE = "DATE"
    TEXT = "TEXT"
    AUTO_INCREMENT = "INT AUTO_INCREMENT"
    PRIMARY_KEY = "PRIMARY KEY"
    FOREIGN_KEY = "FOREIGN KEY"


class SQLQueryBuilder:
    """
    Class for building SQL Queries
    """

    def __init__(self):
        self.query = ""

    def select(
        self,
        columns: List[str],
        table: str,
    ) -> Any:

        """
        Build a SELECT query.

        Args:
            columns (List[str]): List of column names to select.
            table (str): Name of the table.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.table = table
        self.query = f"SELECT {','.join(columns)} FROM {table}"
        return self

    def conditions(
        self, conditions: List[Tuple], logical_op: Optional[str] = None
    ) -> Any:

        """
        Add condiotions to query.

        Args:
            conditions (List[Tuple]): List of conditions, each tuple of (column, operator, value)
            logical_op (str): Logical operator to join multiple conditions

        Returns:
            self: The SQLQueryBuilder instance.
        """
        # iterate over conditions, (col, gte, val), (col, eq, val)
        conditions_queries = []
        for col, op, val in conditions:
            if col.dtype == SQLTypes.INT:
                conditions_queries.append(f"{self.table}.{col.name} {op.value} {val}")
            else:
                conditions_queries.append(f"{self.table}.{col.name} {op.value} '{val}'")
        if len(conditions_queries) > 1:
            self.query += f" WHERE {conditions_queries[0] + ' AND ' + f'{logical_op.value}'.join(conditions_queries[1:])}"
        else:
            self.query += f" WHERE {' AND '.join(conditions_queries)}"
        return self

    def order_by(self, col: str, type: SQLOperators) -> Any:
        """
        Add an ORDER BY clause to the query.

        Args:
            col (str): Column name to order by.
            type (SQLOperators): Order type (ASC or DESC).

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.query += f" ORDER BY {col} {type.value}"
        return self

    def limit(self, limit: int) -> Any:
        """
        Add a LIMIT clause to the query.

        Args:
            limit (int): Maximum number of rows to return.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.query += f" LIMIT {limit}"
        return self

    def offset(self, offset: int) -> Any:
        """
        Add an OFFSET clause to the query.

        Args:
            offset (int): Number of rows to skip before starting to return rows.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.query += f" OFFSET {offset}"
        return self

    def group_by(self, cols: List[str]) -> Any:
        """
        Add a GROUP BY clause to the query.

        Args:
            cols (List[str]): List of column names to group by.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.query += f" GROUP BY {','.join(cols)}"
        return self

    def create(self, table: Any):
        """
        Build a CREATE TABLE query.

        Args:
            table (Any): Table schema object with name, columns, and constraints.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        if table.constraints:
            constraints = ", ".join(table.constraints)
        self.query = f"""CREATE TABLE IF NOT EXISTS {table.name} ({','.join([f"{column.name} {column.dtype.value}" for column in table.columns])}, {constraints})"""
        return self

    def insert_batch(self, table: str, columns: List[str]):
        """
        Build an INSERT INTO query for batch insertion.

        Args:
            table (str): Name of the table.
            columns (List[str]): List of column names.

        Returns:
            self: The SQLQueryBuilder instance.
        """
        self.query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['%s'] * len(columns))})"
        return self

    def construct_query(self):
        """
        Construct and return the final query string.

        Returns:
            str: The final SQL query string.
        """

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
