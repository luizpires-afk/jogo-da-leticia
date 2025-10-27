from flask import Flask, render_template, request, jsonify
import ia  # importa o arquivo ia.py

app = Flask(__name__)

# Inicializa a primeira pergunta
ia.proxima_pergunta()

@app.route("/")
def index():
    return render_template("index.html", pergunta=ia.fase_atual["pergunta"])

@app.route("/verificar", methods=["POST"])
def verificar():
    data = request.get_json()
    tentativa = data.get("tentativa", "").strip()

    acertou, mensagem = ia.verificar_resposta(tentativa)

    if acertou:
        nova_pergunta = ia.proxima_pergunta()
        return jsonify({
            "acertou": True,
            "mensagem": mensagem,
            "nova_pergunta": nova_pergunta
        })
    else:
        return jsonify({
            "acertou": False,
            "mensagem": mensagem,
            "nova_pergunta": ia.fase_atual["pergunta"]
        })

if __name__ == "__main__":
    app.run(debug=True)
