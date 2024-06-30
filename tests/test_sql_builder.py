import unittest
from utils.sql_query_builder import SQLQueryBuilder, SQLOperators, SQLTypes  

class MockColumn:
    """
    A mock column class to simulate table column objects.

    Attributes:
        name (str): The name of the column.
        dtype (SQLTypes): The data type of the column.
    """

    def __init__(self, name, dtype):
        self.name = name
        self.dtype = dtype 


class TestSQLQueryBuilder(unittest.TestCase):
    """
    Test suite for the SQLQueryBuilder class.
    """

    
    def setUp(self):
        """
        Set up the SQLQueryBuilder instance before each test.
        """
        self.sql_builder = SQLQueryBuilder()

    def test_select_query(self):
        """
        Test building a simple SELECT query with no conditions.
        """

        columns = ["col1", "col2"]
        query = self.sql_builder.select(columns=columns, table="table").construct_query()
        expected_query = "SELECT col1,col2 FROM table;"
        self.assertEqual(query, expected_query)

    def test_select_with_conditions(self):
        """
        Test building a simple SELECT query with  conditions.
        """
        columns = ["col1", "col2"]
        mock_col1 = MockColumn(name="col1", dtype=SQLTypes.VARCHAR)
        mock_col2 = MockColumn(name="col2", dtype=SQLTypes.VARCHAR)
        conditions = [(mock_col1, SQLOperators.EQ, "val1"), (mock_col2, SQLOperators.LTE, "val2")]        
        query = (
            self.sql_builder.select(columns=columns, table="table")
            .conditions(conditions=conditions, logical_op=SQLOperators.OR)
            .construct_query()
        )
        expected_query = "SELECT col1,col2 FROM table WHERE table.col1 = 'val1' AND table.col2 <= 'val2';"
        self.assertEqual(query, expected_query)

    def test_select_with_order_by(self):
        """
            Test building a SELECT query with an ORDER BY clause.
        """
        columns = ["col1", "col2"]
        query = (
            self.sql_builder.select(columns=columns, table="table")
            .order_by(col="col1", type=SQLOperators.ASC)
            .construct_query()
        )
        expected_query = "SELECT col1,col2 FROM table ORDER BY col1 ASC;"
        self.assertEqual(query, expected_query)

    def test_select_with_limit(self):
        """
        Test building a SELECT query with a LIMIT clause.
        """
        columns = ["col1", "col2"]
        query = (
            self.sql_builder.select(columns=columns, table="table")
            .limit(limit=10)
            .construct_query()
        )
        expected_query = "SELECT col1,col2 FROM table LIMIT 10;"
        self.assertEqual(query, expected_query)

    def test_select_with_offset(self):
        """
        Test building a SELECT query with a OFFSET clause.
        """
        columns = ["col1", "col2"]
        query = (
            self.sql_builder.select(columns=columns, table="table")
            .offset(offset=5)
            .construct_query()
        )
        expected_query = "SELECT col1,col2 FROM table OFFSET 5;"
        self.assertEqual(query, expected_query)

    def test_select_with_group_by(self):
        """
        Test building a SELECT query with a GROUPBY clause.
        """
        columns = ["col1", "col2"]
        query = (
            self.sql_builder.select(columns=columns, table="table")
            .group_by(cols=["col1", "col2"])
            .construct_query()
        )
        expected_query = "SELECT col1,col2 FROM table GROUP BY col1,col2;"
        self.assertEqual(query, expected_query)

    def test_create_table_query(self):
        """
        Test building a CREATE TABLE query.
        """
        class Column:
            """
            A mock column class to simulate table column objects for CREATE TABLE queries.

            Attributes:
                name (str): The name of the column.
                dtype (SQLTypes): The data type of the column.
            """
            def __init__(self, name, dtype):
                self.name = name
                self.dtype = dtype

        class Table:
            """
            A mock table class to simulate table objects for CREATE TABLE queries.

            Attributes:
                name (str): The name of the table.
                columns (List[Column]): The list of columns in the table.
                constraints (List[str]): The list of constraints in the table.
            """
            def __init__(self, name, columns, constraints):
                self.name = name
                self.columns = columns
                self.constraints = constraints

        columns = [Column(name="id", dtype=SQLTypes.AUTO_INCREMENT), Column(name="name", dtype=SQLTypes.VARCHAR)]
        constraints = ["PRIMARY KEY (id)"]
        table = Table(name="test_table", columns=columns, constraints=constraints)

        query = self.sql_builder.create(table=table).construct_query()
        expected_query = "CREATE TABLE IF NOT EXISTS test_table (id INT AUTO_INCREMENT,name VARCHAR(255), PRIMARY KEY (id));"
        self.assertEqual(query, expected_query)

    def test_insert_batch_query(self):
        """
        Test building an INSERT INTO query.
        """
        columns = ["col1", "col2"]
        query = self.sql_builder.insert_batch(table="table", columns=columns).construct_query()
        expected_query = "INSERT INTO table (col1,col2) VALUES (%s,%s);"
        self.assertEqual(query, expected_query)

if __name__ == "__main__":
    unittest.main()
