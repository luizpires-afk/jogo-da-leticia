import random

def gerar_fase(numero_fase):
    temas = [
        ("Futebol", [
            ("Em que ano o Brasil perdeu de 7x1 para a Alemanha?", "2014"),
            ("Qual país venceu a Copa do Mundo de 2022?", "Argentina"),
            ("Quantos títulos mundiais o Brasil tem?", "5")
        ]),
        ("História", [
            ("Em que ano o homem pisou na Lua pela primeira vez?", "1969"),
            ("Ano em que começou a Segunda Guerra Mundial?", "1939"),
            ("Ano em que terminou a Segunda Guerra Mundial?", "1945")
        ]),
        ("Entretenimento", [
            ("Em que ano foi lançado o primeiro filme dos Vingadores?", "2012"),
            ("Ano de lançamento do primeiro iPhone?", "2007"),
            ("Ano de estreia de Stranger Things?", "2016")
        ]),
    ]

    tema, perguntas = random.choice(temas)
    num_perguntas = min(3 + numero_fase // 3, len(perguntas))  # aumenta dificuldade
    perguntas_fase = random.sample(perguntas, num_perguntas)

    senha_correta = "".join([resposta for _, resposta in perguntas_fase])
    dicas = [p for p, _ in perguntas_fase]

    return {
        "fase": numero_fase,
        "tema": tema,
        "dicas": dicas,
        "senha": senha_correta
    }


def resposta_ia(acertou, tentativas=0):
    respostas_acerto = [
        "Excelente! Você é demais! 🔓",
        "Uau, acertou em cheio! 🚀",
        "Parabéns, senha correta! Vamos para a próxima fase!",
        "Nada mal, humano. Você me surpreendeu 😏",
    ]

    respostas_erro = [
        "Hmm... acho que não é isso. Tente novamente!",
        "Senha incorreta! A IA está te observando 👀",
        "Quase lá, pense melhor nas dicas!",
        "Haha, você realmente achou que seria tão fácil?",
        "Tente prestar atenção nas perguntas, talvez algo esteja escondido nelas...",
    ]

    if acertou:
        return random.choice(respostas_acerto)
    else:
        # Adiciona um toque de personalidade conforme o número de erros
        if tentativas > 3:
            return "Você já errou várias vezes... quer uma dica extra? 😈"
        elif tentativas == 2:
            return "A senha tem {} caracteres. Isso ajuda?".format(random.randint(5, 15))
        return random.choice(respostas_erro)
