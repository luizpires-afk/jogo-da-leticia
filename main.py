# main.py
# Servidor Flask completo e robusto para o jogo da Letícia 💫

from flask import Flask, render_template, request, jsonify, send_from_directory
from ia import IA
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Instância global (estado do jogo para a sessão/singleton)
ia = IA()

# ----------------------------
# Rota principal
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------
# Iniciar jogo
# ----------------------------
@app.route("/iniciar", methods=["POST"])
def iniciar():
    nome = request.form.get("nome", "Jogador").strip()
    if not nome:
        nome = "Jogador"

    # ✅ Corrige: usar 'ia' (não 'ai')
    ia.estado["jogador"] = nome
    ia.estado["nivel"] = 1
    ia.estado["pontos"] = 0
    ia.estado["humor_level"] = 0
    ia.estado["game_over"] = False
    ia.estado["modo_pesadelo"] = False
    ia.estado["acertos_consecutivos"] = 0
    ia.estado["acertos_consecutivos_dificil"] = 0
    ia.perguntas_feitas.clear()

    pergunta = ia.proxima_pergunta()

    # ✅ Garante que a pergunta é texto simples
    if isinstance(pergunta, dict):
        pergunta = (
            pergunta.get("pergunta")
            or pergunta.get("texto")
            or "Pergunta não encontrada"
        )

    return jsonify({
        "mensagem": f"🎮 Boa sorte, {nome}! Vamos começar!",
        "pergunta": pergunta,
        "pontos": ia.estado["pontos"],
        "nivel": ia.estado["nivel"],
        "tempo_restante": ia.estado.get("tempo_restante", 30),
        "dificuldade": ia.dificuldade_por_nivel()
    })

# ----------------------------
# Rota para responder
# ----------------------------
@app.route("/responder", methods=["POST"])
def responder():
    tentativa = request.form.get("tentativa", "")
    resultado = ia.verificar_resposta(tentativa)
    resultado = ia._formatar_resposta(resultado)

    # Garante que sempre venha uma nova pergunta (exceto em fim/pesadelo)
    if (
        resultado.get("nova_pergunta") is None
        and not resultado.get("fim")
        and not resultado.get("modo_pesadelo_opcao")
    ):
        resultado["nova_pergunta"] = ia.proxima_pergunta()
        if isinstance(resultado["nova_pergunta"], dict):
            resultado["nova_pergunta"] = (
                resultado["nova_pergunta"].get("pergunta")
                or resultado["nova_pergunta"].get("texto")
                or "Pergunta não encontrada"
            )

        resultado["tempo_restante"] = ia.estado.get("tempo_restante", 30)
        resultado["pontos"] = ia.estado["pontos"]
        resultado["nivel"] = ia.estado["nivel"]

    # Campos adicionais sempre retornados
    resultado.setdefault("pontos", ia.estado["pontos"])
    resultado.setdefault("nivel", ia.estado["nivel"])
    resultado.setdefault("tempo_restante", ia.estado.get("tempo_restante", 30))
    resultado.setdefault("dificuldade", ia.dificuldade_por_nivel())

    return jsonify(resultado)

# ----------------------------
# Rota para modo pesadelo
# ----------------------------
@app.route("/entrar_pesadelo", methods=["POST"])
def entrar_pesadelo():
    resp = ia.entrar_pesadelo()
    return jsonify(resp)

# ----------------------------
# Rota para confirmar entrada no modo pesadelo (nova)
# ----------------------------
@app.route("/confirmar_pesadelo", methods=["POST"])
def confirmar_pesadelo():
    """
    Ativa o modo PESADELO após o jogador aceitar o desafio.
    """
    if ia.estado.get("modo_pesadelo"):
        return jsonify({"mensagem": "⚠️ Você já está no modo PESADELO!"})

    resp = ia.entrar_pesadelo()
    return jsonify(resp)

# ----------------------------
# Rota de ranking global
# ----------------------------
@app.route("/ranking")
def ranking():
    dados = ia.carregar_ranking()
    lista = sorted(dados.items(), key=lambda x: x[1], reverse=True)
    return jsonify(lista[:10])  # top 10

# ----------------------------
# Rota para arquivos estáticos (caso precise servir JSONs)
# ----------------------------
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# ----------------------------
# Inicialização do servidor
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
