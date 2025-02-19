from flask import Flask, render_template, request, redirect, url_for, session
import test_data
import queries

from datetime import date
# from queries import conn, AVGMedicoConsultas, BuscarMedicos, cadastrar_paciente, mostrarConsultasMedico, mostrarConsultasPaciente

from routes.paciente import paciente
from routes.medico import medico


app = Flask(__name__)
app.secret_key = "secret_key"

app.register_blueprint(paciente, url_prefix='/paciente')
app.register_blueprint(medico, url_prefix='/medico')

#Rotas de formulário
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email-input']
        password = request.form['password-input']
        user = queries.procuraUsuario(email, password)
        if user.__class__.__name__ == "Medico":
            session['user_id'] = user.id
            return redirect(url_for('medico.home'))
        elif user.__class__.__name__ == "Paciente":
            session['user_id'] = user.id
            return redirect(url_for('paciente.home'))
    return render_template("login.html", role='logout')


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    import services
    
    if request.method == 'POST':
        form = request.form
        nome = form.get('nome')
        email = form.get('email')
        senha = form.get('senha')
        telefone = form.get('telefone')
        confirmacao_senha = form.get('confirmacao_senha')
        plano_de_saude = form.get('plano_de_saude')
        ano, mes, dia = form.get('data_de_nascimento').split('-')
        necessidade_especial = form.get('necessidade_especial')
        
        data_de_nascimento = date(int(ano), int(mes), int(dia))
        if queries.checa_email_paciente(email):
            if senha == confirmacao_senha:
                queries.cadastrar_paciente(nome, email, senha, data_de_nascimento, telefone, plano_de_saude, necessidade_especial)
                return redirect(url_for('login'))
            else: 
                print('SENHAS NAO CONFEREM')
        else:
            print('EMAIL JA CADASTRADO')


    return render_template("cadastro.html", role='logout')

#Rotas do paciente


#

if __name__ == "__main__":
    app.run(debug=True)