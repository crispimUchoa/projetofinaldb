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