# import psycopg2
# from db import db
# from entities.Medico import Medico
# from entities.Horario import Horario
# from entities.Paciente import Paciente

# def AVGMedicoConsultas(id_medico):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_avg = ('SELECT ID_Medico_Consulta AS ID_Medico, AVG(Nota) AS Media_Avaliacao FROM Consulta WHERE Nota IS NOT AND ID_Medico = %s NULL GROUP BY ID_Medico_Consulta')
#     crsr.execute(query_avg, (id_medico,))
#     crsr.fetchone()
#     conn.commit()
#     tabela_resultado = crsr.fetchone()
#     crsr.close()
#     conn.close()
#     return tabela_resultado    
    
# def BuscarMedicos():

#     conn = db.connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT (M.Id_medico, U.Nome, M.Especializacao, M.Avaliacao) FROM MEDICO M INNER JOIN Usuario U ON M.ID_Medico = U.ID_Usuario')
#     result_medicos = cursor.fetchall()
#     medicos = list()
#     cursor.close()
#     for id, nome, especializacao, avaliacao in result_medicos:
#         horarios = []
#         cursor = conn.cursor()
#         cursor.execute(f'SELECT * FROM HORARIOS WHERE ID_MEDICO = {id}')
#         result_horarios = cursor.fetchall()
#         for id_medico, id_horario in result_horarios:
#             horario = Horario(id_medico, id_horario)
#             horarios.append(horario)
#             medico = Medico(id=id, nome=nome, especializacao=especializacao, horarios=horarios, avaliacao=avaliacao, horarios=horarios)
#             medicos.append(medico)

#     return medicos


# def cadastrar_paciente(nome, email, senha, data_nascimento, telefone):
#     try:
#         conn = db.connection()
#         crsr1 = conn.cursor()
#         crsr2 = conn.cursor()
#         query_usuario = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s RETURNING id;"
#         crsr1.execute(query_usuario, (nome, email, senha))
#         paciente_id = crsr1.fetchone()[0]

#         query_paciente = "INSERT INTO paciente (id_paciente, data_nascimento, telefone) VALUES (%s, %s, %s);"
#         valores_paciente = (paciente_id, data_nascimento,telefone)
#         crsr2.execute(query_paciente, valores_paciente)

#         conn.commit()
#         print("Paciente cadastrado com sucesso!")

#     except psycopg2.Error as e:
#         conn.rollback()
#         print("Erro ao cadastrar paciente:", e)

#     finally:
#         crsr1.close()
#         crsr2.close()
#         conn.close()

# def cadastrar_medico(nome, email, senha, especializacao, horarios, avaliacao, atende_plantao):
#     try:
#         conn = db.connection()
#         crsr1 = conn.cursor()
#         crsr2 = conn.cursor()
#         query_usuario = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_usuario;"
#         crsr1.execute(query_usuario, (nome, email, senha))
#         medico_id = crsr1.fetchone()[0]

#         query_medico = "INSERT INTO medico (id_medico, especializacao, horarios, avaliacao, atende_plantao) VALUES (%s, %s, %s, %s, %s);"
#         valores_medico = (medico_id, especializacao, horarios, avaliacao, atende_plantao)
#         crsr2.execute(query_medico, valores_medico)

#         conn.commit()
#         print("Medico cadastrado com sucesso!")

#     except psycopg2.Error as e:
#         conn.rollback()
#         print("Erro ao cadastrar medico:", e)

#     finally:
#         crsr1.close()
#         crsr2.close()
#         conn.close()

# def adicionar_Prescricao(id_consulta, nome_composto_medicamento, observacao):
#     try:
#         conn = db.connection()
#         crsr = conn.cursor()
#         query_usuario = "INSERT INTO prescricao (id_consulta, nome_composto_medicamento, observacao) VALUES (%s, %s, %s, %s);"
#         crsr.execute(query_usuario, (id_consulta, nome_composto_medicamento, observacao))

#         conn.commit()
#         print("Prescricao escrita com sucesso!")

#     except psycopg2.Error as e:
#         conn.rollback()
#         print("Erro ao enviar prescricao:", e)

#     finally:
#         crsr.close()
#         conn.close()

# def mostrarConsultasPaciente(id_paciente):
#     conn = db.connection()
#     crsr = conn.cursor()
#     crsr.execute('''
#         SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
#         FROM CONSULTA C
#         JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
#         JOIN HORARIOS H ON M.Id_medico = H.Id_medico
#         JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
#         JOIN Usuario U ON M.id_medico = U.ID_Usuario
#         JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
#         WHERE P.Id_paciente = %s
#     ''', (id_paciente,))
#     tabela_resultado = crsr.fetchall()
#     crsr.close()
#     conn.close()
#     return tabela_resultado    

# def mostrarConsultasMedico(id_medico):
#     conn = db.connection()
#     crsr = conn.cursor()
#     crsr.execute('''
#         SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
#         FROM CONSULTA C
#         JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
#         JOIN HORARIOS H ON M.Id_medico = H.Id_medico
#         JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
#         JOIN Usuario U ON P.Id_paciente = U.ID_Usuario
#         JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
#         WHERE M.Id_medico = %s
#     ''', (id_medico,))
#     tabela_resultado = crsr.fetchall()
#     crsr.close()
#     conn.close()
#     return tabela_resultado

# def mostrarMedicoLog(email, senha):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM MEDICO M INNER JOIN USUARIO U ON M.Id_medico = U.Id_Usuario %s = U.email AND %s = U.senha')
#     crsr.execute(query_busca, (email, senha))
#     tabela_resultado = crsr.fetchone()
#     crsr.close()
#     conn.close()
#     return tabela_resultado

# def mostarHorarios(medico):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM HORARIO H JOIN MEDICO M WHERE %s = H.Id_medico')
#     crsr.execute(query_busca, (medico.id,))
#     tabela_resultado = crsr.fetchall()
#     crsr.close()
#     conn.close()
#     return tabela_resultado

# def mostarConsulta(medico):
#     medicoref = Medico(medico)
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM CONSLUTA C JOIN MEDICO M WHERE %s = C.Id_medico_consulta')
#     crsr.execute(query_busca, (medicoref.id,))
#     tabela_resultado = crsr.fetchall()
#     crsr.close()
#     conn.close()
#     return tabela_resultado

# def mostrarPrescricao(id_consulta):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM PRESCRICAO P WHERE %s = P.Id_consulta')
#     crsr.execute(query_busca, (id_consulta,))
#     tabela_resultado = crsr.fetchall()
#     crsr.close()
#     conn.close()
#     return tabela_resultado

# def removerHorario(id_medico, horario):
#     try:
#         conn = db.connection()
#         crsr = conn.cursor()
#         query_busca = ('DELETE FROM HORARIO H WHERE %s = H.id_medico AND %s = H.horario')
#         crsr.execute(query_busca, (id_medico, horario))
#     except psycopg2.Error as e:
#         conn.rollback()
#         print("Erro ao enviar prescricao:", e)
#     finally:
#         crsr.close()
#         conn.close()

# def obterClassePaciente(id_paciente):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM USUARIO U INNER JOIN PACIENTE P ON U.Id_usuario = P.Id_paciente AND P.Id_paciente = %s')
#     crsr.execute(query_busca, id_paciente)
#     id, nome, senha, email, id_prov, plano_de_saude, data_nascimento, necessidade_especial, telefone = crsr.fetchone()
#     return Paciente(id, nome, senha, email, plano_de_saude, data_nascimento, necessidade_especial, telefone)

# def obterClasseMedico(id_medico):
#     conn = db.connection()
#     crsr = conn.cursor()
#     query_busca = ('SELECT * FROM USUARIO U INNER JOIN MEDICO M ON U.Id_usuario = P.Id_medico AND P.Id_medico = %s')
#     crsr.execute(query_busca, id_medico)
#     id, nome, senha, email, id_prov, especializacao, horarios, avaliacao, atende_plantao = crsr.fetchone()
#     return Medico(id, nome, senha, email, especializacao, horarios, avaliacao, atende_plantao)

# """
#     SELECT:
#     -medico que email e senha sejam iguais aos logados *
#     -todos os horarios em que horarios.id_medico = medico.id -
#     -todas as consultas que consulta.id_medico = medico.id 
#     -a consulta em que consulta.id = consulta.id_consulta -
#     -todas as prescrições em que prescricao.id_consulta = id_consulta *

#     INSERT:
#     -insere medico cadastrado no banco
#     -insere nova prescricao -
#     -insere novo horario

#     DELETE:
#     -deleta horario removido *
    
#     Funções:
#     -Obter_Paciente *
#     -Obter_Medico *
# """