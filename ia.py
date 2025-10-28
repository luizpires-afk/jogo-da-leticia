import random
import json
import os
import time

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
    "jogador": "Jogador",
    "tempo_restante": 60,
    "inicio_tempo": time.time(),
    "modo_pesadelo": False
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

    # Top 10
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:10]
    maior_global = ranking_ordenado[0][1] if ranking_ordenado else 0
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
# CARREGAR BANCO DE PERGUNTAS EXTERNAS
# ----------------------------
def carregar_perguntas_externas():
    arquivos = ["perguntas.json", "perguntas_extra.json", "perguntas.js"]
    perguntas = []

    for arq in arquivos:
        if os.path.exists(arq):
            try:
                with open(arq, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()
                    if arq.endswith(".js"):
                        conteudo = conteudo.replace("window.bancoPerguntas =", "").rstrip(";").strip()
                    dados = json.loads(conteudo)
                    perguntas.extend(dados)
                    print(f"✅ {len(dados)} perguntas carregadas de {arq}")
            except Exception as e:
                print(f"⚠️ Erro ao carregar {arq}: {e}")
        else:
            print(f"❌ Arquivo não encontrado: {arq}")

    if perguntas:
        print(f"📊 Total de perguntas combinadas: {len(perguntas)}")
    else:
        print("⚠️ Nenhum arquivo de perguntas encontrado.")

    return perguntas

PERGUNTAS_EXTERNAS = carregar_perguntas_externas()

# ----------------------------
# BANCO DE PERGUNTAS INTERNO (BACKUP)
# ----------------------------
PERGUNTAS_GERADOR = {
    "matematica": [
        {"pergunta": "Quanto é 3 + 4?", "resposta": ["7", "sete"]},
        {"pergunta": "Resolva: 5 x 6", "resposta": ["30", "trinta"]},
        {"pergunta": "Qual é o resultado de 12 ÷ 3?", "resposta": ["4", "quatro"]},
        {"pergunta": "Quanto é 8 + 7?", "resposta": ["15", "quinze"]},
        {"pergunta": "Resolva: 9 x 9", "resposta": ["81", "oitenta e um"]},
    ],
    "curiosidades": [
        {"pergunta": "Qual é a capital da França?", "resposta": ["paris"]},
        {"pergunta": "Quem pintou a Mona Lisa?", "resposta": ["leonardo da vinci", "da vinci"]},
        {"pergunta": "Qual é o maior mamífero do mundo?", "resposta": ["baleia azul"]},
    ],
    "charadas": [
        {"pergunta": "Quanto mais você tira, mais cresce. O que é?", "resposta": ["buraco"]},
        {"pergunta": "O que é, o que é: tem dentes mas não morde?", "resposta": ["pente"]},
        {"pergunta": "Tem pescoço, mas não tem cabeça. O que é?", "resposta": ["garrafa"]},
    ],
    "sobre_luiz": [
        {"pergunta": "Quem é o professor mais bravo quando erram contas?", "resposta": ["luiz", "professor luiz"]},
        {"pergunta": "Quem dá as dicas e faz piadas enquanto você joga?", "resposta": ["luiz", "professor luiz"]},
    ],
}

# ----------------------------
# GERAR NOVAS PERGUNTAS
# ----------------------------
perguntas_feitas = []

def proxima_pergunta():
    global perguntas_feitas
    if PERGUNTAS_EXTERNAS:
        todas_perguntas = [{"pergunta": p["texto"], "resposta": [p["resposta"]]} for p in PERGUNTAS_EXTERNAS]
    else:
        todas_perguntas = [p for grupo in PERGUNTAS_GERADOR.values() for p in grupo]

    if len(perguntas_feitas) == len(todas_perguntas):
        perguntas_feitas.clear()

    pergunta = random.choice([p for p in todas_perguntas if p not in perguntas_feitas])
    perguntas_feitas.append(pergunta)

    # Ajuste de tempo baseado na dificuldade
    base = 60 if not estado["modo_pesadelo"] else 5
    ganho = 8 if estado["nivel"] < 5 else (5 if estado["nivel"] < 10 else 3)
    estado["tempo_restante"] = max(5, base - (estado["nivel"] * 2) + ganho)
    estado["fase"] = pergunta
    estado["inicio_tempo"] = time.time()

    return pergunta["pergunta"]

# ----------------------------
# HUMOR DO LUIZ
# ----------------------------
def humor_reacao(level: int):
    reacoes = {
        0: ("🤓", random.choice(["Boa! 😎", "Mandou bem!", "Excelente!", "Arrasou!"])),
        1: ("😐", random.choice(["Hmm... quase 😅", "Tenta outra vez!", "Por pouco!", "Falta foco, hein!"])),
        2: ("😠", random.choice(["Tá me testando, né? 😤", "Concentra, vai!", "Não acredito nisso 😡"])),
        3: ("😡", random.choice(["Última chance! 😡", "Mais um erro e eu explodo! 💣", "😬 Controla essa cabeça!"])),
        4: ("💥", "💥 O Luiz explodiu de raiva! Game Over! 💥")
    }
    return reacoes.get(level, ("🤖", "Sem emoções... por enquanto 😏"))

# ----------------------------
# AUXILIARES
# ----------------------------
def definir_jogador(nome):
    estado["jogador"] = nome.strip().capitalize() if nome.strip() else "Jogador"

def atualizar_humor(acertou):
    estado["humor_level"] = max(0, estado["humor_level"] - 1) if acertou else min(4, estado["humor_level"] + 1)

def tempo_restante():
    decorrido = time.time() - estado["inicio_tempo"]
    return max(0, estado["tempo_restante"] - int(decorrido))

def reset_game():
    nome = estado["jogador"]
    global_name, global_score = recorde_global()
    estado.update({
        "nivel": 1,
        "humor_level": 0,
        "tentativas": 0,
        "game_over": False,
        "pontos": 0,
        "modo_pesadelo": False
    })
    nova = proxima_pergunta()
    return f"💥 O Luiz explodiu, mas já se recompôs.<br>Vamos de novo, {nome}? 😅<br>🏆 Recorde global: {global_name} ({global_score} pontos)<br>{nova}"

# ----------------------------
# MECÂNICA PRINCIPAL
# ----------------------------
def verificar_resposta(tentativa):
    tentativa = tentativa.lower().strip()
    nome = estado["jogador"]

    # Palavra-chave especial ❤️
    if tentativa == "te amo":
        estado["pontos"] += 10
        estado["nivel"] += 1
        emoji, fala = random.choice([
            ("😍", "Ah... você sabe como me desarmar 💕"),
            ("😊", "Tá trapaceando, mas eu deixo 😏"),
            ("🥰", "Eu também te amo! ❤️ Bora pra próxima!")
        ])
        return {
            "acertou": True,
            "mensagem": f"{emoji} {fala}<br>🎁 +10 pontos pelo amor!",
            "nova_pergunta": proxima_pergunta(),
            "tempo_restante": estado["tempo_restante"],
            "nivel": estado["nivel"],
            "pontos": estado["pontos"]
        }

    # Tempo esgotado
    if tentativa == "__tempo_esgotado__":
        atualizar_humor(False)
        emoji, fala = humor_reacao(estado["humor_level"])
        return {
            "acertou": False,
            "mensagem": f"{emoji} {fala}<br>⏰ Tempo esgotado, {nome}! 😅",
            "nova_pergunta": proxima_pergunta(),
            "tempo_restante": estado["tempo_restante"],
            "nivel": estado["nivel"],
            "pontos": estado["pontos"]
        }

    # Game over
    if estado["game_over"]:
        return {"reiniciar": True, "nova_pergunta": reset_game(), "mensagem": "💀 Luiz teve um colapso, mas já voltou 😅"}

    resposta_certa = estado["fase"]["resposta"]
    acertou = tentativa in resposta_certa
    atualizar_humor(acertou)

    if acertou:
        estado["pontos"] += 10
        estado["nivel"] += 1
        emoji, fala = humor_reacao(estado["humor_level"])
        atualizar_recorde(nome, estado["pontos"])

        # Modo pesadelo
        if estado["nivel"] >= 20 and not estado["modo_pesadelo"]:
            estado["modo_pesadelo"] = True
            return {
                "modo_pesadelo": True,
                "mensagem": "😈 Você chegou longe... Bem-vindo ao MODO PESADELO! ⏱️",
                "nova_pergunta": proxima_pergunta(),
                "tempo_restante": 5,
                "nivel": estado["nivel"],
                "pontos": estado["pontos"]
            }

        return {
            "acertou": True,
            "mensagem": f"{emoji} {fala}<br>🎯 +10 pontos! 🔥",
            "nova_pergunta": proxima_pergunta(),
            "tempo_restante": estado["tempo_restante"],
            "nivel": estado["nivel"],
            "pontos": estado["pontos"]
        }

    else:
        estado["pontos"] = max(0, estado["pontos"] - 2)
        if estado["modo_pesadelo"]:
            estado["game_over"] = True
            emoji, fala = humor_reacao(4)
            nome_global, pontos_global = recorde_global()
            atualizar_recorde(nome, estado["pontos"])
            return {
                "reiniciar": True,
                "nova_pergunta": reset_game(),
                "mensagem": f"{emoji} {fala}<br>{nome}, errou no modo PESADELO! 💀",
            }

        if estado["humor_level"] >= 4:
            estado["game_over"] = True
            emoji, fala = humor_reacao(4)
            nome_global, pontos_global = recorde_global()
            atualizar_recorde(nome, estado["pontos"])
            return {
                "reiniciar": True,
                "nova_pergunta": reset_game(),
                "mensagem": f"{emoji} {fala}<br>{nome}, você terminou com {estado['pontos']} pontos.<br>🏆 Recorde global: {nome_global} ({pontos_global})",
            }

        emoji, fala = humor_reacao(estado["humor_level"])
        return {
            "acertou": False,
            "mensagem": f"{emoji} {fala}<br>😬 Errou! Foco, {nome}!",
            "nova_pergunta": estado["fase"]["pergunta"],
            "tempo_restante": tempo_restante(),
            "nivel": estado["nivel"],
            "pontos": estado["pontos"]
        }

# Inicializa primeira pergunta
proxima_pergunta()
