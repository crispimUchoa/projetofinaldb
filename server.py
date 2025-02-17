from flask import Flask, render_template, request, jsonify
import test_data
app = Flask(__name__)

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

@app.route("/paciente/consulta/<int:id_consulta>")
def paciente_consulta(id_consulta):
    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]
    return render_template("paciente/consulta.html", consulta=consulta)

@app.route("/paciente/avaliar_medico/<int:id_medico>", methods=["GET", "POST"])
def avaliar_medico(id_medico):
    medico = next((med for med in test_data.medicos if med.id == id_medico), None)
    if not medico:
        return "Médico não encontrado", 404  # Retorna erro 404 caso o ID não exista
    if request.method == "POST":
        data = request.get_json()  # Recebe a nota do JSON enviado pelo fetch()
        nota = data.get("nota")
        if nota is None or not (1 <= int(nota) <= 5):
            return jsonify({"erro": "Nota inválida"}), 400  # Retorna erro se a nota for inválida
        # Aqui você pode salvar a nota no banco de dados ou atualizar a média do médico
        # Simulação de atualização da média:
        medico.avaliacoes.append(int(nota))
        medico.avaliacao = sum(medico.avaliacoes) / len(medico.avaliacoes)
        return jsonify({"mensagem": "Avaliação registrada com sucesso!", "nova_media": medico.avaliacao})

    # Se for GET, renderiza a página normalmente
    return render_template("paciente/avaliar_medico.html", medico=medico)

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