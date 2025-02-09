from Usuario import Usuario

class Medico(Usuario):
    def __init__(self, id, nome, senha, email, especializacao, avaliacao=0, atende_plantao=True):
        super().__init__(id, nome, senha, email)
        self.especializacao = especializacao
        self.avaliacao=avaliacao
        self.atende_plantao=atende_plantao