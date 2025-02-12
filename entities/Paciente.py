from entities.Usuario import Usuario

class Paciente(Usuario):
    def __init__(self, id, nome, senha, email, plano_de_saude, necessidade_especial, telefone):
        super().__init__(id, nome, senha, email)
        self.plano_de_saude = plano_de_saude
        self.necessidade_especial = necessidade_especial
        self.telefone = telefone