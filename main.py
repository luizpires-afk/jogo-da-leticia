from flask import Flask, render_template, request, session, redirect, url_for
from ia import gerar_fase, resposta_ia
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "chave-secreta-super-segura"  # troque por uma aleatória depois
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/", methods=["GET", "POST"])
def index():
    # Cria uma sessão se for o primeiro acesso
    if "fase_atual" not in session:
        session["numero_fase"] = 1
        session["fase_atual"] = gerar_fase(session["numero_fase"])
        session["tentativas"] = 0

    fase_atual = session["fase_atual"]
    numero_fase = session["numero_fase"]
    tentativas = session["tentativas"]
    mensagem = ""

    if request.method == "POST":
        tentativa = request.form.get("senha", "").strip()
        session["tentativas"] += 1

        if tentativa == fase_atual["senha"]:
            mensagem = resposta_ia(True)
            session["numero_fase"] += 1
            session["fase_atual"] = gerar_fase(session["numero_fase"])
            session["tentativas"] = 0
        else:
            mensagem = resposta_ia(False, session["tentativas"])

    return render_template(
        "index.html",
        fase=fase_atual,
        mensagem=mensagem,
        tentativas=session["tentativas"],
        numero_fase=session["numero_fase"]
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
