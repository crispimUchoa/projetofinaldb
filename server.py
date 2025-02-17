from flask import Flask, render_template, request
import test_data
app = Flask(__name__)

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

#Rot
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

@app.route('/medico/perfil')
def medico_perfil():
    medico = test_data.medicos[0]
    return render_template('medico/perfil.html', medico=medico)

@app.route('/medico/alterar_horarios', methods=['GET', 'POST'])
def alterar_horarios():
    medico = test_data.medicos[0]
    todos_horarios = [f'{str(n).zfill(2)}:00-{str(n+4).zfill(2)}:00' for n in range(8, 18)]

    if request.method=='POST':
        print(request.form)

    return render_template('medico/alterar_horarios.html', medico=medico, todos_horarios=todos_horarios)

if __name__ == "__main__":
    app.run(debug=True)