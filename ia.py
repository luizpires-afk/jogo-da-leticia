import random
import operator
import re

fase_atual = {}
nivel = 1
acertos_seguidos = 0

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "//": operator.floordiv
}

EMOJIS_CORES = {
    "vermelho": ["❤️", "🟥", "🍎", "🌹", "🚗", "🔥", "🎈", "📕", "🍓"],
    "azul": ["💙", "🟦", "🐳", "🧢", "🌊", "💧", "🪣", "🫐"],
    "verde": ["💚", "🟩", "🍀", "🌳", "🥦", "🐢", "🦎", "🍏"],
    "amarelo": ["💛", "🟨", "🍋", "🐥", "🌻", "🌞", "⚡", "🧀"],
    "roxo": ["💜", "🟪", "🍇", "🔮", "🪻", "👾"],
    "laranja": ["🧡", "🟧", "🍊", "🦊", "🥕"],
    "preto": ["🖤", "⬛", "🐈‍⬛", "🎩", "🕶️"],
    "branco": ["🤍", "⬜", "🐑", "🥛", "❄️"]
}

CHARADAS_FACEIS = [
    ("Tem dentes, mas não morde. O que é?", "pente"),
    ("O que tem pescoço, mas não tem cabeça?", "garrafa"),
    ("Quanto é 7 - 7?", "0"),
    ("O que cai em pé e corre deitado?", "chuva"),
    ("Quanto é 2 + 3?", "5"),
    ("O que passa na frente do sol, mas não faz sombra?", "vento"),
]

# --- Funções auxiliares robustas --- #

def clean_int_string(s):
    """Limpa e converte uma string em inteiro, ignorando espaços e variações de traço."""
    if not s:
        return None
    s = s.strip()
    s = re.sub(r"[–—−]", "-", s)  # substitui travessões por hífen normal
    s = re.sub(r"\s+", "", s)  # remove TODOS os espaços
    try:
        return int(s)
    except ValueError:
        return None


import re

def normalize_text(s: str) -> str:
    """Remove espaços, pontuações e deixa tudo minúsculo."""
    # Remove espaços e pontuações (versão compatível com o re padrão)
    s = re.sub(r"[\s\W_]+", "", s.lower())  # \W remove tudo que não é letra ou número
    return s



# --- Geração de perguntas --- #

def gerar_conta_inteira(nivel):
    """Gera uma conta simples de inteiros com resultado inteiro."""
    if nivel <= 2:
        op = random.choice(["+", "-"])
        a, b = random.randint(0, 9), random.randint(0, 9)
    elif nivel == 3:
        op = random.choice(["+", "-", "*"])
        a, b = random.randint(-10, 10), random.randint(1, 10)
    else:
        op = random.choice(["+", "-", "*", "//"])
        if op == "//":
            b = random.randint(1, 10)
            a = b * random.randint(-10, 10)
        else:
            a = random.randint(-30, 30)
            b = random.randint(-20, 20)

    resultado = OPS[op](a, b)
    return {"pergunta": f"Quanto é {a} {op} {b}?", "resposta": str(resultado), "tipo": "conta"}


def gerar_pergunta_cor():
    cor = random.choice(list(EMOJIS_CORES.keys()))
    emoji = random.choice(EMOJIS_CORES[cor])
    return {"pergunta": f"Qual é a cor deste emoji? {emoji}", "resposta": cor, "tipo": "cor"}


def gerar_charada(nivel):
    pergunta, resposta = random.choice(CHARADAS_FACEIS)
    return {"pergunta": pergunta, "resposta": resposta, "tipo": "charada"}


# --- Fluxo do jogo --- #

def proxima_pergunta():
    global fase_atual, nivel
    if nivel <= 2:
        tipo = "conta"
    elif nivel == 3:
        tipo = random.choice(["conta", "cor"])
    else:
        tipo = random.choice(["conta", "cor", "charada"])

    if tipo == "conta":
        fase_atual = gerar_conta_inteira(nivel)
    elif tipo == "cor":
        fase_atual = gerar_pergunta_cor()
    else:
        fase_atual = gerar_charada(nivel)

    return fase_atual["pergunta"]


def verificar_resposta(tentativa):
    global fase_atual, nivel, acertos_seguidos

    tentativa_int = clean_int_string(tentativa)
    resposta_int = clean_int_string(fase_atual.get("resposta", ""))

    tentativa_norm = normalize_text(tentativa)
    resposta_norm = normalize_text(fase_atual.get("resposta", ""))

    acertou = False

    # --- Comparação numérica segura ---
    if tentativa_int is not None and resposta_int is not None:
        acertou = tentativa_int == resposta_int
    else:
        acertou = tentativa_norm == resposta_norm

    if acertou:
        acertos_seguidos += 1
        if acertos_seguidos % 3 == 0:
            nivel = min(nivel + 1, 5)
        msg = random.choice([
            "✅ Acertou! Luiz está orgulhoso! 😎",
            "🎯 Boa! Subindo o nível!",
            "👏 Mandou bem! Luiz curtiu!"
        ])
        return True, msg

    acertos_seguidos = 0
    nivel = max(1, nivel - 0.2)

    dica = {
        "conta": "Revise o cálculo — lembre-se: espaços e sinais negativos contam! 😉",
        "cor": "Olhe o emoji com calma e veja a cor principal 🌈",
        "charada": "Pense fora da caixa! Luiz adora enigmas 🤓"
    }.get(fase_atual.get("tipo"), "")

    msg = random.choice([
        f"❌ Errou! {dica}",
        f"😅 Quase lá... {dica}",
        f"❌ Não foi dessa vez. {dica}"
    ])
    return False, msg
