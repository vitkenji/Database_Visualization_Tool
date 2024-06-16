import psycopg2
from psycopg2 import sql

class PostgresConnector:
    def __init__(self, user, password, host='localhost', port=5432):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            schemas = self.cursor.fetchall()
            return True, schemas
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return False, []

    def select_schema(self, schema):
        try:
            self.connection.close()
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=schema
            )
            self.cursor = self.connection.cursor()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return False

    def get_databases(self):
        try:
            self.cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = [db[0] for db in self.cursor.fetchall()]
            return databases
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return []

    def get_tables(self, schema):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return []

    def get_columns(self, schema, table):
        try:
            self.cursor.execute(sql.SQL("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = %s
            """), [table])
            columns = []
            for column in self.cursor.fetchall():
                column_info = {
                    'Field': column[0],
                    'Type': column[1],
                    'Null': column[2],
                    'Default': column[3]
                }
                columns.append(column_info)
            return columns
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return []

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error executing query: {error}")
            return None
