from flask import Flask, render_template, request
import test_data
app = Flask(__name__)
app.secret_key = "secret key"

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
                return medico_home()
            elif user_type == "paciente":
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

#Rotas do paciente
@app.route("/paciente_home", methods=['GET', 'POST'])
def paciente_home():
    return render_template("/paciente/home.html", consultas=test_data.consultas)

@app.route("/paciente/consulta")
def paciente_consulta():
    return render_template("paciente/consulta.html")

#Rotas do medico
@app.route('/medico/home')
def medico_home():

    return render_template('medico/home.html', consultas=test_data.consultas)

@app.route('/medico/consulta/<int:id_consulta>')
def medico_consulta(id_consulta):
    
    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]
    return render_template('medico/consulta.html', consulta=consulta)

@app.route('/medico/consulta/<int:id_consulta>/prescricao', methods = ["GET", "POST"])
def criar_prescricao(id_consulta):
    q = request.args.get('q').lower() if request.args.get('q') else ''
    
    medicamentos = filter(lambda med: q in med.nome_do_composto.lower() ,test_data.medicamentos)

    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]

    if request.method == 'POST':
        from entities.Prescricao import Prescricao
        print(request.form)
        
    return render_template('medico/prescricao.html', consulta=consulta, medicamentos=medicamentos)

if __name__ == "__main__":
    app.run(debug=True)