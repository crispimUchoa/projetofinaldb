import psycopg2
from psycopg2 import connect

dbname='railway'
password = 'dLZGjVutNkAFzasklAeLSqrUaPMrmeKq'
user = 'postgres'
host = 'switchback.proxy.rlwy.net'
port = '41846'

conn = connect(dbname=dbname, user=user, host=host, password=password, port=port)
crsr = conn.cursor()
def AVGMedicoConsultas(medico):
	crsr.execute('SELECT ID_Medico_Consulta AS ID_Medico, AVG(Nota) AS Media_Avaliacao FROM Consulta WHERE Nota IS NOT NULL GROUP BY ID_Medico_Consulta')
	return crsr.fetchone()

def BuscarMedicos(medico):
	crsr.execute('SELECT (M.Nome, H.Id_horario, M.Especialização, M.Nota) FROM MEDICO M JOIN HORARIOS H ON M.Id_medico = H.Id_medico JOIN Usuario U ON M.ID_Medico = U.ID_Usuario')
	return crsr.fetchall()

def cadastrar_paciente(nome, email, senha, data_nascimento, cpf, telefone, endereco):
    try:
        query_usuario = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, 'paciente') RETURNING id;"
        crsr.execute(query_usuario, (nome, email, senha))
        usuario_id = crsr.fetchone()

        query_paciente = "INSERT INTO pacientes (usuario_id, data_nascimento, cpf, telefone, endereco) VALUES (%s, %s, %s, %s, %s);"
        valores_paciente = (usuario_id, data_nascimento, cpf, telefone, endereco)
        crsr.execute(query_paciente, valores_paciente)

        conn.commit()
        print("Paciente cadastrado com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar paciente:", e)

    finally:
        crsr.close()
        conn.close()

def mostrarConsultasPaciente(id_paciente):
    crsr.execute('''
        SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
        JOIN HORARIOS H ON M.Id_medico = H.Id_medico
        JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
        JOIN Usuario U ON P.Id_paciente = U.ID_Usuario
        JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
        WHERE P.Id_paciente = %s
    ''', (id_paciente,))
    return crsr.fetchall()

def mostrarConsultasMedico(id_medico):
    crsr.execute('''
        SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
        JOIN HORARIOS H ON M.Id_medico = H.Id_medico
        JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
        JOIN Usuario U ON M.Id_medico = U.ID_Usuario
        JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
        WHERE M.Id_medico = %s
    ''', (id_medico,))
    return crsr.fetchall()