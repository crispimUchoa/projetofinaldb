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
    
railway = DB('railway', 'dLZGjVutNkAFzasklAeLSqrUaPMrmeKq', 'postgres', 'switchback.proxy.rlwy.net', '41846')