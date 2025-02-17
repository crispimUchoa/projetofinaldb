import psycopg2
from db import railway

def AVGMedicoConsultas(medico):
    conn = railway.connection()
    crsr = conn.cursor()
    crsr.execute('SELECT ID_Medico_Consulta AS ID_Medico, AVG(Nota) AS Media_Avaliacao FROM Consulta WHERE Nota IS NOT NULL GROUP BY ID_Medico_Consulta')
    crsr.fetchone()
    conn.commit()
    tabela_resultado = crsr.fetchone()
    crsr.close()
    conn.close()
    return tabela_resultado    
    
def BuscarMedicos(medico):

    conn = railway.connection()
    crsr = conn.cursor()
    crsr.execute('SELECT (M.Nome, H.Id_horario, M.Especialização, M.Nota) FROM MEDICO M JOIN HORARIOS H ON M.Id_medico = H.Id_medico JOIN Usuario U ON M.ID_Medico = U.ID_Usuario')
    tabela_resultado = crsr.fetchone()
    crsr.close()
    conn.close()
    return tabela_resultado
    

def cadastrar_paciente(nome, email, senha, data_nascimento, cpf, telefone, endereco):
    try:
        conn = railway.connection()
        crsr1 = conn.cursor()
        crsr2 = conn.cursor()
        query_usuario = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, 'paciente') RETURNING id;"
        crsr1.execute(query_usuario, (nome, email, senha))
        usuario_id = crsr1.fetchone()

        query_paciente = "INSERT INTO pacientes (usuario_id, data_nascimento, cpf, telefone, endereco) VALUES (%s, %s, %s, %s, %s);"
        valores_paciente = (usuario_id, data_nascimento, cpf, telefone, endereco)
        crsr2.execute(query_paciente, valores_paciente)

        conn.commit()
        print("Paciente cadastrado com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar paciente:", e)

    finally:
        crsr1.close()
        crsr2.close()
        conn.close()

def mostrarConsultasPaciente(id_paciente):
    conn = railway.connection()
    crsr = conn.cursor()
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
    tabela_resultado = crsr.fetchall()
    crsr.close()
    conn.close()
    return tabela_resultado    

def mostrarConsultasMedico(id_medico):
    conn = railway.connection()
    crsr = conn.cursor()
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
    tabela_resultado = crsr.fetchall()
    crsr.close()
    conn.close()
    return tabela_resultado    