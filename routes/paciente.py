from flask import Flask, render_template, request, Blueprint, session
import test_data
import queries

<<<<<<< HEAD
=======

>>>>>>> hchuvas

paciente = Blueprint('paciente', __name__)

@paciente.route("/home", methods=['GET', 'POST'])
def home():
    user_id = session['user_id']
    consultas = queries.mostrarConsultasPaciente(user_id)
    return render_template("/paciente/home.html", consultas=consultas)

@paciente.route("/consulta/<int:id_consulta>")
def consulta(id_consulta):
    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]
    return render_template("paciente/consulta.html", consulta=consulta)

@paciente.route("/avaliar_consulta/<int:id_consulta>", methods=["GET", "POST"])
def avaliar_consulta(id_consulta):
    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]
    if request.method == "POST":
        nota = request.form['rating']
        queries.atualizarNotaConsulta(id_consulta, nota)
<<<<<<< HEAD
        
=======
>>>>>>> hchuvas
    return render_template("paciente/avaliar_consulta.html", consulta=consulta)

@paciente.route('/lista_medicos')
def lista_medicos():
    return render_template("paciente/lista_medicos.html", medicos=test_data.medicos)

@paciente.route('/marcar_consulta/<int:id_medico>')
def marcar_consulta(id_medico):
    medico = list(filter(lambda cons: cons.id == id_medico, test_data.medicos))
    if medico:
        medico = medico[0]
    return render_template("paciente/marcar_consulta.html", medico=medico)