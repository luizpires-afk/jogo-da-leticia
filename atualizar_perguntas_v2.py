import json
import os
import random
from datetime import datetime

# ------------------------------------
# ⚙️ CONFIGURAÇÕES
# ------------------------------------
ARQUIVO_ORIGINAL = "perguntas.json"
ARQUIVO_SAIDA = "perguntas_balanceadas.json"
BACKUP_AUTOMATICO = True
MODO_TESTE = False
GERAR_NOVAS = True

# ------------------------------------
# 🧩 FUNÇÕES DE ARQUIVO
# ------------------------------------
def carregar_perguntas(arquivo):
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo não encontrado: {arquivo} (será criado novo banco)")
        return []
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if not isinstance(dados, list):
            print("⚠️ Estrutura inválida — o arquivo deve conter uma lista de perguntas.")
            return []
        return dados
    except json.JSONDecodeError:
        print("❌ Erro ao ler o arquivo JSON — verifique a formatação.")
        return []

def salvar_perguntas(perguntas, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(perguntas, f, indent=4, ensure_ascii=False)
    print(f"✅ Arquivo salvo com sucesso: {arquivo}")

def criar_backup(arquivo):
    if os.path.exists(arquivo):
        data = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_backup = f"{arquivo.replace('.json', '')}_backup_{data}.json"
        os.rename(arquivo, nome_backup)
        print(f"🗂️ Backup criado: {nome_backup}")

# ------------------------------------
# 🧠 CLASSIFICAÇÃO AUTOMÁTICA
# ------------------------------------
def classificar_pergunta(pergunta):
    texto = pergunta.get("texto", "").lower().strip()
    dificuldade = pergunta.get("dificuldade", "").lower().strip()

    # Menos peso para perguntas matemáticas
    if any(op in texto for op in ["+", "-", "÷", "/", "x", "*", "quanto é"]):
        dificuldade = "facil"

    # Perguntas com ano = difícil
    if any(str(ano) in texto for ano in range(1500, 2100)):
        dificuldade = "dificil"

    # Perguntas do tipo “Quem”, “Qual”, “O que” — categorização leve
    if any(padrao in texto for padrao in ["quem", "qual", "o que", "onde"]):
        if "ano" in texto or "quando" in texto or "em que" in texto:
            dificuldade = "dificil"
        elif len(texto.split()) > 8:
            dificuldade = "medio"
        else:
            dificuldade = "facil"

    if not dificuldade:
        dificuldade = random.choice(["facil", "medio", "dificil"])

    return {
        "texto": texto.capitalize(),
        "resposta": pergunta.get("resposta", "").lower(),
        "dificuldade": dificuldade
    }

# ------------------------------------
# 🌱 GERADOR AUTOMÁTICO (balanceado)
# ------------------------------------
def gerar_perguntas_automaticas():
    perguntas = []

    # Fáceis — lógica cotidiana
    perguntas += [
        {"texto": "Qual é a capital do Brasil?", "resposta": "brasilia", "dificuldade": "facil"},
        {"texto": "De que cor é o céu em um dia claro?", "resposta": "azul", "dificuldade": "facil"},
        {"texto": "Qual animal é conhecido como o rei da selva?", "resposta": "leão", "dificuldade": "facil"},
        {"texto": "Quantos dias tem uma semana?", "resposta": "7", "dificuldade": "facil"},
        {"texto": "Qual é o nome do satélite natural da Terra?", "resposta": "lua", "dificuldade": "facil"},
        {"texto": "Em que estação do ano as flores costumam florescer?", "resposta": "primavera", "dificuldade": "facil"},
        {"texto": "Qual é o oposto de quente?", "resposta": "frio", "dificuldade": "facil"},
        {"texto": "Qual fruta é conhecida por ser amarela e rica em potássio?", "resposta": "banana", "dificuldade": "facil"},
    ]

    # Médias — cultura, geografia, ciências simples
    perguntas += [
        {"texto": "Quem descobriu o Brasil?", "resposta": "pedro alvares cabral", "dificuldade": "medio"},
        {"texto": "Qual é o maior planeta do sistema solar?", "resposta": "jupiter", "dificuldade": "medio"},
        {"texto": "O que é H2O?", "resposta": "agua", "dificuldade": "medio"},
        {"texto": "Quem pintou a Mona Lisa?", "resposta": "leonardo da vinci", "dificuldade": "medio"},
        {"texto": "Em que continente está o Egito?", "resposta": "africa", "dificuldade": "medio"},
        {"texto": "Qual o idioma mais falado no mundo?", "resposta": "ingles", "dificuldade": "medio"},
        {"texto": "Qual o menor país do mundo?", "resposta": "vaticano", "dificuldade": "medio"},
        {"texto": "Quem escreveu Dom Quixote?", "resposta": "miguel de cervantes", "dificuldade": "medio"},
        {"texto": "Em que continente fica o Japão?", "resposta": "asia", "dificuldade": "medio"},
        {"texto": "Quem foi Napoleão Bonaparte?", "resposta": "imperador francês", "dificuldade": "medio"}
    ]

    # Difíceis — história, ciência e cultura global
    perguntas += [
        {"texto": "Em que ano o homem pisou na Lua pela primeira vez?", "resposta": "1969", "dificuldade": "dificil"},
        {"texto": "Qual é o elemento químico representado por 'Au'?", "resposta": "ouro", "dificuldade": "dificil"},
        {"texto": "Quem desenvolveu a teoria da relatividade?", "resposta": "albert einstein", "dificuldade": "dificil"},
        {"texto": "Qual é a capital da Austrália?", "resposta": "camberra", "dificuldade": "dificil"},
        {"texto": "Qual cientista formulou as leis do movimento?", "resposta": "isaac newton", "dificuldade": "dificil"},
        {"texto": "Em que ano começou a Segunda Guerra Mundial?", "resposta": "1939", "dificuldade": "dificil"},
        {"texto": "Quem foi o primeiro presidente do Brasil?", "resposta": "marechal deodoro da fonseca", "dificuldade": "dificil"},
        {"texto": "Em que país nasceu o físico Albert Einstein?", "resposta": "alemanha", "dificuldade": "dificil"},
        {"texto": "Qual é a fórmula química do sal de cozinha?", "resposta": "nacl", "dificuldade": "dificil"}
    ]

    return perguntas

# ------------------------------------
# 🚀 FLUXO PRINCIPAL (HÍBRIDO)
# ------------------------------------
def atualizar_banco():
    print("🔄 Atualizando banco de perguntas...")

    perguntas_existentes = carregar_perguntas(ARQUIVO_ORIGINAL)
    print(f"📁 Perguntas existentes: {len(perguntas_existentes)}")

    novas_perguntas = gerar_perguntas_automaticas() if GERAR_NOVAS else []
    print(f"✨ Novas perguntas geradas: {len(novas_perguntas)}")

    todas = perguntas_existentes + novas_perguntas

    # Remove duplicadas
    unicas = {p["texto"].strip().lower(): p for p in todas}.values()

    # Reclassifica e normaliza
    atualizadas = [classificar_pergunta(p) for p in unicas if p.get("texto") and p.get("resposta")]

    totais = {"facil": 0, "medio": 0, "dificil": 0}
    for p in atualizadas:
        if p["dificuldade"] in totais:
            totais[p["dificuldade"]] += 1

    print("\n📊 Distribuição final:")
    for k, v in totais.items():
        print(f"  - {k.capitalize()}: {v}")

    if not MODO_TESTE:
        if BACKUP_AUTOMATICO:
            criar_backup(ARQUIVO_SAIDA)
        salvar_perguntas(atualizadas, ARQUIVO_SAIDA)
    else:
        print("🧪 MODO TESTE — nada foi sobrescrito.")

    print("\n✅ Banco balanceado e atualizado com sucesso!")

# ------------------------------------
# ▶️ EXECUÇÃO
# ------------------------------------
if __name__ == "__main__":
    atualizar_banco()
