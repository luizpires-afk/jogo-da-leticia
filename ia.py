# ia.py
# Backend do "Desafio do Luiz" — versão otimizada para comportamento progressivo,
# temporizador fluido, modo PESADELO (5s), reações do Luiz e ranking persistente.

import random
import json
import os
import time
from datetime import datetime

# ----------------------------
# Configurações
# ----------------------------
ARQUIVOS_PERGUNTAS = [
    "perguntas_atualizadas.json",
    "perguntas_balanceadas.json",
    "perguntas.json",
    "perguntas_extra.json",
    "perguntas.js"
]
RANKING_FILE = "ranking.json"
LOG_FILE = "ia_log.txt"

TEMPO_TETO = {
    "facil": 30,
    "medio": 22,
    "dificil": 14,
    "pesadelo": 5
}

# ----------------------------
# Utilitários
# ----------------------------
def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.utcnow().isoformat()}] {msg}\n")
    except Exception:
        pass

def safe_lower_trim(s):
    return (s or "").strip().lower()

# ----------------------------
# Classe IA
# ----------------------------
class IA:
    def __init__(self):
        self.estado = {
            "nivel": 1,
            "humor_level": 0,
            "tentativas": 0,
            "game_over": False,
            "pontos": 0,
            "fase": {},
            "jogador": "Jogador",
            "tempo_restante": TEMPO_TETO["facil"],
            "inicio_tempo": time.time(),
            "modo_pesadelo": False,
            "acertos_consecutivos_dificil": 0,
            "acertos_consecutivos": 0
        }

        self.perguntas_feitas = []
        self.PERGUNTAS_EXTERNAS = self._carregar_perguntas_externas()
        self.PERGUNTAS_BACKUP = self._perguntas_backup()
        self._normalize_perguntas()
        log(f"IA inicializada. Perguntas externas: {len(self.PERGUNTAS_EXTERNAS)}")

    # ----------------------------
    def obter_perguntas_por_dificuldade(self, dificuldade):
        perguntas = self.PERGUNTAS_EXTERNAS if self.PERGUNTAS_EXTERNAS else self.PERGUNTAS_BACKUP
        filtradas = [p for p in perguntas if (p.get("dificuldade") or "medio") == dificuldade]
        return filtradas or perguntas

    # ----------------------------
    def _carregar_perguntas_externas(self):
        todas = []
        for arquivo in ARQUIVOS_PERGUNTAS:
            if not os.path.exists(arquivo):
                continue
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()
                    if arquivo.endswith(".js"):
                        conteudo = conteudo.replace("window.bancoPerguntas =", "").rstrip(";").strip()
                    dados = json.loads(conteudo)
                    if isinstance(dados, list):
                        todas.extend(dados)
                        log(f"Carregadas {len(dados)} perguntas de {arquivo}")
            except Exception as e:
                log(f"Erro ao ler {arquivo}: {e}")
        return todas

    # ----------------------------
    def _normalize_perguntas(self):
        norm = []
        for p in self.PERGUNTAS_EXTERNAS:
            try:
                if not isinstance(p, dict):
                    continue
                texto = (p.get("pergunta") or p.get("texto") or "").strip()
                raw = p.get("resposta") or p.get("respostas") or ""
                if isinstance(raw, list):
                    respostas = [safe_lower_trim(x) for x in raw if x]
                else:
                    respostas = [safe_lower_trim(str(raw))]
                dif = (p.get("dificuldade") or p.get("nivel") or "").strip().lower()
                if dif not in ("facil", "medio", "dificil", "pesadelo"):
                    t = texto.lower()
                    dif = "facil" if any(sym in t for sym in ["+", "-", "x", "/", "*", "quanto é"]) else "medio"
                dica = p.get("dica") or ""
                if texto and respostas:
                    norm.append({
                        "pergunta": texto,
                        "resposta": respostas,
                        "dificuldade": dif,
                        "dica": dica
                    })
            except Exception as e:
                log(f"Erro normalizar pergunta: {e}")
        self.PERGUNTAS_EXTERNAS = norm

    # ----------------------------
    def _perguntas_backup(self):
        return [
            {"pergunta": "Quanto é 2 + 2?", "resposta": ["4", "quatro"], "dificuldade": "facil"},
            {"pergunta": "Qual é a capital do Brasil?", "resposta": ["brasilia"], "dificuldade": "facil"},
            {"pergunta": "Quem pintou a Mona Lisa?", "resposta": ["leonardo da vinci"], "dificuldade": "medio"},
            {"pergunta": "Em que ano o homem pisou na Lua pela primeira vez?", "resposta": ["1969"], "dificuldade": "dificil"},
        ]

    # ----------------------------
    def carregar_ranking(self):
        if os.path.exists(RANKING_FILE):
            try:
                with open(RANKING_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def salvar_ranking(self, rank):
        try:
            with open(RANKING_FILE, "w", encoding="utf-8") as f:
                json.dump(rank, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log(f"erro salvar ranking: {e}")

    def atualizar_recorde(self, nome, pontos):
        rank = self.carregar_ranking()
        rank[nome] = max(rank.get(nome, 0), int(pontos))
        ordenado = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[:100])
        self.salvar_ranking(ordenado)

    # ----------------------------
    def dificuldade_por_nivel(self):
        if self.estado["modo_pesadelo"]:
            return "pesadelo"
        n = self.estado["nivel"]
        if n < 5:
            return "facil"
        if n < 10:
            return "medio"
        return "dificil"

    # ----------------------------
    def ganho_por_acerto(self, dif):
        base = 6 if dif == "facil" else 4 if dif == "medio" else 2
        decaimento = (self.estado["nivel"] - 1) // 5
        return max(1, base - decaimento)

    # ----------------------------
    def proxima_pergunta(self, dificuldade_forcada=None):
        dificuldade = "dificil" if self.estado.get("modo_pesadelo") else (dificuldade_forcada or self.dificuldade_por_nivel())
        perguntas = self.obter_perguntas_por_dificuldade(dificuldade)
        restantes = [p for p in perguntas if p["pergunta"] not in self.perguntas_feitas]
        if not restantes:
            self.perguntas_feitas.clear()
            restantes = perguntas
        pergunta = random.choice(restantes)
        self.perguntas_feitas.append(pergunta["pergunta"])

        self.estado["tempo_restante"] = TEMPO_TETO["pesadelo"] if self.estado["modo_pesadelo"] else max(10, 30 - min(self.estado["nivel"] * 0.7, 20))

        if self.estado.get("modo_pesadelo") and not pergunta.get("alternativas"):
            todas_respostas = [p["resposta"][0] for p in perguntas if p.get("resposta")]
            alternativas = random.sample(todas_respostas, min(3, len(todas_respostas)))
            if pergunta["resposta"][0] not in alternativas:
                alternativas[random.randrange(len(alternativas))] = pergunta["resposta"][0]
            pergunta["alternativas"] = alternativas

        self.estado["fase"] = pergunta
        return {
            "pergunta": pergunta["pergunta"],
            "alternativas": pergunta.get("alternativas", []),
            "dificuldade": dificuldade
        }

    # ----------------------------
    def reacao_luiz(self):
        hl = self.estado["humor_level"]
        if hl <= 0: return "🤓 Tranquilo e confiante!"
        if hl == 1: return "🙂 Tá indo bem!"
        if hl == 2: return "😐 Meio chateado..."
        if hl == 3: return "😠 Tá ficando bravo..."
        if hl == 4: return "😡 Muito zangado!"
        return "💥 Luiz explodiu de raiva!"

    # ----------------------------
    def entrar_pesadelo(self):
        self.estado.update({
            "modo_pesadelo": True,
            "nivel": 999,
            "tempo_restante": TEMPO_TETO["pesadelo"],
            "acertos_consecutivos_dificil": 0,
            "humor_level": 0,
            "game_over": False
        })
        pergunta = self.proxima_pergunta(dificuldade_forcada="dificil")
        return {
            "mensagem": "🔥 Bem-vindo ao MODO PESADELO! Agora é tudo ou nada...",
            "pergunta": pergunta,
            "tempo_restante": self.estado["tempo_restante"],
            "pontos": self.estado["pontos"],
            "nivel": "∞",
            "dificuldade": "pesadelo"
        }

    # ----------------------------
    def _handle_tempo_esgotado(self):
        self.estado["humor_level"] += 1
        self.estado["acertos_consecutivos"] = 0
        self.estado["acertos_consecutivos_dificil"] = 0
        self.estado["tentativas"] += 1

        if self.estado["modo_pesadelo"]:
            self.estado["game_over"] = True
            self.atualizar_recorde(self.estado["jogador"], self.estado["pontos"])
            return {"acertou": False, "mensagem": "⏰ Tempo esgotado no PESADELO!", "fim": True, "pontuacao_final": self.estado["pontos"]}

        if self.estado["humor_level"] >= 5:
            self.estado["game_over"] = True
            self.atualizar_recorde(self.estado["jogador"], self.estado["pontos"])
            return {"acertou": False, "mensagem": "⏰ Tempo esgotado! Fim de jogo.", "fim": True}

        proxima = self.proxima_pergunta()
        return {"acertou": False, "mensagem": "⏰ Tempo esgotado!", "nova_pergunta": proxima}

    # ----------------------------
    def verificar_resposta(self, tentativa_raw: str):
        tentativa = safe_lower_trim(tentativa_raw)
        if tentativa == "__TEMPO_ESGOTADO__":
            return self._handle_tempo_esgotado()
        if self.estado["game_over"]:
            return {"acertou": False, "mensagem": "Jogo terminado.", "fim": True}

        fase = self.estado.get("fase", {})
        respostas = [safe_lower_trim(r) for r in fase.get("resposta", [])]

        if tentativa in ("te amo", "eu te amo", "amo voce", "amo você"):
            self.estado["pontos"] += 5
            self.estado["nivel"] += 1
            self.estado["humor_level"] = max(0, self.estado["humor_level"] - 1)
            self.atualizar_recorde(self.estado["jogador"], self.estado["pontos"])
            proxima = self.proxima_pergunta()
            return {"acertou": True, "mensagem": "🥰 Eu também te amo!", "nova_pergunta": proxima}

        acertou = tentativa in respostas
        if acertou:
            self.estado["pontos"] += 10
            self.estado["nivel"] += 1
            self.estado["humor_level"] = max(0, self.estado["humor_level"] - 1)
            self.atualizar_recorde(self.estado["jogador"], self.estado["pontos"])
            proxima = self.proxima_pergunta()
            return {"acertou": True, "mensagem": "✅ Correto!", "nova_pergunta": proxima}

        self.estado["pontos"] = max(0, self.estado["pontos"] - 2)
        self.estado["humor_level"] += 1
        proxima = self.proxima_pergunta()
        return {"acertou": False, "mensagem": f"❌ Errou! Dica: {fase.get('dica','')}", "nova_pergunta": proxima}

    # ----------------------------
    def _formatar_resposta(self, resposta_dict):
        if isinstance(resposta_dict, dict) and "nova_pergunta" in resposta_dict:
            if isinstance(resposta_dict["nova_pergunta"], dict):
                resposta_dict["nova_pergunta"] = resposta_dict["nova_pergunta"].get("pergunta", "")
        return resposta_dict


# ======================================================
# 🔧 GARANTIA DE TEXTO LIMPO (EVITA [object Object])
# ======================================================
def _garantir_texto_pergunta(pergunta):
    if isinstance(pergunta, dict):
        return pergunta.get("pergunta") or pergunta.get("texto") or str(pergunta)
    return str(pergunta)


if hasattr(IA, "proxima_pergunta_original") is False:
    IA.proxima_pergunta_original = IA.proxima_pergunta

    def proxima_pergunta_segura(self, dificuldade_forcada=None):
        p = self.proxima_pergunta_original(dificuldade_forcada)
        # Garante que a pergunta é string limpa
        if isinstance(p, dict) and "pergunta" in p:
            p["pergunta"] = _garantir_texto_pergunta(p["pergunta"])
        return p

    IA.proxima_pergunta = proxima_pergunta_segura
