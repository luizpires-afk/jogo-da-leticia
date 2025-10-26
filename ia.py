import random
import math

# 🎨 Emojis coloridos por cor
CORES_EMOJIS = {
    "vermelho": ["❤️", "🟥", "🍎", "🌹", "🍓", "🎈", "🚗", "📕", "🧣"],
    "verde": ["💚", "🟩", "🍀", "🌲", "🥦", "🐸", "🧤"],
    "azul": ["💙", "🟦", "🌊", "🐳", "🧢", "🎽"],
    "amarelo": ["💛", "🟨", "🌞", "🌻", "⭐", "🍋"],
    "preto": ["🖤", "⬛", "🐈‍⬛", "🎩", "🕶️"],
    "branco": ["🤍", "⬜", "🐑", "❄️"],
    "roxo": ["💜", "🟪", "🍇", "🔮"],
    "laranja": ["🟧", "🍊", "🦊", "🏀"],
    "rosa": ["🌸", "🎀", "🩷", "🍑"],
    "marrom": ["🟫", "🐻", "🥔", "🍫"],
}

# 🎲 Charadas e enigmas
CHARADAS = [
    {"pergunta": "O que é o que é: quanto mais se tira, maior fica?", "resposta": "buraco"},
    {"pergunta": "Tem dentes, mas não morde. O que é?", "resposta": "pente"},
    {"pergunta": "Quanto mais cresce, menos se vê. O que é?", "resposta": "escuridão"},
    {"pergunta": "O que corre, mas não tem pernas?", "resposta": "rio"},
    {"pergunta": "Qual é o animal que tem no meio do coração?", "resposta": "cavalo"},
]

# 🔢 Função que gera contas de acordo com a dificuldade
def gerar_conta(dificuldade):
    ops = ["+", "-", "*", "//", "**"]
    op = random.choice(ops[:2] if dificuldade == "fácil" else ops[:3] if dificuldade == "médio" else ops)

    a, b = random.randint(-10, 20), random.randint(-10, 20)

    if op == "//":  # divisão inteira, garantir resultado inteiro
        b = random.randint(1, 10)
        a = b * random.randint(-10, 10)
        resultado = a // b
    elif op == "**":
        a = random.randint(1, 5)
        b = random.randint(2, 3)
        resultado = a ** b
    else:
        resultado = eval(f"{a}{op}{b}")

    return {"tipo": "conta", "pergunta": f"Resolva: {a} {op} {b}", "resposta": str(resultado)}

# 🔀 Gera fase infinita com progressão de dificuldade
def gerar_fase(nivel=1):
    if nivel < 5:
        dificuldade = "fácil"
    elif nivel < 10:
        dificuldade = "médio"
    else:
        dificuldade = "difícil"

    tipo = random.choices(["conta", "emoji", "charada"], weights=[60, 25, 15])[0]

    if tipo == "conta":
        return gerar_conta(dificuldade)
    elif tipo == "emoji":
        cor = random.choice(list(CORES_EMOJIS.keys()))
        return {"tipo": "emoji", "pergunta": f"Digite um emoji {cor}.", "resposta": random.choice(CORES_EMOJIS[cor]), "cor": cor}
    else:
        return random.choice(CHARADAS)

# 🎭 Reações inteligentes e sarcásticas do Luiz
def gerar_reacao(tentativa, fase):
    tentativa = tentativa.strip().lower()
    resposta = fase["resposta"].strip().lower()
    tipo = fase.get("tipo", "conta")

    if tipo == "conta":
        try:
            tentativa_num = int(tentativa)
            resposta_num = int(resposta)
            diff = tentativa_num - resposta_num

            if tentativa_num == resposta_num:
                return "🤓 Luiz: Finalmente acertou! A matemática agradece. 📈"
            elif abs(diff) <= 2:
                return "🤓 Luiz: Quase lá, parece que a calculadora travou no último dígito. 🧮"
            elif tentativa_num > resposta_num:
                return "🤓 Luiz: Passou do ponto! Isso tá grande demais! 😅"
            else:
                return "🤓 Luiz: Tá muito baixo, nem o resultado te viu lá embaixo. 🕳️"
        except:
            return "🤓 Luiz: Isso é número ou foi inspirado em arte abstrata?"

    elif tipo == "emoji":
        cor_correta = fase["cor"]
        for cor, lista in CORES_EMOJIS.items():
            if tentativa in [e.lower() for e in lista]:
                if cor == cor_correta:
                    return f"🤓 Luiz: Boa! Isso sim é um emoji {cor}! 🌈"
                else:
                    return f"🤓 Luiz: Tá colorido, mas errou o tom... isso é {cor}, não {cor_correta}! 🎨"
        return "🤓 Luiz: Isso... é um emoji? Ou uma tentativa de arte moderna?"

    elif tipo == "charada":
        if tentativa == resposta:
            return "🤓 Luiz: Mandou bem! Acertou o enigma como um verdadeiro detetive 🕵️"
        else:
            return random.choice([
                "🤓 Luiz: Essa resposta foi... criativa 😅",
                "🤓 Luiz: Pensa diferente, o enigma é mais lógico do que parece!",
                "🤓 Luiz: Tá frio, muito frio! ❄️",
                "🤓 Luiz: Eu acreditava mais em você... mas ainda dá tempo!",
                "🤓 Luiz: Não é isso, mas gostei da tentativa 😂"
            ])

    return "🤓 Luiz: Acho que bugou meu cérebro com essa resposta..."

# 🧩 Sistema de avaliação
def avaliar_tentativa(fase, tentativa, tentativas):
    resposta_correta = fase["resposta"].strip().lower()
    tentativa_normalizada = tentativa.strip().lower()

    acertou = tentativa_normalizada == resposta_correta
    dica = gerar_reacao(tentativa, fase)

    if acertou:
        return True, f"✅ {dica}", ""

    if tentativas > 2:
        dica_extra = gerar_dica_extra(fase)
        dica += f" 🤔 Dica do Luiz: {dica_extra}"

    return False, f"❌ {dica}", dica

# 💡 Dicas adicionais do Luiz
def gerar_dica_extra(fase):
    if fase["tipo"] == "conta":
        return "Use a lógica matemática e lembre-se: nada de vírgula, só inteiros!"
    elif fase["tipo"] == "emoji":
        return f"Tente algo realmente {fase['cor']}."
    elif fase["tipo"] == "charada":
        return "Pense com criatividade, mas não complique demais!"
    return "A resposta é simples... se você for esperto o bastante 😏"
