import psycopg2
from db import db
from entities.Medico import Medico
from entities.Horario import Horario
from entities.Paciente import Paciente
from entities.Consulta import Consulta
from entities.Prescricao import Prescricao

from entities.Medicamento import Medicamento



def AVGMedicoConsultas(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    query_avg = ('SELECT m.id AS id_medico, AVG(c.nota) as avaliacao_media FROM medico m INNER JOIN consulta c ON m.id = c.id_medico WHERE m.id=%s GROUP BY m.id HAVING AVG(c.nota) IS NOT NULL; ')
    cursor.execute(query_avg, (id_medico,))
    id, media = cursor.fetchone()
    
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('UPDATE medico SET avaliacao=%s WHERE id=%s', (media, id))
    cursor.close()
    conn.commit()
    conn.close()
     
    
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


def cadastrar_paciente(nome, email, senha, data_nascimento, telefone, plano_de_saude, necessidade_especial):
    try:
        conn = db.connection()
        cursor1 = conn.cursor()
        
        query_usuario = "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s) RETURNING id;"
        cursor1.execute(query_usuario, (nome, email, senha))
        paciente_id = cursor1.fetchone()[0]

        cursor1.close()
        cursor2 = conn.cursor()
        query_paciente = "INSERT INTO paciente (id, data_de_nascimento, telefone, plano_de_saude, necessidade_especial) VALUES (%s, %s, %s, %s, %s);"
        valores_paciente = (paciente_id, data_nascimento,telefone, plano_de_saude, necessidade_especial)
        cursor2.execute(query_paciente, valores_paciente)

        conn.commit()
        print("Paciente cadastrado com sucesso!")
        cursor2.close()
        
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao cadastrar paciente:", e)

    finally:
        # cursor1.close()
        # cursor2.close()
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

def adicionar_Prescricao(id_consulta, prescricao):
    medicamentos, obs = prescricao.values()
    med_values = list()
    for med in medicamentos:
        med_values.append((id_consulta, med, obs))
        
    try:
        conn = db.connection()
        cursor = conn.cursor()
        query_usuario = "INSERT INTO prescricao (id_consulta, composto_medicamento, observacao) VALUES (%s, %s, %s);" 
        print(query_usuario)
        print(med_values)
        cursor.executemany(query_usuario, med_values)

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

def criarHorario(id_medico, horarios):
    try:
        conn = db.connection()
        cursor = conn.cursor()
        print(horarios)
        cursor.execute("DELETE FROM horarios WHERE id_medico=%s", (id_medico,)) 
            
        cursor.close()
        cursor = conn.cursor()
        query_busca = ('INSERT INTO HORARIOS (id_medico, horario) VALUES (%s, %s)')
        cursor.executemany(query_busca, [(id_medico, horario) for horario in horarios])
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
    query_busca = ('SELECT * FROM MEDICO M INNER JOIN USUARIO U ON M.Id = U.Id %s = U.email WHERE %s = U.senha')
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

    LEFT JOIN descricao d ON d.id_consulta=c.id

    WHERE c.id= %s;
    """)
    cursor.execute(query_busca, (id_consulta,))
    consulta_data = cursor.fetchone()

    print('DATA', consulta_data)


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
    query_busca = ('SELECT * FROM USUARIO U INNER JOIN PACIENTE P ON U.Id = P.Id WHERE P.Id = %s')
    cursor.execute(query_busca, (id_paciente,))
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
    query_busca = ('UPDATE consulta SET nota = %s WHERE id = %s RETURNING id_medico')
    crsr.execute(query_busca, (nota, id_consulta))
    id_medico = crsr.fetchone()[0]
    conn.commit()
    conn.close()
    AVGMedicoConsultas(id_medico)

def mostrarConsultasMedico(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id,  up.nome, c.data, d.descricao, c.preco
        FROM consulta c
        INNER JOIN usuario up ON up.id = c.id_paciente
        LEFT JOIN descricao d ON d.id_consulta = c.id
        WHERE EXISTS (
        SELECT 1
        FROM consulta c2
        WHERE c2.id = c.id
        AND c2.id_medico = %s
);
    ''', (id_medico,))
    result = cursor.fetchall()
    print(result)
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('SELECT u.nome FROM medico m INNER JOIN usuario u ON u.id=m.id WHERE m.id=%s', (id_medico,))
    medico = cursor.fetchone()
    cursor.close()
    consultas = list()
    for id, paciente, data, descricao, preco in result:
        consulta = Consulta(id, paciente, medico, data, preco, descricao)
        consultas.append(consulta)

    conn.close()
    return consultas

def obter_medicamentos(q):
    conn = db.connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM medicamento WHERE nome_do_composto ILIKE '%{q}%';" if q else 'SELECT * FROM medicamento'
    cursor.execute(query)
    medicamentos = list()
    for med in cursor.fetchall():
        nome_composto, laboratorio = med
        medicamento = Medicamento(nome_composto, laboratorio)
        medicamentos.append(medicamento)
    return medicamentos

    # cursor.execute('''
    #     SELECT c.id, U.Nome, c.data, D.Descricao, C.Preco 
    #     FROM CONSULTA C
    #     JOIN MEDICO M ON C.Id_medico = M.Id
    #     JOIN PACIENTE P ON C.Id_paciente = P.Id
    #     JOIN Usuario U ON P.Id = U.ID
    #     JOIN DESCRICAO D ON C.Id = D.Id_consulta
    #     WHERE M.id = %s
    # ''', (id_medico,))
    # result = cursor.fetchall()
    # cursor.close()
    # cursor = conn.cursor()
    # cursor.execute('SELECT (u.nome) FROM medico m INNER JOIN usuario u ON u.id=m.id WHERE m.id=%s', (id_medico,))
    # medico = cursor.fetchone()[0]
    # cursor.close()
    # consultas = list()
    # for id, paciente, data, descricao, preco in result:
    #     print(data)
    #     consulta = Consulta(id, paciente, medico, data, preco, descricao)
    #     consultas.append(consulta)
    # conn.close()
    # return consultas

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

def marcaConsulta(id_medico, id_paciente, preco, data, descricao):
    conn = db.connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO consulta (id_medico, id_paciente, preco, data) VALUES (%s, %s, %s, %s) RETURNING id', (id_medico, id_paciente, preco, data))
    id_consulta = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO descricao (id_consulta, descricao) VALUES (%s, %s)', (id_consulta, descricao))
    conn.commit()
    cursor.close()
    conn.close()

def checa_email_paciente(email):
    conn= db.connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM usuario WHERE email=%s', (email,))
    existe = cursor.fetchone()
    print(existe)
    cursor.close()
    conn.close()
    return True if existe is None else False
    