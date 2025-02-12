
class Consulta:
    def __init__(self, id, id_paciente, id_medico, data, preco, descricoes, nota=0):
        self.id = id
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.data = data
        self.preco = preco
        self.descricoes = descricoes
        self.nota = nota