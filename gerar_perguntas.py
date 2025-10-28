import json
import random

# Categorias variadas
categorias = {
    "matematica": [
        ("Quanto é {a} + {b}?", lambda a, b: str(a + b)),
        ("Resolva: {a} x {b}", lambda a, b: str(a * b)),
        ("Quanto é {a} - {b}?", lambda a, b: str(a - b)),
        ("Quanto é {a} ÷ {b}?", lambda a, b: str(int(a / b))),  # garantimos divisão inteira abaixo
    ],
    "geografia": [
        ("Qual é a capital da Alemanha?", "berlim"),
        ("Em que continente fica o Egito?", "áfrica"),
        ("Qual país é conhecido como a Terra do Sol Nascente?", "japão"),
        ("Qual é o maior oceano do planeta?", "pacífico"),
        ("Qual é o deserto mais quente do mundo?", "saara"),
        {"texto": "Qual é a capital do Canadá?", "resposta": "ottawa"},
        {"texto": "Quem inventou a lâmpada?", "resposta": "thomas edison"},
        {"texto": "Quem escreveu Dom Casmurro?", "resposta": "machado de assis"},
        {"texto": "Qual é o maior animal terrestre?", "resposta": "elefante africano"}
    ],
    "ciencia": [
        ("Qual é o planeta mais próximo do Sol?", "mercúrio"),
        ("O que os humanos respiram para viver?", "oxigênio"),
        ("Qual é o órgão responsável por bombear sangue?", "coração"),
        ("Qual é o estado físico da água no gelo?", "sólido"),
        ("Qual é o símbolo químico da água?", "h2o"),
    ],
    "historia": [
        ("Quem descobriu o Brasil?", "pedro álvares cabral"),
        ("Em que ano começou a Segunda Guerra Mundial?", "1939"),
        ("Quem foi o primeiro presidente dos Estados Unidos?", "george washington"),
        ("Em que ano o homem pisou na Lua?", "1969"),
        ("Quem foi Napoleão Bonaparte?", "imperador francês"),
    ],
    "curiosidades": [
        ("Quantas cores tem o arco-íris?", "7"),
        ("Que animal é conhecido por sua memória?", "elefante"),
        ("Qual fruta é símbolo do amor?", "maçã"),
        ("Qual é o metal mais leve do mundo?", "lítio"),
        ("Qual é o idioma mais falado do mundo?", "inglês"),
    ],
    "cultura_pop": [
        ("Quem é o criador do Mickey Mouse?", "walt disney"),
        ("Qual é o nome do mago em O Senhor dos Anéis?", "gandalf"),
        ("Qual é o nome do mago em Harry Potter?", "dumbledore"),
        ("Em que casa de Hogwarts está Harry Potter?", "grifinória"),
        ("Qual é o nome do robô dourado em Star Wars?", "c3po"),
        ("Quem canta 'Thriller'?", "michael jackson"),
        ("Quem é o super-herói de Gotham City?", "batman"),
        ("Qual é o verdadeiro nome do Homem-Aranha?", "peter parker"),
        ("Quem é o vilão principal em Star Wars?", "darth vader"),
        ("Qual é o nome do martelo do Thor?", "mjolnir"),
        ("Quem é o líder dos Vingadores?", "capitão américa"),
        ("Qual é o nome do planeta natal do Superman?", "krypton"),
        ("Quem é o detetive da série 'Sherlock'?", "sherlock holmes"),
        ("Qual é o nome da escola de mutantes dos X-Men?", "xavier"),
        ("Qual é o nome da princesa de Star Wars?", "leia"),
        ("Quem é o famoso encanador da Nintendo?", "mario"),
        ("Quem é o irmão do Mario?", "luigi"),
        ("Quem é o protagonista de The Legend of Zelda?", "link")
    ],
    "charadas": [
        ("O que é, o que é: quanto mais tira, maior fica?", "buraco"),
        ("Tem dente, mas não morde. O que é?", "pente"),
        ("Tem pescoço mas não tem cabeça. O que é?", "garrafa"),
        ("Quanto mais se seca, mais molhado fica. O que é?", "toalha"),
        ("Cai em pé e corre deitado. O que é?", "chuva"),
        ("Anda com os pés na cabeça. O que é?", "piolho"),
        ("É redondo, tem bola, mas não é jogo. O que é?", "olho"),
        ("Não tem asas, mas voa. O que é?", "tempo"),
        ("Quanto mais cresce, menor fica. O que é?", "vela"),
        ("Tem chaves, mas não abre portas. O que é?", "piano"),
        ("Corre mas não tem pernas. O que é?", "rio"),
        ("Tem boca mas não fala. O que é?", "rio"),
        ("Tem orelhas mas não ouve. O que é?", "milho"),
        ("Pode ser de vidro, mas não é janela. O que é?", "garrafa")
    ]
}

# Lista final de perguntas (cada item: {"texto": ..., "resposta": ...})
perguntas = []

# 1) Gerar muitas perguntas de matemática (variáveis) de forma segura
math_templates = categorias.get("matematica", [])
# Quantidade desejada; ajuste conforme necessário (ex: 2000)
MATH_COUNT = 100

for _ in range(MATH_COUNT):
    formato, func = random.choice(math_templates)

    # Gera valores a e b apropriados
    # Para divisão, garantimos que o resultado seja inteiro: fazemos a = b * q
    if "÷" in formato or "÷" in formato:
        b = random.randint(1, 12)
        q = random.randint(1, 12)
        a = b * q
    else:
        a = random.randint(1, 100)
        b = random.randint(1, 100)

    # Calcula resposta usando func (certificando-se que func é chamável)
    if callable(func):
        try:
            resposta = func(a, b)
        except Exception:
            # fallback seguro
            if "÷" in formato:
                resposta = str(int(a / b))
            else:
                resposta = str(a + b)
    else:
        # caso inesperado, tratar como string
        resposta = str(func)

    texto = formato.format(a=a, b=b)
    perguntas.append({"texto": texto, "resposta": str(resposta).lower()})

# 2) Adicionar perguntas estáticas (uma vez cada)
for categoria, lista in categorias.items():
    if categoria == "matematica":
        continue  # já geradas acima
    for item in lista:
        # cada item pode ser (texto, resposta) onde resposta é string
        texto, resposta = item
        perguntas.append({"texto": texto, "resposta": str(resposta).lower()})

# 3) Embaralhar e salvar
random.shuffle(perguntas)

with open("perguntas.json", "w", encoding="utf-8") as f:
    json.dump(perguntas, f, ensure_ascii=False, indent=2)

print(f"✅ Geradas {len(perguntas)} perguntas e salvas em 'perguntas.json'.")
