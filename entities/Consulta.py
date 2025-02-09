from Medico import Medico
from Usuario import Usuario

class Consulta:
    def __init__(self, id, paciente, medico, data, preco, nota=0):
        self.id = id
        self.paciente = paciente
        self.medico = medico
        self.data = data
        self.preco = preco
        self.nota = nota