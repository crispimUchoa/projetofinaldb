import test_data

def checa_email_existe(email):
    user = list(filter(lambda user: user.email == email ,test_data.users))
    if user:
        return True
    return False


def compara_senhas(senha, confirmacao):
    if senha == confirmacao:
        return True
    return False

def checa_usuario(email, senha):
    for user in test_data.users:
        if user.email == email and user.senha == senha:
           if user.__class__.__name__ == "Medico":
               return "medico"
           if user.__class__.__name__ == "Paciente":
               return "paciente"
    return None
