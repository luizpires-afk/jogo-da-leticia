from flask import Flask, render_template, request, jsonify
import ia

app = Flask(__name__)
fase_atual = ia.gerar_fase()
tentativas = 0
nivel = 1

@app.route("/")
def index():
    return render_template("index.html", pergunta=fase_atual["pergunta"])

@app.route("/responder", methods=["POST"])
def responder():
    global fase_atual, tentativas, nivel
    data = request.get_json()
    tentativa = data.get("resposta", "")
    tentativas += 1

    acertou, mensagem, _ = ia.avaliar_tentativa(fase_atual, tentativa, tentativas)
    if acertou:
        nivel += 1
        fase_atual = ia.gerar_fase()
        tentativas = 0
        return jsonify({
            "acertou": True,
            "mensagem": mensagem,
            "nova_pergunta": fase_atual["pergunta"],
            "nivel": nivel
        })
    return jsonify({
        "acertou": False,
        "mensagem": mensagem,
        "nova_pergunta": fase_atual["pergunta"],
        "nivel": nivel
    })

if __name__ == "__main__":
    app.run(debug=True)
