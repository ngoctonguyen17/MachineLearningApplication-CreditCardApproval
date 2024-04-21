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

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password)
            return self.conn
        except:
            traceback.print_exc()
        return None

    def commit(self):
        if self.conn != None:
            self.conn.commit()
    def disConnect(self):
        if self.conn != None:
            self.conn.close()

    def queryDataset(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall())
            df.columns = cursor.column_names
            return df
        except:
            traceback.print_exc()

        return None