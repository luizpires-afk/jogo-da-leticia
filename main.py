from flask import Flask, render_template, request, jsonify
import random, string, time

app = Flask(__name__)

# ---------- BANCO DE DADOS SIMPLES (em memória) ----------
ranking = []  # [(nome, pontuacao, tag)]

# ---------- PERGUNTAS ----------
perguntas = {
    "facil": [
        {"pergunta": "Quanto é 2 + 2?", "resposta": "4"},
        {"pergunta": "Qual é o primeiro planeta do sistema solar?", "resposta": "Mercúrio"},
        {"pergunta": "Qual a cor do céu em um dia ensolarado?", "resposta": "azul"},
        {"pergunta": "Quanto é 10 - 7?", "resposta": "3"},
        {"pergunta": "Qual animal é conhecido como o rei da selva?", "resposta": "leão"}
    ],
    "medio": [
        {"pergunta": "Quanto é 12 x 3?", "resposta": "36"},
        {"pergunta": "Qual é o maior oceano do mundo?", "resposta": "Pacífico"},
        {"pergunta": "Quem pintou a Mona Lisa?", "resposta": "Leonardo da Vinci"},
        {"pergunta": "Quanto é 15 ÷ 3?", "resposta": "5"},
        {"pergunta": "Em que continente fica o Egito?", "resposta": "África"}
    ],
    "dificil": [
        {"pergunta": "Quanto é 25 x 4 - 10?", "resposta": "90"},
        {"pergunta": "Quem escreveu Dom Casmurro?", "resposta": "Machado de Assis"},
        {"pergunta": "Qual é o elemento químico representado por 'Au'?", "resposta": "Ouro"},
        {"pergunta": "Quantos ossos tem o corpo humano adulto?", "resposta": "206"},
        {"pergunta": "Qual é o país com maior população do mundo?", "resposta": "China"}
    ],
    "pesadelo": [
        {"pergunta": "Raiz quadrada de 529?", "resposta": "23"},
        {"pergunta": "Qual o 7º planeta do sistema solar?", "resposta": "Urano"},
        {"pergunta": "Quem descobriu o elétron?", "resposta": "Thomson"},
        {"pergunta": "Qual o maior deserto do mundo?", "resposta": "Antártico"},
        {"pergunta": "Quanto é 72 ÷ 9 + 8 x 2?", "resposta": "22"}
    ]
}

# ---------- VARIÁVEIS DE ESTADO ----------
estado = {
    "pontuacao": 0,
    "dificuldade": "facil",
    "tempo": 30,
    "perguntas_feitas": set(),
    "modo_pesadelo": False,
    "nome": "",
}

# ---------- FUNÇÕES AUXILIARES ----------
def gerar_tag(nome):
    sufixo = ''.join(random.choices(string.digits, k=4))
    return f"{nome}#{sufixo}"

def proxima_pergunta():
    nivel = estado["dificuldade"]
    disponiveis = [p for i, p in enumerate(perguntas[nivel]) if i not in estado["perguntas_feitas"]]
    if not disponiveis:
        estado["perguntas_feitas"] = set()
        disponiveis = perguntas[nivel]
    pergunta = random.choice(disponiveis)
    estado["perguntas_feitas"].add(perguntas[nivel].index(pergunta))
    return pergunta

def ajustar_tempo(acertou):
    if estado["modo_pesadelo"]:
        estado["tempo"] = 5
    else:
        if acertou:
            if estado["dificuldade"] == "facil":
                estado["tempo"] += 8
            elif estado["dificuldade"] == "medio":
                estado["tempo"] += 5
            elif estado["dificuldade"] == "dificil":
                estado["tempo"] += 3
        else:
            estado["tempo"] -= 5
            if estado["tempo"] < 5:
                estado["tempo"] = 5

def proxima_dificuldade():
    if estado["pontuacao"] >= 5 and estado["dificuldade"] == "facil":
        estado["dificuldade"] = "medio"
        estado["tempo"] = 25
    elif estado["pontuacao"] >= 10 and estado["dificuldade"] == "medio":
        estado["dificuldade"] = "dificil"
        estado["tempo"] = 20
    elif estado["pontuacao"] >= 10 and estado["dificuldade"] == "dificil":
        return "modo_pesadelo"
    return None

def expressao_luiz(acertou, tempo):
    if acertou:
        if tempo > 20:
            return "😁 Uau, acertou rápido! Boa!"
        elif tempo > 10:
            return "😎 Mandou bem, amor!"
        else:
            return "😉 Foi por pouco, mas valeu!"
    else:
        if tempo > 15:
            return "😠 Poxa, tenta de novo!"
        elif tempo > 7:
            return "😡 Assim não dá, hein!"
        else:
            return "💀 Luiz está furioso!"

# ---------- ROTAS ----------
@app.route("/")
def index():
    pergunta = proxima_pergunta()
    return render_template("index.html", pergunta=pergunta["pergunta"], tempo=estado["tempo"], dificuldade=estado["dificuldade"])

@app.route("/responder", methods=["POST"])
def responder():
    dados = request.get_json()
    resposta = dados.get("resposta", "").strip().lower()
    pergunta_atual = dados.get("pergunta_atual")
    acertou = False
    comentario = ""

    if resposta == "te amo":
        acertou = True
        comentario = "💖 Aw... Te amo também! Pode passar, vai. 😍"
    else:
        for p in perguntas[estado["dificuldade"]]:
            if p["pergunta"] == pergunta_atual:
                if resposta.lower() == p["resposta"].lower():
                    acertou = True
                break

    if acertou:
        estado["pontuacao"] += 1
        ajustar_tempo(True)
        comentario = comentario or expressao_luiz(True, estado["tempo"])
        proximo = proxima_dificuldade()
        if proximo == "modo_pesadelo":
            return jsonify({"status": "transicao", "mensagem": "🔥 Chegou até aqui?! Quer entrar no modo PESADELO ou encerrar com orgulho?", "pontuacao": estado["pontuacao"]})
    else:
        ajustar_tempo(False)
        comentario = expressao_luiz(False, estado["tempo"])
        if estado["modo_pesadelo"] and not acertou:
            return jsonify({"status": "fim", "mensagem": "💀 Luiz explodiu de raiva! Fim de jogo.", "pontuacao": estado["pontuacao"]})

    if estado["tempo"] <= 0:
        return jsonify({"status": "fim", "mensagem": "💥 Tempo esgotado! Luiz perdeu a paciência!", "pontuacao": estado["pontuacao"]})

    prox = proxima_pergunta()
    return jsonify({"status": "ok", "pergunta": prox["pergunta"], "tempo": estado["tempo"], "comentario": comentario, "dificuldade": estado["dificuldade"], "pontuacao": estado["pontuacao"]})

@app.route("/modo_pesadelo", methods=["POST"])
def modo_pesadelo():
    estado["modo_pesadelo"] = True
    estado["dificuldade"] = "pesadelo"
    estado["tempo"] = 5
    return jsonify({"status": "ok", "mensagem": "😈 Bem-vindo ao modo PESADELO! Boa sorte!"})

@app.route("/salvar_ranking", methods=["POST"])
def salvar_ranking():
    dados = request.get_json()
    nome = dados.get("nome", "Jogador")
    pontuacao = dados.get("pontuacao", 0)
    tag = gerar_tag(nome)
    ranking.append((nome, pontuacao, tag))
    ranking.sort(key=lambda x: x[1], reverse=True)
    top10 = ranking[:10]
    return jsonify({"status": "ok", "ranking": top10})

if __name__ == "__main__":
    app.run(debug=True)
