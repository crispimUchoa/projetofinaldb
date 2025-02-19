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
    cursor.execute('SELECT (M.Id_medico, U.Nome, M.Especializacao, M.Avaliacao) FROM MEDICO M INNER JOIN Usuario U ON M.ID_Medico = U.ID_Usuario')
    result_medicos = cursor.fetchall()
    medicos = list()
    cursor.close()
    for id, nome, especializacao, avaliacao in result_medicos:
        horarios = []
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM HORARIOS WHERE ID_MEDICO = {id}')
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

def mostarConsulta(id_consulta):
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
    query_busca = ('SELECT * FROM USUARIO U INNER JOIN PACIENTE P ON U.Id_usuario = P.Id_paciente AND P.Id_paciente = %s')
    cursor.execute(query_busca, id_paciente)
    id, nome, senha, email, id_prov, plano_de_saude, data_nascimento, necessidade_especial, telefone = cursor.fetchone()
    return Paciente(id, nome, senha, email, plano_de_saude, data_nascimento, necessidade_especial, telefone)

def obterClasseMedico(id_medico):
    conn = db.connection()
    cursor = conn.cursor()
    query_busca = ('SELECT * FROM USUARIO U INNER JOIN MEDICO M ON U.Id = M.Id WHERE M.Id = %s')
    cursor.execute(query_busca, (id_medico,))
    id, nome, senha, email, id_prov, especializacao, avaliacao, atende_plantao = cursor.fetchone()
    cursor.close()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horarios WHERE id_medico=%s', (id_medico,))
    horarios = []
    for h in cursor.fetchall():
        horario = Horario(id_medico, h[1])
        horarios.append(horario)
    cursor.close()
    return Medico(id, nome, senha, email, especializacao, horarios, avaliacao, atende_plantao)

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