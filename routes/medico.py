from flask import Flask, render_template, request, Blueprint
import test_data

medico = Blueprint('medico', __name__)

@medico.route('/home')
def home():
    return render_template('medico/home.html', consultas=test_data.consultas)



@medico.route('/consulta/<int:id_consulta>')
def consulta(id_consulta):
    
    consulta = list(filter(lambda cons: cons.id == id_consulta, test_data.consultas))
    if consulta:
        consulta = consulta[0]
    return render_template('medico/consulta.html', consulta=consulta)

#Rot
@medico.route('/consulta/<int:id_consulta>/prescricao', methods = ["GET", "POST"])
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

@medico.route('/perfil')
def perfil():
    medico = test_data.medicos[0]
    return render_template('medico/perfil.html', medico=medico)

@medico.route('/alterar_horarios', methods=['GET', 'POST'])
def alterar_horarios():
    medico = test_data.medicos[0]
    todos_horarios = [f'{str(n).zfill(2)}:00-{str(n+4).zfill(2)}:00' for n in range(8, 18)]

    if request.method=='POST':
        print(request.form)

    return render_template('medico/alterar_horarios.html', medico=medico, todos_horarios=todos_horarios)