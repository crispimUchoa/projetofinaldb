from flask import Flask, render_template, request, Blueprint
import test_data
import queries

medico = Blueprint('medico', __name__)

@medico.route('/home')
def home():
    consultas = queries.mostrarConsultasMedico(8)
    print(consultas)
    return render_template('medico/home.html', consultas=consultas)

@medico.route('/consulta/<int:id_consulta>')
def consulta(id_consulta):
    
    consulta = queries.mostarConsulta(id_consulta)
    return render_template('medico/consulta.html', consulta=consulta)

@medico.route('/consulta/<int:id_consulta>/prescricao', methods = ["GET", "POST"])
def criar_prescricao(id_consulta):
    q = request.args.get('q').lower() if request.args.get('q') else ''
    
    medicamentos = queries.obter_medicamentos()

    consulta = queries.mostarConsulta(3)

    if request.method == 'POST':
        from entities.Prescricao import Prescricao
        form = request.form
        prescricao = {'medicamentos': form.getlist('medicamento'), 'obs': form.get('observacao')}
        queries.adicionar_Prescricao(id_consulta, prescricao)
        
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