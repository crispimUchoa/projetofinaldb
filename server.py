from flask import Flask, render_template, request, redirect, url_for, session
import test_data
import queries

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
    return render_template("login.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    import services
    
    if request.method == 'POST':
        form = request.form
        user_existe = 'usuario ja existente' if services.checa_email_existe(form['email']) else 'sucesso ao cadastrar e-mail!'
        print(user_existe)
    return render_template("cadastro.html")

#Rotas do paciente


#

if __name__ == "__main__":
    app.run(debug=True)