from flask import Flask, render_template, request, jsonify, redirect, url_for
import test_data

# from queries import conn, AVGMedicoConsultas, BuscarMedicos, cadastrar_paciente, mostrarConsultasMedico, mostrarConsultasPaciente

from routes.paciente import paciente
from routes.medico import medico


app = Flask(__name__)

app.register_blueprint(paciente, url_prefix='/paciente')
app.register_blueprint(medico, url_prefix='/medico')

#Rotas de formulário
@app.route("/", methods=['GET', 'POST'])
def login():
    import services
    if request.method == 'POST':
        email = request.form['email-input']
        password = request.form['password-input']
        user_type = services.checa_usuario(email, password)
        if user_type:
            if user_type == "medico":
                return redirect(url_for('medico.home'))
            elif user_type == "paciente":
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