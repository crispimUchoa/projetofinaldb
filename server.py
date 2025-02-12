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

if __name__ == "__main__":
    app.run(debug=True)