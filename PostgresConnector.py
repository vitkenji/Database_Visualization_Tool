import psycopg2

# Só ctr c ctr v do código do MySQL

class PostgresConnector:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.mydb = None
        self.cursor = None

    def connect(self):
        try:
            connection = psycopg2.connect(
                user="root",
                password="root",
                host="localhost",
                port=3306
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")

    def select_schema(self, schema):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=schema
            )
            self.cursor = self.mydb.cursor()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def get_databases(self):
        try:
            self.cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in self.cursor.fetchall()]
            return databases
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_tables(self, database):
        try:
            self.cursor.execute(f"USE {database}")
            self.cursor.execute("SHOW TABLES")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def get_columns(self, database, table):
        try:
            self.cursor.execute(f"USE {database}")
            self.cursor.execute(f"DESCRIBE `{table}`")
            columns = []
            for column in self.cursor.fetchall():
                column_info = {
                    'Field': column[0],
                    'Type': column[1],
                    'Null': column[2],
                    'Key': column[3],
                    'Default': column[4]
                }
                columns.append(column_info)
            return columns
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None

