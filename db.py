from psycopg2 import connect
from dotenv import load_dotenv
import os
load_dotenv()


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
    
db = DB(os.getenv('DB_NAME'), os.getenv('PASSWORD'), os.getenv('USER'), os.getenv('HOST'), os.getenv('PORT'))
