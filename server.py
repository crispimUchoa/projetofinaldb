from flask import Flask, render_template, request
import test_data

from routes import *

app = Flask(__name__)

app.register_blueprint(medico, url_prefix='/medico')

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email-input']
        password = request.form['password-input']
        if email == "1@1" and password == "2":
            return paciente_home()
    return render_template("login.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    import services
    if request.method == 'POST':
        form = request.form
        user_existe = 'usuario ja existente' if services.checa_email_existe(form['email']) else 'sucesso ao cadastrar e-mail!'
        print(user_existe)
    return render_template("cadastro.html")

@app.route("/paciente_home")
def paciente_home():
    return render_template("paciente_home.html")


#

if __name__ == "__main__":
    app.run(debug=True)