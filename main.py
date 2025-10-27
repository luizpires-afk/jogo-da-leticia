from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# ----------------------------
# ESTADO GLOBAL DO JOGO
# ----------------------------
estado = {
    "nivel": 1,
    "humor_level": 0,   # 0 = tranquilo, 4 = explodiu
    "tentativas": 0,
    "game_over": False,
    "pontos": 0,
    "fase": {},
    "jogador": "Jogador"
}

RANKING_FILE = "ranking.json"

# ----------------------------
# FUNÇÕES DE RANKING
# ----------------------------
def carregar_ranking():
    if os.path.exists(RANKING_FILE):
        try:
            with open(RANKING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def salvar_ranking(ranking):
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

def atualizar_recorde(nome, pontos):
    ranking = carregar_ranking()
    recorde_antigo = ranking.get(nome, 0)
    ranking[nome] = max(recorde_antigo, pontos)
    salvar_ranking(ranking)

    maior_global = max(ranking.values(), default=0)
    novo_pessoal = pontos > recorde_antigo
    novo_global = pontos >= maior_global

    return novo_pessoal, novo_global, maior_global

def recorde_global():
    ranking = carregar_ranking()
    if not ranking:
        return "Ninguém ainda", 0
    melhor = max(ranking.items(), key=lambda x: x[1])
    return melhor

# ----------------------------
# BANCO DE PERGUNTAS
# ----------------------------
perguntas = [
    {"pergunta": "Quanto é 3 + 4?", "resposta": ["7", "sete"]},
    {"pergunta": "Resolva: 5 x 6", "resposta": ["30", "trinta"]},
    {"pergunta": "Qual é o resultado de 12 ÷ 3?", "resposta": ["4", "quatro"]},
    {"pergunta": "Resolva: 9 - 5", "resposta": ["4", "quatro"]},
    {"pergunta": "Quanto é 8 + 7?", "resposta": ["15", "quinze"]},
    {"pergunta": "Resolva: 9 x 9", "resposta": ["81", "oitenta e um"]},
    {"pergunta": "Quanto é 100 ÷ 10?", "resposta": ["10", "dez"]},
    {"pergunta": "Resolva: 2 x 12", "resposta": ["24", "vinte e quatro"]},
    {"pergunta": "Quanto é 7 + 8?", "resposta": ["15", "quinze"]},
    {"pergunta": "Resolva: 11 x 11", "resposta": ["121", "cento e vinte e um"]},
]

# ----------------------------
# HUMOR DO LUIZ
# ----------------------------
def humor_reacao(level: int):
    reacoes = {
        0: ("🤓", random.choice([
            "Boa! Essa foi tranquila 😎",
            "Mandou bem! Tá com o raciocínio em dia 💡",
            "Acertou! Luiz tá orgulhoso 👏"
        ])),
        1: ("😐", random.choice([
            "Hmm... quase lá 😅",
            "Errou, mas ainda acredito em você 😬",
            "Essa escapou por pouco 🤏"
        ])),
        2: ("😠", random.choice([
            "Tá me testando, né? 😤",
            "A paciência do Luiz tá no limite 😡",
            "Melhor rever essa conta, hein? 👀"
        ])),
        3: ("😡", random.choice([
            "Última chance, ein! 💣",
            "Mais um erro e eu surto 😬",
            "Luiz tá prestes a explodir 💥"
        ])),
        4: ("💥", "💥 O Luiz explodiu de raiva! Game Over! 💥")
    }
    return reacoes.get(level, ("🤖", "Sem emoções... por enquanto 😏"))

# ----------------------------
# FUNÇÕES AUXILIARES
# ----------------------------
def definir_jogador(nome):
    if nome.strip():
        estado["jogador"] = nome.strip().capitalize()
    else:
        estado["jogador"] = "Jogador"

def atualizar_humor(acertou: bool):
    if acertou:
        estado["humor_level"] = max(0, estado["humor_level"] - 1)
    else:
        estado["humor_level"] = min(4, estado["humor_level"] + 1)

def proxima_pergunta():
    pergunta = random.choice(perguntas)
    estado["fase"] = pergunta
    return pergunta["pergunta"]

def reset_game():
    nome = estado["jogador"]
    global_name, global_score = recorde_global()
    estado.update({
        "nivel": 1,
        "humor_level": 0,
        "tentativas": 0,
        "game_over": False,
        "pontos": 0
    })
    nova = proxima_pergunta()
    return f"💥 O Luiz explodiu, mas já se recompôs. Vamos de novo, {nome}? 😅<br>🏆 Recorde global: {global_name} ({global_score} pontos)<br>{nova}"

# ----------------------------
# MECÂNICA PRINCIPAL
# ----------------------------
def verificar_resposta(tentativa: str):
    tentativa = tentativa.lower().replace("*", "x").strip()
    nome = estado["jogador"]

    if estado["game_over"]:
        nova = reset_game()
        return {
            "reiniciar": True,
            "nova_pergunta": nova,
            "mensagem": f"💀 O Luiz teve um colapso, mas já voltou ao normal, {nome} 😅",
            "nivel": 1,
            "humor": 0
        }

    if not estado["fase"]:
        proxima_pergunta()

    resposta_certa = estado["fase"]["resposta"]
    acertou = tentativa in resposta_certa
    atualizar_humor(acertou)

    # --- ACERTO ---
    if acertou:
        estado["pontos"] += 10
        estado["nivel"] += 1
        emoji, fala = humor_reacao(estado["humor_level"])
        nova_pergunta = proxima_pergunta()

        novo_pessoal, novo_global, recorde_global_pontos = atualizar_recorde(nome, estado["pontos"])
        if novo_global:
            mensagem_extra = f"🏆 Inacreditável, {nome}! Novo RECORDISTA GLOBAL com {estado['pontos']} pontos! 🎉"
        elif novo_pessoal:
            mensagem_extra = f"👏 Parabéns, {nome}! Novo recorde pessoal 🔥"
        else:
            mensagem_extra = random.choice([
                f"Luiz: Boa, {nome}! 👏",
                f"Você tá afiado hoje, {nome}! 😎",
                f"O Luiz até sorriu dessa vez 😁"
            ])

        return {
            "acertou": True,
            "mensagem": f"{emoji} {fala}<br>{mensagem_extra}<br>➡️ Próxima: {nova_pergunta}",
            "nova_pergunta": nova_pergunta,
            "nivel": estado["nivel"],
            "humor": estado["humor_level"],
            "pontos": estado["pontos"]
        }

    # --- ERRO ---
    else:
        estado["pontos"] = max(0, estado["pontos"] - 2)

        if estado["humor_level"] >= 4:
            estado["game_over"] = True
            emoji, fala = humor_reacao(4)
            nome_global, pontos_global = recorde_global()
            atualizar_recorde(nome, estado["pontos"])
            return {
                "reiniciar": True,
                "nova_pergunta": reset_game(),
                "mensagem": f"{emoji} {fala}<br>{nome}, você terminou com {estado['pontos']} pontos.<br>🏆 Recorde global: {nome_global} ({pontos_global} pontos).",
                "nivel": 1,
                "humor": 4,
                "pontos": estado["pontos"]
            }

        emoji, fala = humor_reacao(estado["humor_level"])
        sarcasmo = random.choice([
            f"Luiz: sério isso, {nome}? 😂",
            f"Hmm... {nome}, acho que você dormiu na aula 😅",
            f"Isso doeu no raciocínio, {nome} 🧠💥",
            f"{nome}, tenta mais uma vez antes que eu perca a fé 😑"
        ])
        dica = random.choice([
            "💡 Dica: tenta pensar com calma.",
            "💡 Multiplicação não é adivinhação 😉",
            "💡 Revê a conta, confia no raciocínio!",
            "💡 Pode usar os dedos, eu não julgo 😏",
            "💡 O Luiz ainda acredita em você 😬"
        ])

        return {
            "acertou": False,
            "mensagem": f"{emoji} {fala}<br>{sarcasmo}<br>{dica}",
            "nova_pergunta": estado["fase"]["pergunta"],
            "nivel": estado["nivel"],
            "humor": estado["humor_level"],
            "pontos": estado["pontos"]
        }

# ----------------------------
# ROTAS FLASK
# ----------------------------
@app.route("/")
def index():
    pergunta = proxima_pergunta()
    return render_template("index.html", pergunta=pergunta)

@app.route("/definir_jogador", methods=["POST"])
def definir_nome():
    nome = request.json.get("nome", "Jogador")
    definir_jogador(nome)
    return jsonify({"status": "ok", "nome": nome})

@app.route("/verificar", methods=["POST"])
def verificar():
    tentativa = request.json.get("tentativa", "")
    resposta = verificar_resposta(tentativa)
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True)
