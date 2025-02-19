import psycopg2
from db import db
from entities.Medico import Medico
from entities.Horario import Horario
from entities.Paciente import Paciente
from entities.Consulta import Consulta
from entities.Prescricao import Prescricao

def AVGMedicoConsultas(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    query_avg = ('SELECT ID_Medico_Consulta AS ID_Medico, AVG(Nota) AS Media_Avaliacao FROM Consulta WHERE Nota IS NOT AND ID_Medico = %s NULL GROUP BY ID_Medico_Consulta')
    cursor.execute(query_avg, (id_medico,))
    cursor.fetchone()
    conn.commit()
    tabela_resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return tabela_resultado    
    
def BuscarMedicos():

    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('SELECT M.Id, U.Nome, M.Especializacao, M.Avaliacao FROM MEDICO M INNER JOIN Usuario U ON M.ID = U.ID')
    result_medicos = cursor.fetchall()
    medicos = list()
    cursor.close()
    for id, nome, especializacao, avaliacao in result_medicos:
        horarios = []
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM HORARIOS WHERE ID_MEDICO = %s', (id,))
        result_horarios = cursor.fetchall()
        for id_medico, id_horario in result_horarios:
            horario = Horario(id_medico, id_horario)
            horarios.append(horario)
        medico = Medico(id, nome, '', '', especializacao, horarios, avaliacao, 'sim')
        medicos.append(medico)
    return medicos


def cadastrar_paciente(nome, email, senha, data_nascimento, telefone):
    try:
        conn = db.connection()
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        query_usuario = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s RETURNING id;"
        cursor1.execute(query_usuario, (nome, email, senha))
        paciente_id = cursor1.fetchone()[0]

        query_paciente = "INSERT INTO paciente (id_paciente, data_nascimento, telefone) VALUES (%s, %s, %s);"
        valores_paciente = (paciente_id, data_nascimento,telefone)
        cursor2.execute(query_paciente, valores_paciente)

        conn.commit()
        print("Paciente cadastrado com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar paciente:", e)

    finally:
        cursor1.close()
        cursor2.close()
        conn.close()

def cadastrar_medico(nome, email, senha, especializacao, horarios, avaliacao, atende_plantao):
    try:
        conn = db.connection()
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        query_usuario = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_usuario;"
        cursor1.execute(query_usuario, (nome, email, senha))
        medico_id = cursor1.fetchone()[0]

        query_medico = "INSERT INTO medico (id_medico, especializacao, horarios, avaliacao, atende_plantao) VALUES (%s, %s, %s, %s, %s);"
        valores_medico = (medico_id, especializacao, horarios, avaliacao, atende_plantao)
        cursor2.execute(query_medico, valores_medico)

        conn.commit()
        print("Medico cadastrado com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar medico:", e)

    finally:
        cursor1.close()
        cursor2.close()
        conn.close()

def adicionar_Prescricao(id_consulta, nome_composto_medicamento, observacao):
    try:
        conn = db.connection()
        cursor = conn.cursor()
        query_usuario = "INSERT INTO prescricao (id_consulta, nome_composto_medicamento, observacao) VALUES (%s, %s, %s, %s);"
        cursor.execute(query_usuario, (id_consulta, nome_composto_medicamento, observacao))

        conn.commit()
        print("Prescricao escrita com sucesso!")

    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao enviar prescricao:", e)

    finally:
        cursor.close()
        conn.close()

def mostrarConsultasPaciente(id_paciente):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
        JOIN HORARIOS H ON M.Id_medico = H.Id_medico
        JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
        JOIN Usuario U ON M.id_medico = U.ID_Usuario
        JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
        WHERE P.Id_paciente = %s
    ''', (id_paciente,))
    tabela_resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return tabela_resultado    

def mostrarConsultasMedico(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT U.Nome, H.Id_horario, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico_consulta = M.Id_medico
        JOIN HORARIOS H ON M.Id_medico = H.Id_medico
        JOIN PACIENTE P ON C.Id_paciente_consulta = P.Id_paciente
        JOIN Usuario U ON P.Id_paciente = U.ID_Usuario
        JOIN DESCRICAO D ON C.Id_consulta = D.Id_consulta
        WHERE M.Id_medico = %s
    ''', (id_medico,))
    tabela_resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return tabela_resultado

def criarHorario(id_medico, horario):
    try:
        conn = db.connection()
        cursor = conn.cursor()
        query_busca = ('INSERT INTO HORARIO(id_medico, horario) VALUE (%s, %s)')
        cursor.execute(query_busca, (id_medico, horario))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao adicionar horÃ¡rio:", e)
    finally:
        cursor.close()
        conn.close()

def mostrarMedicoLog(email, senha):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ('SELECT * FROM MEDICO M INNER JOIN USUARIO U ON M.Id_medico = U.Id_Usuario %s = U.email AND %s = U.senha')
    cursor.execute(query_busca, (email, senha))
    tabela_resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return tabela_resultado

def mostarHorarios(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ('SELECT * FROM HORARIO WHERE id_medico = %s')
    cursor.execute(query_busca, (id_medico,))
    tabela_resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return tabela_resultado

def mostrarConsulta(id_consulta):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ("""
    SELECT c.id, c.data, c.preco, c.nota, um.nome, up.nome, d.descricao FROM consulta c 
    INNER JOIN usuario um ON um.id = c.id_medico
    INNER JOIN medico m ON m.id = um.id
    INNER JOIN usuario up ON up.id = c.id_paciente
    INNER JOIN paciente p ON p.id = up.id
    INNER JOIN descricao d ON d.id_consulta=c.id
    WHERE c.id= %s;
    """)
    cursor.execute(query_busca, (id_consulta,))
    consulta_data = cursor.fetchone()
    if not consulta_data:
        return
    id, data, preco, nota, medico, paciente, descricao = consulta_data
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM prescricao WHERE id_consulta = %s', (id_consulta,))
    prescricoes_data = cursor.fetchall()
    prescricoes = []
    for p in prescricoes_data:
        consulta, medicamento, obs = p
        prescricao = Prescricao(consulta, medicamento, obs)
        prescricoes.append(prescricao)
    consulta = Consulta(id, paciente, medico, data, preco, descricao, nota=nota if nota else 0,prescricoes=prescricoes)
    conn.close()
    return consulta

def mostrarPrescricao(id_consulta):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ('SELECT * FROM PRESCRICAO P WHERE %s = P.Id_consulta')
    cursor.execute(query_busca, (id_consulta,))
    tabela_resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return tabela_resultado

def removerHorario(id_medico, horario):
    try:
        conn = db.connection()
        cursor = conn.cursor()
        query_busca = ('DELETE FROM HORARIO H WHERE %s = H.id_medico AND %s = H.horario')
        cursor.execute(query_busca, (id_medico, horario))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao deletar:", e)
    finally:
        cursor.close()
        conn.close()

def obterClassePaciente(id_paciente):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ('SELECT * FROM USUARIO U INNER JOIN PACIENTE P ON U.Id_usuario = P.Id_paciente AND P.Id_paciente = %s')
    cursor.execute(query_busca, id_paciente)
    id, nome, senha, email, id_prov, plano_de_saude, data_nascimento, necessidade_especial, telefone = cursor.fetchone()
    return Paciente(id, nome, senha, email, plano_de_saude, data_nascimento, necessidade_especial, telefone)

def obterClasseMedico(id_medico):
    medicos = BuscarMedicos()
    for medico in medicos:
        if id_medico == medico.id:
            return medico

def atualizarNotaConsulta(id_consulta, nota):
    conn = db.connection()
    crsr = conn.cursor()
    query_busca = ('UPDATE consulta SET nota = %s WHERE id = %s')
    crsr.execute(query_busca, (nota, id_consulta))
    conn.commit()
    conn.close()

def mostrarConsultasMedico(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, U.Nome, c.data, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico = M.Id
        JOIN PACIENTE P ON C.Id_paciente = P.Id
        JOIN Usuario U ON P.Id = U.ID
        JOIN DESCRICAO D ON C.Id = D.Id_consulta
        WHERE M.id = %s
    ''', (id_medico,))
    result = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('SELECT (u.nome) FROM medico m INNER JOIN usuario u ON u.id=m.id WHERE m.id=%s', (id_medico,))
    medico = cursor.fetchone()[0]
    cursor.close()
    consultas = list()
    for id, paciente, data, descricao, preco in result:
        print(data)
        consulta = Consulta(id, paciente, medico, data, preco, descricao)
        consultas.append(consulta)
    conn.close()
    return consultas

def mostrarConsultasPaciente(id_paciente):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, U.Nome, c.data, D.Descricao, C.Preco 
        FROM CONSULTA C
        JOIN MEDICO M ON C.Id_medico = M.Id
        JOIN PACIENTE P ON C.Id_paciente = P.Id
        JOIN Usuario U ON M.Id = U.ID
        JOIN DESCRICAO D ON C.Id = D.Id_consulta
        WHERE P.id = %s
    ''', (id_paciente,))
    result = cursor.fetchall()
    print(result)
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('SELECT (u.nome) FROM paciente p INNER JOIN usuario u ON u.id=p.id WHERE p.id=%s', (id_paciente,))
    paciente = cursor.fetchone()[0]
    cursor.close()
    consultas = list()
    for id, medico, data, descricao, preco in result:
        print(medico)
        consulta = Consulta(id, paciente, medico, data, preco, descricao)
        consultas.append(consulta)
    conn.close()
    return consultas

def procuraUsuario(email, password):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('SELECT u.id, u.nome, u.email, u.senha, p.plano_de_saude, p.data_de_nascimento, p.necessidade_especial, p.telefone FROM usuario u JOIN paciente p ON u.id = p.id WHERE u.email = %s AND u.senha = %s', (email, password))
    usuario = cursor.fetchone()
    if usuario is None:
        cursor.execute('SELECT u.id, u.nome, u.email, u.senha, m.especializacao, m.avaliacao, m.atende_plantao FROM usuario u JOIN medico m ON u.id = m.id WHERE u.email = %s AND u.senha = %s', (email, password))
        usuario = cursor.fetchone()
        if usuario is None:
            return None
        else:
            id, nome, senha, email, especializacao, avaliacao, atende_plantao = usuario
            return Medico(id, nome, senha, email, especializacao, avaliacao, atende_plantao)
    else:
        id, nome, senha, email, plano_de_saude, data_de_nascimento, necessidade_especial, telefone = usuario
        return Paciente(id, nome, senha, email, plano_de_saude, data_de_nascimento, necessidade_especial, telefone)
