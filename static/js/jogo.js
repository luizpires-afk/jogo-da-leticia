// elemento
const input = document.getElementById("inputSenha");
const btn = document.getElementById("btnEnviar");
const baloon = document.getElementById("baloon");
const baloonText = document.getElementById("baloonText");
const mascot = document.getElementById("mascote");
const voz = document.getElementById("voz");
const hint = document.getElementById("hint");
const status = document.getElementById("status");


let lastReq = 0;

// util: mostra balão com efeito de digitação (simples)
function showBaloonText(text){
  baloon.classList.add("show");
  baloonText.textContent = "";
  let i=0;
  const id = setInterval(()=>{
    baloonText.textContent = text.slice(0,i);
    i++;
    if(i>text.length){ clearInterval(id); }
  }, 22);
}

// toca um arquivo de voz se existir
function playVoice(filename){
  if(!filename) return;
  voz.src = `/static/audio/${filename}`;
  voz.play().catch(()=>{ /* ignora erros de autoplay */ });
}

// animações faciais simples (muda sobrancelhas/olhos)
function setMascotMood(mood){
  // mood: 'neutro','feliz','irritado','pensando'
  mascot.classList.remove("shake","happy");
  if(mood === 'irritado'){ mascot.classList.add("shake"); }
  if(mood === 'feliz'){ mascot.classList.add("happy"); }
}

// REAÇÃO em tempo real enquanto digita (debounce)
input.addEventListener("input", async ()=>{
  const parcial = input.value;
  lastReq++;
  const thisReq = lastReq;
  // chama /reagir para reacao curta
  try{
    const resp = await fetch("/reagir", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ parcial })
    });
    if(thisReq !== lastReq) return; // descartas antigas
    const data = await resp.json();
    // mostra fala curta (dica + reacao)
    if(data.dica) showBaloonText(data.dica);
    if(data.reacao){
      showBaloonText(data.reacao.fala);
      playVoice(data.reacao.get ? data.reacao.get('voz') : data.reacao.voz);
      // mood heurística
      const emo = data.reacao.emoji || '';
      if(emo.includes('😤')||emo.includes('😤')) setMascotMood('irritado');
      else if(emo.includes('😏')||emo.includes('🤔')) setMascotMood('pensando');
      else setMascotMood('neutro');
    }
  }catch(e){
    // console.warn(e);
  }
});

// SUBMIT tentativa completa
btn.addEventListener("click", async ()=>{
  const tentativa = input.value.trim();
  if(!tentativa) return;
  try{
    const resp = await fetch("/tentar", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ tentativa })
    });
    const data = await resp.json();

    // mostra mensagem e fala
    status.textContent = data.mensagem || "";
    showBaloonText(data.reacao.fala || "");
    playVoice(data.reacao.voz);

    // define humor do mascot
    if(data.reacao.emoji && data.reacao.emoji.includes('😤')) setMascotMood('irritado');
    else if(data.reacao.emoji && data.reacao.emoji.includes('🥳')) setMascotMood('feliz');
    else setMascotMood('neutro');

    if(data.correto){
      // pequena animação de sucesso
      mascot.classList.add("happy");
      setTimeout(()=>{
        // atualiza hint (nova fase)
        if(data.nova_fase){
          hint.textContent = `${data.nova_fase.emoji} ${data.nova_fase.pergunta}`;
          status.textContent = "";
          input.value = "";
          showBaloonText("Bora pra próxima fase! 😎");
        }
        mascot.classList.remove("happy");
      },1400);
    } else {
      // erro: sacudir mascot
      mascot.classList.add("shake");
      setTimeout(()=> mascot.classList.remove("shake"),600);
      input.value = "";
    }
  }catch(e){
    console.error(e);
  }
});

// mostrar balão inicial
setTimeout(()=> showBaloonText("Eu sou o Luiz 🤓. Vou te corrigir com carinho — e um pouco de sarcasmo."), 700);
