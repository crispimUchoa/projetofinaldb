from flask import Flask, render_template, request
from test_data import consultas
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email-input']
        password = request.form['password-input']
        if email == "1@1" and password == "2":
            return paciente_home()
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/paciente_home")
def paciente_home():
    return render_template("paciente_home.html")


#Rotas do medico
@app.route('/medico/home')
def medico_home():

    return render_template('medico/home.html', consultas=consultas)

@app.route('/medico/consulta/<int:id_consulta>')
def medico_consulta(id_consulta):
    
    consulta = list(filter(lambda cons: cons.id == id_consulta, consultas))
    if consulta:
        consulta = consulta[0]
    return render_template('medico/consulta.html', consulta=consulta)
if __name__ == "__main__":
    app.run(debug=True)