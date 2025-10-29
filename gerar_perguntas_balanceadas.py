import json
import random

# 🔹 Caminho de saída
ARQUIVO_SAIDA = "perguntas_balanceadas.json"

# 🔹 Base de temas e perguntas — você pode expandir à vontade
banco_perguntas = {
    "matematica": {
        "facil": [
            ("Quanto é 2 + 2?", "4"),
            ("Quanto é 5 + 3?", "8"),
            ("Quanto é 10 - 6?", "4")
        ],
        "medio": [
            ("Quanto é 12 × 3?", "36"),
            ("Quanto é 45 ÷ 9?", "5"),
            ("Qual é o dobro de 27?", "54")
        ],
        "dificil": [
            ("Quanto é 15 × 14?", "210"),
            ("Qual é a raiz quadrada de 121?", "11")
        ]
    },
    "geografia": {
        "facil": [
            ("Qual é a capital do Brasil?", "Brasília"),
            ("Qual é a capital da França?", "Paris")
        ],
        "medio": [
            ("Em qual continente fica o Egito?", "África"),
            ("Qual é o maior país do mundo em extensão territorial?", "Rússia")
        ],
        "dificil": [
            ("Qual é a capital da Islândia?", "Reykjavik"),
            ("Em que oceano está Madagascar?", "Oceano Índico")
        ]
    },
    "historia": {
        "facil": [
            ("Quem foi o primeiro presidente do Brasil?", "Deodoro da Fonseca")
        ],
        "medio": [
            ("Em que ano o Brasil proclamou a independência?", "1822"),
            ("Quem descobriu o Brasil?", "Pedro Álvares Cabral")
        ],
        "dificil": [
            ("Em que ano começou a Segunda Guerra Mundial?", "1939"),
            ("Quando terminou a Primeira Guerra Mundial?", "1918")
        ]
    },
    "ciencias": {
        "facil": [
            ("Qual é o planeta mais próximo do Sol?", "Mercúrio"),
            ("Qual é o gás que os humanos respiram?", "Oxigênio")
        ],
        "medio": [
            ("Qual é o elemento químico representado por 'O'?", "Oxigênio"),
            ("Qual é o maior órgão do corpo humano?", "Pele")
        ],
        "dificil": [
            ("Qual é o elemento químico representado por 'Au'?", "Ouro"),
            ("Qual é o nome científico da água?", "H2O")
        ]
    },
    "cultura_pop": {
        "facil": [
            ("Qual é o nome do rato famoso da Disney?", "Mickey Mouse"),
            ("Quem é o personagem principal de 'Bob Esponja'?", "Bob Esponja")
        ],
        "medio": [
            ("Em qual filme aparece o sabre de luz?", "Star Wars"),
            ("Quem canta 'Shape of You'?", "Ed Sheeran")
        ],
        "dificil": [
            ("Quem dirigiu o filme 'Interestelar'?", "Christopher Nolan"),
            ("Qual série tem o personagem Walter White?", "Breaking Bad")
        ]
    },
    "curiosidades": {
        "facil": [
            ("Qual fruta é símbolo do amor?", "Maçã"),
            ("Qual é o animal mais rápido do mundo?", "Guepardo")
        ],
        "medio": [
            ("Quantos ossos tem o corpo humano adulto?", "206"),
            ("Quantos planetas há no Sistema Solar?", "8")
        ],
        "dificil": [
            ("Quantos anos tem um século?", "100"),
            ("Qual é o nome da galáxia em que vivemos?", "Via Láctea")
        ]
    },
    "pesadelo": {
        "pesadelo": [
            ("Em que ano caiu o Império Romano do Ocidente?", "476"),
            ("Qual é o número atômico do Urânio?", "92"),
            ("Quem formulou a Teoria da Relatividade Geral?", "Albert Einstein"),
            ("Qual o nome do cientista que descobriu o elétron?", "J. J. Thomson"),
            ("Em que ano o homem pisou na Lua?", "1969")
        ]
    }
}

# 🔹 Geração do banco balanceado
perguntas_final = []

for tema, niveis in banco_perguntas.items():
    for nivel, lista in niveis.items():
        for pergunta, resposta in lista:
            perguntas_final.append({
                "pergunta": pergunta,
                "resposta": resposta,
                "dificuldade": nivel,
                "tema": tema
            })

# 🔹 Embaralhar para variedade
random.shuffle(perguntas_final)

# 🔹 Salvar o novo arquivo
with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(perguntas_final, f, ensure_ascii=False, indent=2)

print(f"✅ Banco de perguntas gerado com sucesso: {len(perguntas_final)} perguntas salvas em '{ARQUIVO_SAIDA}'")
