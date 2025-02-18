from db import db

connection = db.connection()
cursor = connection.cursor()
sql = 'CREATE TABLE Usuario (id SEIRAL PRIMARY KEY, nome VARCHAR(50) NOT NULL, senha VARCHAR(50) NOT NULL), Email VARCHAR(50) NOT NULL, UNIQUE (Senha));'

try:
    cursor.execute(sql)
    print('inserido por sucesso')
except Exception as error:
    print('erro:', error)
    

cursor.close()
connection.close()