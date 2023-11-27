import sqlite3

class Connection:

    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        if not self.conn or not self.cursor:
            raise RuntimeError("A conexão com o banco de dados não foi estabelecida. Chame o método 'connect' primeiro.")
        
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        if self.conn:
            self.conn.close()