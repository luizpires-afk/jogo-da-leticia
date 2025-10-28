import json, os

arquivos = ["perguntas.json", "perguntas_extra.json"]
perguntas = []

for arq in arquivos:
    if os.path.exists(arq):
        print(f"🔍 Lendo {arq}...")
        with open(arq, "r", encoding="utf-8") as f:
            dados = json.load(f)
            print(f"✅ {len(dados)} perguntas carregadas de {arq}")
            perguntas.extend(dados)
    else:
        print(f"❌ Arquivo não encontrado: {arq}")

print(f"\n📊 Total de perguntas carregadas: {len(perguntas)}")
