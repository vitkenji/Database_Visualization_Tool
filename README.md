# **Database Visualization**

## **Description**

This project is a semi-graphical tool for database visualization, allowing users to explore PostgreSQL and MySQL databases interactively and intuitively. Through a simple graphical interface, users can view tables, fields, primary keys, query data, and export results in CSV or JSON formats.

## **Features**

- **Connect to PostgreSQL and MySQL Databases:** The program allows connection to both PostgreSQL and MySQL databases.
- **Save Connection Data:** The program stores connection information, making it easier to access recurring databases.
- **View Tables and Views:** Displays the tables and views of the database in a tree structure.
- **Show Table Fields:** Shows the fields of each table, including their types and sizes.
- **Primary Keys:** Indicates the primary keys of each table.
- **Query Data:** Allows querying the data of a table, with the option to limit the number of records displayed (up to 1000, configurable).
- **Run SQL Queries:** Users can input and execute SQL queries directly.
- **Export Data:** Provides options to export table data or query results in CSV or JSON formats.

## **Technologies Used**

- **Python**
- **Tkinter**
- **psycopg2**
- **mysql-connector-python**
