import psycopg2

def connect():
    try:
        connection = psycopg2.connect(
            user="postrges",
            password="root",
            host="localhost",
            port=5432
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

connect()
