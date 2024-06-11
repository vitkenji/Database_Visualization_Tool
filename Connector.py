import mysql.connector

class MySQLConnector:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.mydb = None
        self.cursor = None

    def connect(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user=self.user,
                password=self.password
            )
            self.cursor = self.mydb.cursor()
            self.cursor.execute("SHOW DATABASES")
            response = self.cursor.fetchall()
            return True, response
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, []

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

    def get_column_information(self, column):
        if not self.mydb or not self.cursor:
            print("Error: no database connected")
            return

        if ' ' in column:
            print("Error: weird column name")
            return

        self.cursor.execute(f"DESCRIBE `{column}`")
        response = self.cursor.fetchall()
        print(response)
