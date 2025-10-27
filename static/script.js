document.addEventListener("DOMContentLoaded", () => {
  const perguntaEl = document.getElementById("pergunta");
  const falaEl = document.getElementById("fala");
  const faceEl = document.getElementById("luiz-face");
  const respostaEl = document.getElementById("resposta");
  const enviarBtn = document.getElementById("enviar");
  const nivelEl = document.getElementById("nivel");
  const pontosEl = document.getElementById("pontos");

  let humorEmojis = ["🤓", "😐", "😠", "😡", "💥"];

  // Inicializa o jogo
  fetch("/definir_jogador", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({nome: "Jogador"})
  })
    .then(res => res.json())
    .then(data => {
      falaEl.innerHTML = data.mensagem;
      perguntaEl.innerHTML = data.pergunta;
    });

  enviarBtn.addEventListener("click", () => {
    const resposta = respostaEl.value.trim();
    if (!resposta) return;

    fetch("/responder", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({resposta})
    })
      .then(res => res.json())
      .then(data => {
        falaEl.innerHTML = data.mensagem;
        perguntaEl.innerHTML = data.nova_pergunta;
        faceEl.textContent = humorEmojis[data.humor];
        nivelEl.textContent = `Nível: ${data.nivel}`;
        pontosEl.textContent = `Pontos: ${data.pontos}`;

        // animação de reação
        faceEl.style.transform = "scale(1.2)";
        setTimeout(() => faceEl.style.transform = "scale(1)", 400);

        respostaEl.value = "";
        respostaEl.focus();
      });
  });
});
