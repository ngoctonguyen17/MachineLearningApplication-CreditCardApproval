import mysql.connector
import traceback
import pandas as pd


class Connector:
    def __init__(self, server=None, port=None, database=None, username=None, password=None):
        self.server = server
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.conn = None  # Khởi tạo conn là None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password)
            print("Connection established to the database.")
            return self.conn
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            traceback.print_exc()
        return None

    def commit(self):
        if self.conn:
            self.conn.commit()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def queryDataset(self, sql):
        if self.conn is None:
            raise ValueError("Connection to the database is not established.")

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall())
            df.columns = cursor.column_names
            return df
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            traceback.print_exc()
        return None

    def getTablesName(self):
        if self.conn is None:
            raise ValueError("Connection to the database is not established.")

        try:
            cursor = self.conn.cursor()
            cursor.execute("SHOW TABLES;")
            results = cursor.fetchall()
            tablesName = [item[0] for item in results]
            return tablesName
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            traceback.print_exc()
        return []