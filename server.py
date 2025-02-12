from flask import Flask, render_template, request

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
    from entities.Consulta import Consulta

    consultas = [
        Consulta(1, 45, 123, "2025-02-15", 250.50, "Consulta de rotina 1", 4),
        Consulta(2, 78, 123, "2025-02-18", 300.75, "Consulta de check-up", 5),
        Consulta(3, 12, 123, "2025-02-20", 180.00, "Consulta dermatológica", 3),
        Consulta(4, 56, 123, "2025-02-22", 400.00, "Consulta cardiológica", 5),
        Consulta(5, 33, 123, "2025-02-25", 220.30, "Consulta pediátrica", 4),
        Consulta(6, 90, 123, "2025-02-28", 320.00, "Consulta ortopédica", 5),
        Consulta(7, 22, 123, "2025-03-03", 150.90, "Consulta ginecológica", 3),
        Consulta(8, 67, 123, "2025-03-07", 275.60, "Consulta oftalmológica", 4),
        Consulta(9, 39, 123, "2025-03-10", 290.80, "Consulta neurológica", 5),
        Consulta(10, 81, 123, "2025-03-15", 210.50, "Consulta psiquiátrica", 4),
    ]


    return render_template('medico/home.html', consultas=consultas)

@app.route('/medico/consulta/<int:id_consulta>')
def medico_consulta(id_consulta):
    from entities.Consulta import Consulta
    consultas = [
        Consulta(1, 45, 123, "2025-02-15", 250.50, "Consulta de rotina 1", 4),
        Consulta(2, 78, 123, "2025-02-18", 300.75, "Consulta de check-up", 5),
        Consulta(3, 12, 123, "2025-02-20", 180.00, "Consulta dermatológica", 3),
        Consulta(4, 56, 123, "2025-02-22", 400.00, "Consulta cardiológica", 5),
        Consulta(5, 33, 123, "2025-02-25", 220.30, "Consulta pediátrica", 4),
        Consulta(6, 90, 123, "2025-02-28", 320.00, "Consulta ortopédica", 5),
        Consulta(7, 22, 123, "2025-03-03", 150.90, "Consulta ginecológica", 3),
        Consulta(8, 67, 123, "2025-03-07", 275.60, "Consulta oftalmológica", 4),
        Consulta(9, 39, 123, "2025-03-10", 290.80, "Consulta neurológica", 5),
        Consulta(10, 81, 123, "2025-03-15", 210.50, "Consulta psiquiátrica", 4),
    ]
    consulta = list(filter(lambda cons: cons.id == id_consulta, consultas))
    if consulta:
        consulta = consulta[0]
    return render_template('medico/consulta.html', consulta=consulta)
if __name__ == "__main__":
    app.run(debug=True)