const modulos = [
  ['Pastos', '/pasto', '/apps/pasto/pasto.html'],
  ['Piquetes', '/piquete', '/apps/piquete/piquete.html'],
  ['Animais', '/animal', '/apps/animal/animal.html'],
  ['Alocações', '/alocado', '/apps/alocado/alocado.html'],
];

async function carregarHome() {
  const caixa = document.getElementById('cartoes');
  caixa.innerHTML = modulos
    .map(([nome, , url], i) => `<a class="cartao" href="${url}">
      <div class="numero" id="qtd${i}">…</div><div>${nome}</div></a>`)
    .join('');
  try {
    await Promise.all(modulos.map(async ([, rota], i) => {
      const lista = await apiFetch(rota);
      document.getElementById('qtd' + i).textContent = lista.length;
    }));
  } catch (e) {
    const aviso = document.getElementById('aviso');
    aviso.textContent = e.message;
    aviso.hidden = false;
  }
}

if (Auth.token()) carregarHome();
