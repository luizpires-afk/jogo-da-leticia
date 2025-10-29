let tempoRestante = 30;
let temporizador;
let modoPesadelo = false;

function iniciar() {
    const nome = document.getElementById("nomeInput").value.trim();
    if (!nome) {
        alert("Digite seu nome antes de começar!");
        return;
    }

    fetch("/iniciar", {
        method: "POST",
        body: new URLSearchParams({ nome })
    })
    .then(res => res.json())
    .then(dados => {
        document.getElementById("jogo").style.display = "block";
        document.getElementById("pergunta").innerText = dados.pergunta;
        tempoRestante = dados.tempo_restante || 30;
        atualizarBalão(dados.mensagem);
        iniciarTimer();
    });
}

function responder() {
    const tentativa = document.getElementById("respostaInput").value.trim();
    if (!tentativa) return;
    clearInterval(temporizador);

    fetch("/responder", {
        method: "POST",
        body: new URLSearchParams({ tentativa })
    })
    .then(res => res.json())
    .then(dados => {
        if (dados.fim) {
            atualizarBalão(dados.mensagem + " 🏁 Pontuação: " + dados.pontuacao_final);
            mostrarRanking();
            return;
        }

        if (dados.modo_pesadelo_opcao) {
            if (confirm(dados.mensagem)) ativarModoPesadelo();
            else proximaPergunta(dados.nova_pergunta, dados.tempo_restante);
            return;
        }

        atualizarBalão(dados.mensagem);
        proximaPergunta(dados.nova_pergunta, dados.tempo_restante);
    });
}

function proximaPergunta(pergunta, tempo = 30) {
    document.getElementById("respostaInput").value = "";
    document.getElementById("pergunta").innerText = pergunta;
    tempoRestante = tempo;
    iniciarTimer();
}

function iniciarTimer() {
    clearInterval(temporizador);
    document.getElementById("tempo").innerText = tempoRestante;
    temporizador = setInterval(() => {
        tempoRestante--;
        document.getElementById("tempo").innerText = tempoRestante;
        if (tempoRestante <= 0) {
            clearInterval(temporizador);
            atualizarBalão("⏰ O tempo acabou!");
            mostrarRanking();
        }
    }, 1000);
}

function ativarModoPesadelo() {
    modoPesadelo = true;
    fetch("/modo_pesadelo", { method: "POST" })
        .then(res => res.json())
        .then(dados => {
            atualizarBalão(dados.mensagem);
            proximaPergunta(dados.nova_pergunta, dados.tempo_restante);
        });
}

function atualizarBalão(texto) {
    const balao = document.getElementById("balão");
    balao.innerText = texto;
    balao.style.transform = "scale(1.1)";
    setTimeout(() => balao.style.transform = "scale(1)", 200);
}

function mostrarRanking() {
    fetch("/ranking")
    .then(res => res.json())
    .then(lista => {
        let html = "<h3>🏆 Ranking Global</h3><ol>";
        lista.forEach(([nome, pontos]) => {
            html += `<li>${nome} — ${pontos} pts</li>`;
        });
        html += "</ol>";
        document.getElementById("ranking").innerHTML = html;
    });
}
