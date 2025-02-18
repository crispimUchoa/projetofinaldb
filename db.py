from psycopg2 import connect

class DB():
    def __init__ (self, dbname, password, user, host, port):
        self.dbname = dbname
        self.password = password
        self.user = user
        self.host = host
        self.port = port
        
    def connection(self):
        conn = connect(dbname=self.dbname,password=self.password,user=self.user,host=self.host,port=self.port)
        return conn
    
db = DB('flask_db', 'Chtehe112327!', 'postgres', 'localhost', '5432')