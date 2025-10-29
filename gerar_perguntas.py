import json
import os
import random
import re

# ---------------------------------------------
# Caminhos
# ---------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_PERGUNTAS = os.path.join(BASE_DIR, "perguntas.json")

# ---------------------------------------------
# Função: classificar dificuldade
# ---------------------------------------------
def classificar_pergunta(texto: str) -> str:
    """
    Atribui dificuldade automaticamente com base no conteúdo da pergunta.
    Retorna: 'facil', 'medio', 'dificil' ou 'pesadelo'
    """
    t = texto.lower()

    faceis = [
        "soma", "subtra", "adi", "cor", "animal", "capital", "multiplica",
        "+", "-", "quanto é", "2 + 2", "1 + 1", "quantos", "nome do"
    ]
    medias = [
        "presidente", "história", "descobriu", "planeta", "data", "química",
        "cientista", "energia", "fórmula", "multiplicação", "divisão"
    ]
    dificeis = [
        "teorema", "física", "álgebra", "equação", "raiz quadrada", "potência",
        "^", "log", "complexa", "derivada", "cálculo"
    ]
    pesadelo = [
        "quantum", "relatividade", "tungstênio", "nuclear", "criptografia",
        "história antiga", "imperador", "grego", "latim", "constante de planck"
    ]

    if any(p in t for p in pesadelo):
        return "pesadelo"
    elif any(p in t for p in dificeis):
        return "dificil"
    elif any(p in t for p in medias):
        return "medio"
    elif any(p in t for p in faceis):
        return "facil"

    # Heurísticas extras
    if re.search(r"[0-9]+\s*[\+\-\*/]\s*[0-9]+", t):
        return "facil"
    if re.search(r"[0-9]+\s*[\*/]\s*[0-9]+\s*[\+\-]\s*[0-9]+", t):
        return "medio"
    if re.search(r"\^|√", t):
        return "dificil"

    # fallback aleatório
    return random.choice(["facil", "medio", "dificil", "pesadelo"])

# ---------------------------------------------
# Banco base de perguntas automáticas
# ---------------------------------------------
temas = {
    "facil": [
        ("Qual é a capital do Brasil?", "Brasília", ["Rio de Janeiro", "São Paulo", "Salvador"]),
        ("Quanto é 5 + 3?", "8", ["7", "9", "10"]),
        ("Qual é o planeta mais próximo do Sol?", "Mercúrio", ["Vênus", "Terra", "Marte"]),
    ],
    "medio": [
        ("Quem escreveu 'Dom Casmurro'?", "Machado de Assis", ["José de Alencar", "Monteiro Lobato", "Clarice Lispector"]),
        ("Qual é o símbolo químico do ouro?", "Au", ["Ag", "Pt", "Pb"]),
        ("Em que continente fica o Egito?", "África", ["Ásia", "Europa", "América"]),
    ],
    "dificil": [
        ("Quem formulou as Leis de Newton?", "Isaac Newton", ["Einstein", "Galileu", "Kepler"]),
        ("Em que ano caiu o Império Romano do Ocidente?", "476", ["1453", "1066", "800"]),
        ("Qual é a capital da Islândia?", "Reykjavik", ["Oslo", "Helsinque", "Copenhague"]),
    ],
    "pesadelo": [
        ("Qual é o número atômico do elemento Tungstênio?", "74", ["79", "47", "82"]),
        ("Quem desenvolveu o primeiro algoritmo computacional conhecido?", "Ada Lovelace", ["Alan Turing", "Charles Babbage", "Grace Hopper"]),
        ("Qual é o idioma mais falado na Suíça?", "Alemão", ["Francês", "Italiano", "Romanche"]),
        ("Qual é a equação de Einstein que relaciona energia e massa?", "E=mc²", ["F=ma", "PV=nRT", "a²+b²=c²"]),
    ],
}

# ---------------------------------------------
# Gera perguntas estruturadas
# ---------------------------------------------
def gerar_banco():
    banco = []
    for nivel, perguntas in temas.items():
        for (texto, resposta_certa, erradas) in perguntas:
            alternativas = [resposta_certa] + erradas
            random.shuffle(alternativas)
            banco.append({
                "pergunta": texto,
                "alternativas": alternativas,
                "resposta": resposta_certa,
                "dificuldade": nivel,
                "categoria": "Geral",
                "dica": f"Pergunta nível {nivel.title()}."
            })
    return banco

# ---------------------------------------------
# Atualiza / cria perguntas.json
# ---------------------------------------------
def salvar_banco(perguntas_novas):
    if os.path.exists(CAMINHO_PERGUNTAS):
        with open(CAMINHO_PERGUNTAS, "r", encoding="utf-8") as f:
            try:
                existentes = json.load(f)
            except json.JSONDecodeError:
                existentes = []
    else:
        existentes = []

    textos_existentes = {p.get("pergunta", "").strip() for p in existentes}
    novas = [p for p in perguntas_novas if p["pergunta"].strip() not in textos_existentes]

    total = existentes + novas

    with open(CAMINHO_PERGUNTAS, "w", encoding="utf-8") as f:
        json.dump(total, f, ensure_ascii=False, indent=2)

    print(f"✅ Banco atualizado com {len(novas)} novas perguntas ({len(total)} no total).")

# ---------------------------------------------
# Carrega e garante que todas tenham dificuldade
# ---------------------------------------------
def carregar_perguntas_com_dificuldade():
    if not os.path.exists(CAMINHO_PERGUNTAS):
        raise FileNotFoundError(f"Arquivo {CAMINHO_PERGUNTAS} não encontrado!")

    with open(CAMINHO_PERGUNTAS, "r", encoding="utf-8") as f:
        perguntas = json.load(f)

    alterado = False
    for p in perguntas:
        if "dificuldade" not in p or p["dificuldade"] not in ["facil", "medio", "dificil", "pesadelo"]:
            p["dificuldade"] = classificar_pergunta(p.get("pergunta", ""))
            alterado = True

    if alterado:
        with open(CAMINHO_PERGUNTAS, "w", encoding="utf-8") as f:
            json.dump(perguntas, f, indent=4, ensure_ascii=False)

    return perguntas

# ---------------------------------------------
# Gerar pergunta aleatória
# ---------------------------------------------
def gerar_pergunta(dificuldade=None):
    perguntas = carregar_perguntas_com_dificuldade()
    if not perguntas:
        raise ValueError("Nenhuma pergunta disponível!")

    if dificuldade:
        filtradas = [p for p in perguntas if p.get("dificuldade") == dificuldade]
        if not filtradas:
            print(f"[AVISO] Nenhuma pergunta para '{dificuldade}'. Usando todas.")
            filtradas = perguntas
    else:
        filtradas = perguntas

    return random.choice(filtradas)

# ---------------------------------------------
# Execução direta (teste rápido)
# ---------------------------------------------
if __name__ == "__main__":
    novas = gerar_banco()
    salvar_banco(novas)

    todas = carregar_perguntas_com_dificuldade()
    print(f"📚 Total de perguntas: {len(todas)}")

    for nivel in ["facil", "medio", "dificil", "pesadelo"]:
        exemplo = gerar_pergunta(nivel)
        texto = (
            exemplo.get("pergunta")
            or exemplo.get("Pergunta")
            or exemplo.get("texto")
            or exemplo.get("questao")
            or str(exemplo)
        )
        print(f"\n[{nivel.upper()}] {texto}")
