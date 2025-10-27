import random
import json
import os

# ----------------------------
# ESTADO GLOBAL DO JOGO
# ----------------------------
estado = {
    "nivel": 1,
    "humor_level": 0,
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

    {"pergunta": "Quanto é 14 + 9?", "resposta": ["23", "vinte e três"]},
    {"pergunta": "Resolva: 8 x 7", "resposta": ["56", "cinquenta e seis"]},
    {"pergunta": "Qual é o resultado de 81 ÷ 9?", "resposta": ["9", "nove"]},
    {"pergunta": "Resolva: 15 - 6", "resposta": ["9", "nove"]},
    {"pergunta": "Quanto é 11 + 14?", "resposta": ["25", "vinte e cinco"]},
    {"pergunta": "Resolva: 3 x 15", "resposta": ["45", "quarenta e cinco"]},
    {"pergunta": "Quanto é 144 ÷ 12?", "resposta": ["12", "doze"]},
    {"pergunta": "Resolva: 25 + 36", "resposta": ["61", "sessenta e um"]},
    {"pergunta": "Quanto é 13 x 3?", "resposta": ["39", "trinta e nove"]},
    {"pergunta": "Resolva: 90 ÷ 5", "resposta": ["18", "dezoito"]},
    {"pergunta": "Quanto é 7²?", "resposta": ["49", "quarenta e nove"]},
    {"pergunta": "Resolva: 10 x 10", "resposta": ["100", "cem"]},
    {"pergunta": "Qual é o dobro de 25?", "resposta": ["50", "cinquenta"]},
    {"pergunta": "Qual é a metade de 80?", "resposta": ["40", "quarenta"]},
    {"pergunta": "Resolva: 5 + 9 + 6", "resposta": ["20", "vinte"]},

    # Perguntas sobre o Luiz 😎
    {"pergunta": "Quem fica bravo quando você erra as contas?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Qual é o nome do professor mais bravo, mas gente boa?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Quem é o mestre dos desafios de matemática?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Qual é o nome do criador desse jogo?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Quem é o mais inteligente da sala? (Dica: começa com L)", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Quem fica feliz quando você acerta uma questão?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Qual é o nome do seu maior rival em matemática?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Quem é o Luiz?", "resposta": ["professor", "meu professor", "professor luiz"]},
    {"pergunta": "Quem te desafia nesse jogo?", "resposta": ["luiz", "professor luiz"]},
    {"pergunta": "Quem está de olho nas suas respostas agora mesmo?", "resposta": ["luiz", "professor luiz", "o luiz"]}
]


# ----------------------------
# HUMOR DO LUIZ
# ----------------------------
def humor_reacao(level: int):
    reacoes = {
        0: ("🤓", random.choice([
            "Essa foi moleza pra você 😏",
            "Tô vendo potencial aí, hein 😎",
            "Boa! Vamos ver se mantém o ritmo 👀"
        ])),
        1: ("😐", random.choice([
            "Hmm... quase, mas ainda não 😅",
            "Tenta outra vez, confio em você!",
            "Errou, mas tá no caminho 😬"
        ])),
        2: ("😠", random.choice([
            "Tá me testando, né? 😤",
            "Não me faz perder a paciência 😡",
            "Você quer me deixar careca? 😤"
        ])),
        3: ("😡", random.choice([
            "Última chance, ein! 😡",
            "Mais um erro e eu surto 😬",
            "Luiz está prestes a explodir 💣"
        ])),
        4: ("💥", "💥 O Luiz explodiu de raiva! Game Over! 💥")
    }
    return reacoes.get(level, ("🤖", "Sem emoções... por enquanto 😏"))

# ----------------------------
# AUXILIARES
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
    nivel = estado["nivel"]
    pergunta = perguntas[(nivel - 1) % len(perguntas)]
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
    return f"💥 O Luiz explodiu, mas já se recompôs.<br>Vamos de novo, {nome}? 😅<br>🏆 Recorde global: {global_name} ({global_score} pontos)<br>{nova}"

def estado_atual():
    return estado

# ----------------------------
# MECÂNICA PRINCIPAL
# ----------------------------
def verificar_resposta(tentativa: str):
    tentativa = tentativa.lower().replace("*", "x").replace("÷", "/").strip()
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

    # ACERTO ✅
    if acertou:
        estado["pontos"] += 10
        estado["nivel"] += 1
        emoji, fala = humor_reacao(estado["humor_level"])
        nova_pergunta = proxima_pergunta()
        novo_pessoal, novo_global, recorde_global_pontos = atualizar_recorde(nome, estado["pontos"])

        if novo_global:
            mensagem_extra = f"🏆 Inacreditável, {nome}! Novo RECORDISTA GLOBAL com {estado['pontos']} pontos! 🎉"
        elif novo_pessoal:
            mensagem_extra = f"👏 Parabéns, {nome}! Você superou seu recorde pessoal! 🔥"
        else:
            mensagem_extra = random.choice([
                f"Luiz: Mandou bem, {nome}! 👏",
                f"Tá ficando esperto, hein {nome}? 😎",
                f"O Luiz até ficou orgulhoso dessa, {nome} 😁"
            ])

        return {
            "acertou": True,
            "mensagem": f"{emoji} {fala}<br>{mensagem_extra}",
            "nova_pergunta": nova_pergunta,
            "nivel": estado["nivel"],
            "humor": estado["humor_level"],
            "pontos": estado["pontos"]
        }

    # ERRO ❌
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
            f"Isso doeu no raciocínio, {nome} 🧠💥"
        ])
        dica = random.choice([
            "💡 Dica: pensa com calma.",
            "💡 Multiplicação não é adivinhação, hein? 😉",
            "💡 Revê a conta, confia no raciocínio!"
        ])

        return {
            "acertou": False,
            "mensagem": f"{emoji} {fala}<br>{sarcasmo}<br>{dica}",
            "nova_pergunta": estado["fase"]["pergunta"],
            "nivel": estado["nivel"],
            "humor": estado["humor_level"],
            "pontos": estado["pontos"]
        }

# Inicializa primeira pergunta
proxima_pergunta()
