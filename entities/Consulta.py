
class Consulta:
    def __init__(self, id, paciente, medico, data, preco, descricoes, nota=0, prescricoes = []):
        self.id = id
        self.paciente = paciente
        self.medico = medico
        self.data = data
        self.preco = preco
        self.descricoes = descricoes
        self.nota = nota
        self.prescricoes = prescricoes