from flask import Flask, render_template, request, Blueprint, session
import test_data
import queries
import datetime

paciente = Blueprint('paciente', __name__)

@paciente.route("/home", methods=['GET', 'POST'])
def home():
    user_id = session['user_id']
    consultas = queries.mostrarConsultasPaciente(user_id)
    return render_template("/paciente/home.html", consultas=consultas, role='pac')

@paciente.route("/consulta/<int:id_consulta>")
def consulta(id_consulta):
    consulta = queries.mostrarConsulta(id_consulta)
    return render_template("paciente/consulta.html", consulta=consulta, role='pac')

@paciente.route("/avaliar_consulta/<int:id_consulta>", methods=["GET", "POST"])
def avaliar_consulta(id_consulta):
    consulta = queries.mostrarConsulta(id_consulta)
    if request.method == "POST":
        nota = request.form['rating']
        queries.atualizarNotaConsulta(id_consulta, nota)
        
    return render_template("paciente/avaliar_consulta.html", consulta=consulta, role='pac')

@paciente.route('/lista_medicos')
def lista_medicos():
    medicos = queries.BuscarMedicos()
    return render_template("paciente/lista_medicos.html", medicos=medicos, role='pac')

@paciente.route('/marcar_consulta/<int:id_medico>', methods=['POST', 'GET'])
def marcar_consulta(id_medico):
    user_id = session['user_id']
    paciente = queries.obterClassePaciente(user_id)
    if request.method == 'POST':
        data_hora = request.form['marcar-consulta-date']
        descricao = request.form['descricao-consulta']
        data, horario = data_hora.split("T")
        ano, mes, dia = data.split('-')
        hora, minuto = horario.split(":")
        new_date_time = datetime.datetime(int(ano), int(mes), int(dia), int(hora), int(minuto))
        queries.marcaConsulta(id_medico, int(user_id), 100, new_date_time, descricao)
    medico = queries.obterClasseMedico(id_medico)
    consultas = queries.mostrarConsultasMedico(id_medico)
    return render_template("paciente/marcar_consulta.html", medico=medico, consultas=consultas, role='pac')