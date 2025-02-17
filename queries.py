import psycopg2
from db import railway
from entities.Medico import Medico
import entities.Horario
from entities.Paciente import Paciente

def AVGMedicoConsultas(Medico):
    conn = railway.connection()
    crsr = conn.cursor()
    query_avg = ('SELECT ID_Medico_Consulta AS ID_Medico, AVG(Nota) AS Media_Avaliacao FROM Consulta WHERE Nota IS NOT AND ID_Medico = %s NULL GROUP BY ID_Medico_Consulta')
    crsr.execute(query_avg, (Medico.id,))
    crsr.fetchone()
    conn.commit()
    tabela_resultado = crsr.fetchone()
    crsr.close()
    conn.close()
    return tabela_resultado    
    
def BuscarMedicos():

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
        query_usuario = "INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, 'paciente') RETURNING id;"
        crsr1.execute(query_usuario, (nome, email, senha))
        usuario_id = crsr1.fetchone()

        query_paciente = "INSERT INTO paciente (usuario_id, data_nascimento, cpf, telefone, endereco) VALUES (%s, %s, %s, %s, %s);"
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

def cadastrar_medico(nome, email, senha, especializacao, horarios, avaliacao=0, atende_plantao=True):
    try:
        conn = railway.connection()
        crsr1 = conn.cursor()
        crsr2 = conn.cursor()
        query_usuario = "INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, 'paciente') RETURNING id;"
        crsr1.execute(query_usuario, (nome, email, senha))
        usuario_id = crsr1.fetchone()

        query_paciente = "INSERT INTO medico (usuario_id, especializacao, horarios, avaliacao, atende_plantao) VALUES (%s, %s, %s, %s, %s);"
        valores_paciente = (usuario_id, especializacao, horarios, avaliacao, atende_plantao)
        crsr2.execute(query_paciente, valores_paciente)

        conn.commit()
        print("Medico cadastrado com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar medico:", e)

    finally:
        crsr1.close()
        crsr2.close()
        conn.close()

def adicionar_Prescricao(id_consulta, nome_composto_medicamento, observacao):
    try:
        conn = railway.connection()
        crsr = conn.cursor()
        query_usuario = "INSERT INTO prescricao (id_consulta, nome_composto_medicamento, observacao) VALUES (%s, %s, %s, %s);"
        crsr.execute(query_usuario, (id_consulta, nome_composto_medicamento, observacao))

        conn.commit()
        print("Prescricao escrita com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao enviar prescricao:", e)

    finally:
        crsr.close()
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

def mostrarMedicoLog(email, senha):
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM MEDICO M JOIN USUARIO U WHERE M.Id_medico = U.Id_Usuario %s = U.email AND %s = U.senha')
    crsr.execute(query_busca, (email, senha))
    tabela_resultado = crsr.fetchone()
    crsr.close()
    conn.close()
    return tabela_resultado

def mostarHorarios(medico):
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM HORARIO H JOIN MEDICO M WHERE %s = H.Id_medico')
    crsr.execute(query_busca, (medico.id,))
    tabela_resultado = crsr.fetchall()
    crsr.close()
    conn.close()
    return tabela_resultado

def mostarConsulta(medico):
    medicoref = Medico(medico)
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM CONSLUTA C JOIN MEDICO M WHERE %s = C.Id_medico_consulta')
    crsr.execute(query_busca, (medicoref.id,))
    tabela_resultado = crsr.fetchall()
    crsr.close()
    conn.close()
    return tabela_resultado

def mostrarPrescricao(id_consulta):
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM PRESCRICAO P WHERE %s = P.Id_consulta')
    crsr.execute(query_busca, (id_consulta,))
    tabela_resultado = crsr.fetchall()
    crsr.close()
    conn.close()
    return tabela_resultado

#Inacabados

def removerHorario(Horario):
    try:
        id_horario = entities.Horario.horario
        conn = railway.connection()
        crsr = conn.cursor()
        query_busca = ('DELETE * FROM HORARIO H WHERE %s = H.Id_horario')
        crsr.execute(query_busca, (id_horario,))
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao enviar prescricao:", e)
    finally:
        crsr.close()
        conn.close()

def obter_paciente(id_paciente):
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM USUARIO U JOIN PACIENTE P WHERE WHERE U.Id_usuario = P.Id_paciente AND P.Id_paciente = %s')
    crsr.execute(query_busca, id_paciente)
    crsr.fetchall()
    return

def obter_medico(id_medico):
    conn = railway.connection()
    crsr = conn.cursor()
    query_busca = ('SELECT * FROM USUARIO U JOIN MEDICO M WHERE WHERE U.Id_usuario = P.Id_medico AND P.Id_medico = %s')
    crsr.execute(query_busca, id_medico)
    crsr.fetchall()
    return

"""
    SELECT:
    -medico que email e senha sejam iguais aos logados *
    -todos os horarios em que horarios.id_medico = medico.id -
    -todas as consultas que consulta.id_medico = medico.id 
    -a consulta em que consulta.id = consulta.id_consulta -
    -todas as prescrições em que prescricao.id_consulta = id_consulta *

    INSERT:
    -insere medico cadastrado no banco
    -insere nova prescricao -
    -insere novo horario

    DELETE:
    -deleta horario removido
    
    Funções:
    -Obter_Paciente
    -Obter_Medico
"""