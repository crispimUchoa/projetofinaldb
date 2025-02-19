from flask import Flask, render_template, request, Blueprint, session
import test_data
import queries


paciente = Blueprint('paciente', __name__)

@paciente.route("/home", methods=['GET', 'POST'])
def home():
    user_id = session['user_id']
    consultas = queries.mostrarConsultasPaciente(user_id)
    return render_template("/paciente/home.html", consultas=consultas)

@paciente.route("/consulta/<int:id_consulta>")
def consulta(id_consulta):
    consulta = queries.mostrarConsulta(id_consulta)
    return render_template("paciente/consulta.html", consulta=consulta)

@paciente.route("/avaliar_consulta/<int:id_consulta>", methods=["GET", "POST"])
def avaliar_consulta(id_consulta):
    consulta = queries.mostrarConsulta(id_consulta)
    if request.method == "POST":
        nota = request.form['rating']
        queries.atualizarNotaConsulta(id_consulta, nota)
        
    return render_template("paciente/avaliar_consulta.html", consulta=consulta)

@paciente.route('/lista_medicos')
def lista_medicos():
    medicos = queries.BuscarMedicos()
    return render_template("paciente/lista_medicos.html", medicos=medicos)

@paciente.route('/marcar_consulta/<int:id_medico>')
def marcar_consulta(id_medico):
    medico = queries.obterClasseMedico(id_medico)
    return render_template("paciente/marcar_consulta.html", medico=medico)