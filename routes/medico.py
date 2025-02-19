from flask import Flask, render_template, request, Blueprint, redirect, url_for, session
import test_data
import queries

medico = Blueprint('medico', __name__)

@medico.route('/home')
def home():
    user_id = session['user_id']
    consultas = queries.mostrarConsultasMedico(user_id)   
    print(consultas)
    return render_template('medico/home.html', consultas=consultas, role='med')

@medico.route('/consulta/<int:id_consulta>')
def consulta(id_consulta):
    
    consulta = queries.mostrarConsulta(id_consulta)
    return render_template('medico/consulta.html', consulta=consulta, role='med')

@medico.route('/consulta/<int:id_consulta>/prescricao', methods = ["GET", "POST"])
def criar_prescricao(id_consulta):
    q = request.args.get('q').lower() if request.args.get('q') else ''
    
    medicamentos = queries.obter_medicamentos(q)

    consulta = queries.mostrarConsulta(id_consulta)

    if request.method == 'POST':
        from entities.Prescricao import Prescricao
        form = request.form
        prescricao = {'medicamentos': form.getlist('medicamento'), 'obs': form.get('observacao')}
        queries.adicionar_Prescricao(id_consulta, prescricao)
        
    return render_template('medico/prescricao.html', consulta=consulta, medicamentos=medicamentos, role='med')

@medico.route('/perfil')
def perfil():
    user_id = session['user_id']
    medico = queries.obterClasseMedico(user_id)
    return render_template('medico/perfil.html', medico=medico, role='med')

@medico.route('/alterar_horarios', methods=['GET', 'POST'])
def alterar_horarios():
    user_id = session['user_id']
    medico = queries.obterClasseMedico(user_id)
    medico_horarios = [h.horario for h in medico.horarios]
    todos_horarios = []
    for h in range(6, 18):
        todos_horarios.append(f'{str(h).zfill(2)}:00')
        todos_horarios.append(f'{str(h).zfill(2)}:30')


    if request.method=='POST':
        horarios = request.form.getlist('alterar_horarios')
        queries.criarHorario(7, horarios)
        return redirect(url_for('medico.alterar_horarios'))

    return render_template('medico/alterar_horarios.html', medico=medico,medico_horarios=medico_horarios, todos_horarios=todos_horarios, role='med')